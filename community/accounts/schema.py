from .models import Profile as ProfileModel, ProfileImage as ProfileImageModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node, Mutation
from django.contrib.auth.models import User
from oauth2_provider.models import AccessToken
import graphene
from graphql_relay.node.node import from_global_id


class AccountNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['username', 'email']
        only_fields = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_active')
        interfaces = (Node,)

class RegisterAccount(Mutation):
    class Input:
        username = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        password = graphene.String()
        image = graphene.String(required=False)

    ok = graphene.Boolean()
    account = graphene.Field(lambda: AccountNode)

    def mutate(self, args, context, info):
        if context.user.is_authenticated():
            return RegisterAccount(account=context.user, ok=False)
        account = User.objects.create_user(
            username=args.get('username'),
            email=args.get('email'),
            first_name=args.get('first_name'),
            last_name=args.get('last_name'),
            password=args.get('password'),
        )
        image_upload = args.get('image')
        profile = ProfileModel.objects.get(user=account)
        image = None
        if context.FILES and context.method == 'POST' and image_upload:
            image = ProfileImageModel.objects.create(
                image=context.FILES[image_upload],
                profile=profile
            )
        account.save()
        if image:
            image.save()
            profile.save()
        return RegisterAccount(account=account, ok=True)

class ModifyAccount(Mutation):
    class Input:
        email = graphene.String(required=False)

    ok = graphene.Boolean()
    account = graphene.Field(lambda: AccountNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return ModifyAccount(account=None, ok=False)
        user = context.user
        user.__dict__.update(args)
        user.save()
        return ModifyAccount(account=user, ok=True)

class ProfileNode(DjangoObjectType):
    class Meta:
        model = ProfileModel
        filter_fields = ['user', 'interests']
        interfaces = (Node,)

class ModifyProfile(Mutation):
    class Input:
        interests = graphene.String(required=False)
        phone_number = graphene.String(required=False)
        image = graphene.ID(required=False)

    ok = graphene.Boolean()
    profile = graphene.Field(lambda: ProfileNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return ModifyProfile(profile=None, ok=False)
        user = context.user
        profile = ProfileModel.objects.get(user=user)
        image_id = args.pop('image', None)
        if image_id:
            image_id = from_global_id(image_id)
            image = ProfileImageModel.objects.get(profile=profile, id=image_id)
            profile.image = image
        profile.__dict__.update(args)
        profile.save()
        return ModifyProfile(profile=profile, ok=True)


class ProfileImageNode(DjangoObjectType):
    class Meta:
        model = ProfileImageModel
        filter_fields = ['profile']
        interfaces = (Node,)

class UploadProfileImage(Mutation):
    class Input:
        user = graphene.ID(required=False)
        image = graphene.String()
        set_current = graphene.Boolean(required=False)

    ok = graphene.Boolean()
    profile = graphene.Field(lambda: ProfileNode)
    image = graphene.Field(lambda: ProfileImageNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return UploadProfileImage(profile=None, ok=False)
        user_id = args.get('user')
        user = User.objects.get(id=from_global_id(user_id)) if user_id else context.user
        profile = user.profile
        image_upload = args.get('image')
        if context.FILES and context.method == 'POST' and image_upload:
            image = ProfileImageModel.objects.create(
                image=context.FILES[image_upload],
                profile=profile
            )
            image.save()
        if args.get('set_current'):
            profile.image = image
            profile.save()
        return UploadProfileImage(profile=profile, image=image, ok=True)


class Query(AbstractType):
    profile = Node.Field(ProfileNode)
    all_profiles = DjangoFilterConnectionField(ProfileNode)
    my_profile = graphene.Field(ProfileNode)
    profile_image = Node.Field(ProfileImageNode)
    all_profile_images = DjangoFilterConnectionField(ProfileImageNode)
    my_account = graphene.Field(AccountNode)

    def resolve_my_profile(self, args, context, info):
        if not context.user.is_authenticated():
            return ProfileModel.objects.none()
        else:
            return ProfileModel.objects.get(user=context.user)

    def resolve_my_account(self, args, context, info):
        if not context.user.is_authenticated():
            return User.objects.none()
        else:
            return context.user

class Mutation(AbstractType):
    register_account = RegisterAccount.Field()
    modify_account = ModifyAccount.Field()
    modify_profile = ModifyProfile.Field()

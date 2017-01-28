from .models import Profile as ProfileModel, ProfileImage as ProfileImageModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node
from django.contrib.auth.models import User
from oauth2_provider.models import AccessToken
import graphene


class AccountNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['username', 'email']
        only_fields = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_active')
        interfaces = (Node,)

class ProfileNode(DjangoObjectType):
    class Meta:
        model = ProfileModel
        filter_fields = ['user', 'interests']
        interfaces = (Node,)


class ProfileImageNode(DjangoObjectType):
    class Meta:
        model = ProfileImageModel
        filter_fields = ['profile']
        interfaces = (Node,)

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

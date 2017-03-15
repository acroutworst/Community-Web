from .models import Community as CommunityModel, CommunityUserProfile as ProfileModel, Post as PostModel, PostImage as PostImageModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node, Mutation
from django.contrib.auth.models import User
from django.utils import timezone
import graphene
from graphql_relay.node.node import from_global_id


class CommunityNode(DjangoObjectType):
    class Meta:
        model = CommunityModel
        filter_fields = ['title', 'acronym', 'creator', 'date_created', 'slug']
        interfaces = (Node,)


class ModifyCommunity(Mutation):
    class Input:
        community = graphene.ID()
        acronym = graphene.String()
        phone_number = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    community = graphene.Field(lambda: CommunityNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return ModifyCommunity(community=None, ok=False)
        community_id = from_global_id(args.get('community'))[1]
        community = CommunityModel.objects.get(id=community_id)
        vals = args
        vals.pop('community', None)
        vals.pop('user', None)
        community.__dict__.update(vals)
        community.save()
        return ModifyCommunity(community=community, ok=True)


class RegisterCommunity(Mutation):
    class Input:
        title = graphene.String()
        acronym = graphene.String()
        phone_number = graphene.String()
        description = graphene.String()
        slug = graphene.String()

    ok = graphene.Boolean()
    community = graphene.Field(lambda: CommunityNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return RegisterCommunity(community=None, ok=False)
        community = CommunityModel(
            title=args.get('title'),
            acronym=args.get('acronym'),
            phone_number=args.get('phone_number'),
            description=args.get('description'),
            creator=context.user,
            date_created=timezone.now(),
            slug=args.get('slug'),
        )
        community.save()
        ok = True
        return RegisterCommunity(community=community, ok=ok)


class JoinCommunity(Mutation):
    class Input:
        community = graphene.ID()
        department = graphene.String()
        position = graphene.String()

    ok = graphene.Boolean()
    community = graphene.Field(lambda: CommunityNode)
    profile = graphene.Field(lambda: CommunityUserProfileNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return JoinCommunity(community=None, profile=None, ok=False)
        community = CommunityModel.objects.get(id=from_global_id(args.get('community'))[1])
        user = context.user
        profile = ProfileModel(
            community=community,
            user=user,
            department=args.get('department'),
            position=args.get('position'),
        )
        profile.save()
        ok = True
        return JoinCommunity(community=community, profile=profile, ok=ok)


class LeaveCommunity(Mutation):
    class Input:
        community = graphene.ID()

    ok = graphene.Boolean()
    community = graphene.Field(lambda: CommunityNode)
    profile = graphene.Field(lambda: CommunityUserProfileNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return LeaveCommunity(community=None, profile=None, ok=False)
        community = from_global_id(args.get('community'))[1]
        user = context.user
        profile = ProfileModel.objects.get(community_id=community, user=user)
        profile.active = False
        profile.save()
        ok = True
        return LeaveCommunity(community=community, profile=profile, ok=ok)


class CommunityUserProfileNode(DjangoObjectType):
    class Meta:
        model = ProfileModel
        filter_fields = ['user', 'community', 'department', 'position', 'active']
        interfaces = (Node,)


class PostNode(DjangoObjectType):
    class Meta:
        model = PostModel
        filter_fields = ['community', 'user', 'create_date', 'active']
        interfaces = (Node,)


class RegisterPost(Mutation):
    class Input:
        community = graphene.ID()
        text = graphene.String()
        image = graphene.String(required=False)

    ok = graphene.Boolean()
    post = graphene.Field(lambda: PostNode)
    image = graphene.Field(lambda: PostImageNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return RegisterPost(post=None, image=None, ok=False)
        community = from_global_id(args.get('community'))[1]
        post = PostModel.objects.create(
            community=CommunityModel.objects.get(id=community),
            user=context.user,
            text=args.get('text'),
        )
        post.save()
        print('post saved')
        image_upload = args.get('image')
        image = None
        if context.FILES and context.method == 'POST' and image_upload:
            image = PostImageModel(
                image=context.FILES[image_upload],
                post=post
            )
            image.save()
        return RegisterPost(ok=True, post=post, image=image)


class ModifyPost(Mutation):
    class Input:
        community = graphene.ID()
        post = graphene.ID()
        text = graphene.String()
        image = graphene.String(required=False)
        active = graphene.Boolean(required=False)

    ok = graphene.Boolean()
    post = graphene.Field(lambda: PostNode)
    image = graphene.Field(lambda: PostImageNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return ModifyPost(post=None, image=None, ok=False)
        community = from_global_id(args.get('community'))[1]
        post = PostImageModel.objects.get(id=from_global_id(args.get('post'))[1], community=community)
        if not post or post.user != context.user:
            return ModifyPost(post=None, image=None, ok=False)
        post.active = args.get('active')
        post.text = args.get('text')
        post.save()
        image_upload = args.get('image')
        image = None
        if context.FILES and context.method == 'POST' and image_upload:
            old_images = PostImageModel.objects.filter(post=post)
            if len(old_images) > 0:
                for i in old_images:
                    i.delete()
            image = PostImageModel(
                image=context.FILES[image_upload],
                post=post
            )
            image.save()
        return ModifyPost(ok=True, post=post, image=image)


class PostImageNode(DjangoObjectType):
    class Meta:
        model = PostImageModel
        filter_fields = ['post']
        interfaces = (Node,)


class ModifyPostImage(Mutation):
    class Input:
        community = graphene.ID()
        post = graphene.ID()
        image = graphene.ID()
        active = graphene.Boolean()

    ok = graphene.Boolean()
    image = graphene.Field(lambda: PostImageNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return ModifyPostImage(image=None, ok=False)
        community_id = from_global_id(args.get('community'))[1]
        post_id = from_global_id(args.get('post'))[1]
        image_id = from_global_id(args.get('image'))[1]
        image = PostImageModel.objects.get(post_id=post_id, post__community_id=community_id, id=image_id)
        if not image or image.post.user != context.user:
            return ModifyPostImage(image=None, ok=False)
        image.active = args.get('active')
        image.save()
        return ModifyPostImage(image=image, ok=True)


class Query(AbstractType):
    community = Node.Field(CommunityNode)
    all_communities = DjangoFilterConnectionField(CommunityNode)
    community_user_profile = Node.Field(CommunityUserProfileNode)
    all_community_user_profiles = DjangoFilterConnectionField(CommunityUserProfileNode)
    my_communities = DjangoFilterConnectionField(CommunityNode)
    post = Node.Field(PostNode)
    all_posts = DjangoFilterConnectionField(PostNode)
    post_image = Node.Field(PostImageNode)
    all_post_images = DjangoFilterConnectionField(PostImageNode)

    def resolve_my_communities(self, args, context, info):
        if not context.user.is_authenticated():
            return CommunityModel.objects.none()
        else:
            return CommunityModel.objects.filter(communityuserprofile__user=context.user, communityuserprofile__active=True, **args)


class Mutation(AbstractType):
    register_community = RegisterCommunity.Field()
    join_community = JoinCommunity.Field()
    leave_community = LeaveCommunity.Field()
    modify_community = ModifyCommunity.Field()
    modify_post = ModifyPost.Field()
    register_post = RegisterPost.Field()
    modify_post_image = ModifyPostImage.Field()

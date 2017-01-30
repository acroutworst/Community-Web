from .models import Community as CommunityModel, CommunityUserProfile as ProfileModel
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
        user = graphene.ID(required=False)
        acronym = graphene.String()
        phone_number = graphene.String()
        description = graphene.String()


    ok = graphene.Boolean()
    community = graphene.Field(lambda: CommunityNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return False
        community_id = from_global_id(args.get('community'))[1]
        community = CommunityModel.objects.get(id=community_id)
        print(args)
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
            return False
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
        user = graphene.ID(required=False)
        department = graphene.String()
        position = graphene.String()

    ok = graphene.Boolean()
    community = graphene.Field(lambda: CommunityNode)
    profile = graphene.Field(lambda: CommunityUserProfileNode)

    def mutate(self, args, context, info):
        community = CommunityModel.objects.get(id=from_global_id(args.get('community'))[1])
        if args.get('user'):
            user = User.objects.get(id=from_global_id(args.get('user'))[1])
        else:
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
        user = graphene.ID(required=False)

    ok = graphene.Boolean()
    community = graphene.Field(lambda: CommunityNode)
    profile = graphene.Field(lambda: CommunityUserProfileNode)

    def mutate(self, args, context, info):
        community = from_global_id(args.get('community'))[1]
        if args.get('user'):
            user = User.objects.get(id=from_global_id(args.get('user'))[1])
        else:
            user = context.user
        profile = ProfileModel.objects.get(community_id=community, user=user)
        profile.active = False
        profile.save()
        ok = True
        return JoinCommunity(community=community, profile=profile, ok=ok)

class CommunityUserProfileNode(DjangoObjectType):
    class Meta:
        model = ProfileModel
        filter_fields = ['user', 'community', 'department', 'position', 'active']
        interfaces = (Node,)


class Query(AbstractType):
    community = Node.Field(CommunityNode)
    all_communities = DjangoFilterConnectionField(CommunityNode)
    community_user_profile = Node.Field(CommunityUserProfileNode)
    all_community_user_profiles = DjangoFilterConnectionField(CommunityUserProfileNode)
    my_communities = DjangoFilterConnectionField(CommunityNode)

    def resolve_my_communities(self, args, context, info):
        if not context.user.is_authenticated():
            return CommunityModel.objects.none()
        else:
            return CommunityModel.objects.filter(communityuserprofile__user=context.user, communityuserprofile__active=True)

class Mutation(AbstractType):
    register_community = RegisterCommunity.Field()
    join_community = JoinCommunity.Field()
    leave_community = LeaveCommunity.Field()
    modify_community = ModifyCommunity.Field()

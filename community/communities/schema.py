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

class RegisterCommunity(Mutation):
    class Input:
        title = graphene.String()
        acronym = graphene.String()
        phone_number = graphene.String()
        description = graphene.String()
        creator = graphene.ID()
        slug = graphene.String()

    ok = graphene.Boolean()
    community = graphene.Field(lambda: CommunityNode)

    def mutate(self, args, context, info):
        creator_id = from_global_id(args.get('creator'))[1]
        print(creator_id)
        community = CommunityModel(
            title=args.get('title'),
            acronym=args.get('acronym'),
            phone_number=args.get('phone_number'),
            description=args.get('description'),
            creator=User.objects.get(id=creator_id),
            date_created=timezone.now(),
            slug=args.get('slug'),
        )
        community.save()
        ok = True
        return RegisterCommunity(community=community, ok=ok)

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

class Mutation(AbstractType):
    register_community = RegisterCommunity.Field()

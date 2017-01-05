from .models import Community as CommunityModel, CommunityUserProfile as ProfileModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node


class CommunityNode(DjangoObjectType):
    class Meta:
        model = CommunityModel
        filter_fields = ['title', 'acronym', 'creator', 'date_created', 'slug']
        interfaces = (Node,)


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

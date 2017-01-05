import community.meetups.schema
import community.communities.schema
import community.accounts.schema
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node
from django.contrib.auth.models import User as UserModel
import graphene
from graphene_django.debug import DjangoDebug


class UserNode(DjangoObjectType):
    class Meta:
        model = UserModel
        filter_fields = ['id', 'email']
        interfaces = (Node,)


class Query(community.meetups.schema.Query,
            community.communities.schema.Query,
            community.accounts.schema.Query,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')
    user = Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

schema = graphene.Schema(query=Query)

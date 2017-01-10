import community.meetups.schema
import community.communities.schema
import community.accounts.schema
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node, ObjectType
import django.contrib.auth
import graphene
from graphene_django.debug import DjangoDebug
from graph_auth.schema import Query as AuthQuery, Mutation as AuthMutation, UserNode as AuthUserNode


class CommunityUserNode(AuthUserNode):
    class Meta:
        model = django.contrib.auth.get_user_model()
        filter_fields = ['id', 'email']
        interfaces = (Node,)

    # @classmethod
    # def get_node(cls, id, context, info):
    #     user = super(UserNode, cls).get_node(id, context, info)
    #     if context.user.id and user.id == context.user.id:
    #         return user
    #     else:
    #         return None

class UserQuery(AuthQuery):
    all_users = DjangoFilterConnectionField(CommunityUserNode)

# UserQuery,
# community.meetups.schema.Query,
# community.communities.schema.Query,
# community.accounts.schema.Query,

class Query(UserQuery,
            community.communities.schema.Query,
            community.meetups.schema.Query,
            community.accounts.schema.Query,
            ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(AuthMutation, community.communities.schema.Mutation, ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

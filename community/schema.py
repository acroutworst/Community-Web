import community.meetups.schema
import community.communities.schema
import community.accounts.schema
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node, ObjectType
from django.contrib.auth.models import User as UserModel
import graphene
from graphene_django.debug import DjangoDebug
from graph_auth.schema import Query as AuthQuery, Mutation as AuthMutation


# class UserNode(DjangoObjectType):
#     class Meta:
#         model = UserModel
#         filter_fields = ['id', 'email']
#         interfaces = (Node,)
#
#     @classmethod
#     def get_node(cls, id, context, info):
#         user = super(UserNode, cls).get_node(id, context, info)
#         if context.user.id and user.id == context.user.id:
#             return user
#         else:
#             return None
#
# class UserQuery(AbstractType):
#
#     user = Node.Field(UserNode)
#     all_users = DjangoFilterConnectionField(UserNode)
#     me = graphene.Field(UserNode)
#
#     def resolve_me(self, args, context, info):
#         UserNode.get_node(context.user.id, context, info)

# UserQuery,
# community.meetups.schema.Query,
# community.communities.schema.Query,
# community.accounts.schema.Query,

class Query(AuthQuery,
            community.communities.schema.Query,
            community.meetups.schema.Query,
            community.accounts.schema.Query,
            ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(AuthMutation, ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

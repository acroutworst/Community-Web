import community.meetups.schema
import community.communities.schema
import community.accounts.schema
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node, ObjectType
import django.contrib.auth
import graphene
from graphene_django.views import GraphQLView
from graphene_django.debug import DjangoDebug
from graph_auth.schema import Query as AuthQuery, Mutation as AuthMutation, UserNode as AuthUserNode
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse


class ProtectedGraphQLEndpoint(ProtectedResourceView, GraphQLView):
    pass


class Query(community.communities.schema.Query,
            community.meetups.schema.Query,
            community.accounts.schema.Query,
            AuthQuery,
            ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(AuthMutation,
              community.communities.schema.Mutation,
              community.meetups.schema.Mutation,
              ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

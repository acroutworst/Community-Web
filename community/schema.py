from community.meetups.schema import Mutation as MeetupMutation, Query as MeetupQuery
from community.communities.schema import Mutation as CommunityMutation, Query as CommunityQuery
from community.events.schema import Query as EventQuery, Mutation as EventMutation
from community.groups.schema import Query as GroupQuery, Mutation as GroupMutation
import community.accounts.schema
import graphene
from graphene import ObjectType
from graphene_django.views import GraphQLView
from graphene_django.debug import DjangoDebug
from oauth2_provider.views.generic import ProtectedResourceView

class ProtectedGraphQLEndpoint(ProtectedResourceView, GraphQLView):
    pass


class Query(
            community.accounts.schema.Query,
            CommunityQuery,
            MeetupQuery,
            GroupQuery,
            EventQuery,
            ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(
            community.accounts.schema.Mutation,
            GroupMutation,
            MeetupMutation,
            EventMutation,
            CommunityMutation,
            ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

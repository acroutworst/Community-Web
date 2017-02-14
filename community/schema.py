from community.meetups.schema import Mutation as MeetupMutation
from community.communities.schema import Mutation as CommunityMutation
from community.events.schema import Query as EventQuery, Mutation as EventMutation
import community.accounts.schema
import graphene
from graphene import ObjectType
from graphene_django.views import GraphQLView
from graphene_django.debug import DjangoDebug
from oauth2_provider.views.generic import ProtectedResourceView

class ProtectedGraphQLEndpoint(ProtectedResourceView, GraphQLView):
    pass


class Query(community.communities.schema.Query,
            community.meetups.schema.Query,
            community.accounts.schema.Query,
            EventQuery,
            ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(
            community.accounts.schema.Mutation,
            MeetupMutation,
            EventMutation,
            CommunityMutation,
            ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

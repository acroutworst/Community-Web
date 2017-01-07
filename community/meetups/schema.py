from .models import Meetup as MeetupModel, Attendee as AttendeeModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node, ObjectType
import graph_auth.schema

class MeetupNode(DjangoObjectType):
    class Meta:
        model = MeetupModel
        filter_fields = ['community', 'active', 'private', 'creator', 'name']
        interfaces = (Node,)

        # @classmethod
        # def get_node(cls, id, context, info):
        #     try:
        #         meetup = cls._meta.model.objects.get(id=id)
        #     except cls._meta.model.DoesNotExist:
        #         return None

class AttendeeNode(DjangoObjectType):
    class Meta:
        model = AttendeeModel
        filter_fields = ['meetup', 'user', 'status']
        interfaces = (Node,)


class Query(AbstractType):
    meetup = Node.Field(MeetupNode)
    all_meetups = DjangoFilterConnectionField(MeetupNode)
    attendee = Node.Field(AttendeeNode)
    all_attendees = DjangoFilterConnectionField(AttendeeNode)
    my_meetups = DjangoFilterConnectionField(MeetupNode)

    def resolve_my_meetups(self, args, context, info):
        if not context.user.is_authenticated():
            return MeetupModel.objects.none()
        else:
            return MeetupModel.objects.filter(attendee__user=context.user)

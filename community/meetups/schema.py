from .models import Meetup as MeetupModel, Attendee as AttendeeModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node


class MeetupNode(DjangoObjectType):
    class Meta:
        model = MeetupModel
        filter_fields = ['community', 'active', 'private', 'creator', 'name']
        interfaces = (Node,)


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
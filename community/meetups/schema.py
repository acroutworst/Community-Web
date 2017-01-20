from .models import Meetup as MeetupModel, Attendee as AttendeeModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node, ObjectType, Mutation
from django.utils import timezone
import graph_auth.schema
import graphene
from community.communities.models import Community
from django.contrib.auth.models import User
from graphql_relay.node.node import from_global_id

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
    def get_meetup(self):
        return self.model

class AttendeeNode(DjangoObjectType):
    class Meta:
        model = AttendeeModel
        filter_fields = ['meetup', 'user', 'status']
        interfaces = (Node,)

class RegisterMeetup(Mutation):
    class Input:
        name = graphene.String()
        description = graphene.String()
        max_attendees = graphene.Int()
        private = graphene.Boolean()
        duration = graphene.Int()
        creator = graphene.ID()
        community = graphene.ID()

    ok = graphene.Boolean()
    meetup = graphene.Field(lambda: MeetupNode)

    def mutate(self, args, context, info):
        creator_id = from_global_id(args.get('creator'))[1]
        community_id = from_global_id(args.get('community'))[1]
        meetup = MeetupModel(
            name=args.get('name'),
            description=args.get('description'),
            max_attendees=args.get('max_attendees'),
            private=args.get('private'),
            duration=args.get('duration'),
            creator=User.objects.get(id=creator_id),
            community=Community.objects.get(id=community_id),
            created_date=timezone.now(),
        )
        meetup.save()
        ok = True
        return RegisterMeetup(meetup=meetup, ok=ok)

class AttendMeetup(Mutation):
    class Input:
        meetup = graphene.ID()
        status = graphene.String()
        community = graphene.ID()
        user = graphene.ID(required=False)

    ok = graphene.Boolean()
    attendee = graphene.Field(lambda: AttendeeNode)
    meetup = graphene.Field(lambda: MeetupNode)

    def mutate(self, args, context, info):
        meetup_id = from_global_id(args.get('meetup'))[1]
        community_id = from_global_id(args.get('community'))[1]
        meetup = MeetupModel.objects.get(community_id=community_id, id=meetup_id)
        if args.get('user'):
            user = User.objects.get(id=from_global_id(args.get('user'))[1])
        else:
            user = context.user
        attendee = AttendeeModel(
            meetup=meetup,
            user=user,
            status=args.get('status'),
            signup_time=timezone.now(),
            updated=timezone.now(),
        )
        attendee.save()
        ok = True
        return AttendMeetup(attendee=attendee, meetup=meetup, ok=ok)

class ModifyMeetup(Mutation):
    class Input:
        meetup = graphene.ID()
        community = graphene.ID()
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        max_attendees = graphene.Int(required=False)
        private = graphene.Boolean(required=False)
        duration = graphene.Int(required=False)

    ok = graphene.Boolean()
    meetup = graphene.Field(lambda: MeetupNode)

    def mutate(self, args, context, info):
        meetup_id = from_global_id(args.get('meetup'))[1]
        community_id = from_global_id(args.get('community'))[1]
        user = context.user
        meetup = MeetupModel.objects.get(community_id=community_id, id=meetup_id)
        name = args.get('name')
        description = args.get('description')
        max_attendees = args.get('max_attendees')
        private = args.get('private')
        duration = args.get('duration')
        if name:
            meetup.name = name
        if description:
            meetup.description = description
        if max_attendees:
            meetup.max_attendees = max_attendees
        if private:
            meetup.private = private
        if duration:
            meetup.duration = duration
        meetup.save()
        ok = True
        return ModifyMeetup(meetup=meetup, ok=ok)

class UpdateAttendeeStatus(Mutation):
    class Input:
        meetup = graphene.ID()
        status = graphene.String()
        community = graphene.ID()
        user = graphene.ID(required=False)

    ok = graphene.Boolean()
    attendee = graphene.Field(lambda: AttendeeNode)
    meetup = graphene.Field(lambda: MeetupNode)

    def mutate(self, args, context, info):
        meetup_id = from_global_id(args.get('meetup'))[1]
        community_id = from_global_id(args.get('community'))[1]
        if args.get('user'):
            user = User.objects.get(id=from_global_id(args.get('user'))[1])
        else:
            user = context.user
        AttendeeModel.objects.get(user=user, community_id=community_id, meetup_id=meetup_id)
        attendee.status = args.get('status')
        attendee.save()
        ok = True
        return AttendMeetup(attendee=attendee, meetup=meetup, ok=ok)

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

class Mutation(AbstractType):
    register_meetup = RegisterMeetup.Field()
    attend_meetup = AttendMeetup.Field()
    modify_meetup = ModifyMeetup.Field()
    update_attendee_status = UpdateAttendeeStatus.Field()
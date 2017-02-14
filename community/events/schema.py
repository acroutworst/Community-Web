from .models import Event as EventModel, EventAttendee as AttendeeModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node, ObjectType, Mutation
from django.utils import timezone
import graph_auth.schema
import graphene
from community.communities.models import Community
from django.contrib.auth.models import User
from graphql_relay.node.node import from_global_id

class EventNode(DjangoObjectType):
    class Meta:
        model = EventModel
        filter_fields = [
        'community',
        'created_date',
        'creator',
        'title',
        'start_datetime',
        'end_datetime',
        'description',
        'location',
        'active',
        'private',
        ]
        interfaces = (Node,)

    def get_event(self):
        return self.model
#
# class AttendeeNode(DjangoObjectType):
#     class Meta:
#         model = AttendeeModel
#         filter_fields = ['event', 'user', 'status']
#         interfaces = (Node,)


class ModifyEvent(Mutation):
    class Input:
        community = graphene.ID()
        event = graphene.ID()
        description = graphene.String(required=False)
        active = graphene.Boolean(required=False)
        start_datetime = graphene.String(required=False)
        end_datetime = graphene.String(required=False)
        location = graphene.String(required=False)
        private = graphene.Boolean(required=False)
        active = graphene.Boolean(required=False)

    ok = graphene.Boolean()
    event = graphene.Field(lambda: EventNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return False
        community_id = from_global_id(args.get('community'))[1]
        event_id = from_global_id(args.get('event'))[1]
        event = EventModel.objects.get(id=event_id, community=Community.objects.get(id=community_id))
        if context.user != event.creator:
            return False
        vals = args
        vals.pop('community', None)
        vals.pop('event', None)
        event.__dict__.update(vals)
        event.save()
        return ModifyEvent(event=event, ok=True)


class RegisterEvent(Mutation):
    class Input:
        community = graphene.ID()
        title = graphene.String()
        start_datetime = graphene.String()
        end_datetime = graphene.String()
        description = graphene.String()
        location = graphene.String()
        private = graphene.Boolean()

    ok = graphene.Boolean()
    event = graphene.Field(lambda: EventNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return False
        community_id = from_global_id(args.get('community'))[1]
        event = EventModel(
            title = args.get('name'),
            start_datetime = args.get('start_time'),
            end_datetime = args.get('end_time'),
            description = args.get('description'),
            location = args.get('location'),
            active = True,
            private = args.get('private'),
            creator=context.user,
            community=Community.objects.get(id=community_id),
            created_date=timezone.now(),
        )
        event.save()
        ok = True
        return RegisterEvent(event=event, ok=ok)

# class AttendEvent(Mutation):
#     class Input:
#         event = graphene.ID()
#         status = graphene.String()
#         community = graphene.ID()
#         user = graphene.ID(required=False)
#
#     ok = graphene.Boolean()
#     attendee = graphene.Field(lambda: AttendeeNode)
#     event = graphene.Field(lambda: EventNode)
#
#     def mutate(self, args, context, info):
#         event_id = from_global_id(args.get('event'))[1]
#         community_id = from_global_id(args.get('community'))[1]
#         event = EventModel.objects.get(community_id=community_id, id=event_id)
#         if args.get('user'):
#             user = User.objects.get(id=from_global_id(args.get('user'))[1])
#         else:
#             user = context.user
#         attendee = AttendeeModel(
#             event=event,
#             user=user,
#             status=args.get('status'),
#             signup_time=timezone.now(),
#             updated=timezone.now(),
#         )
#         attendee.save()
#         ok = True
#         return AttendEvent(attendee=attendee, event=event, ok=ok)
#
#
# class UpdateAttendeeStatus(Mutation):
#     class Input:
#         event = graphene.ID()
#         status = graphene.String()
#         community = graphene.ID()
#         user = graphene.ID(required=False)
#
#     ok = graphene.Boolean()
#     attendee = graphene.Field(lambda: AttendeeNode)
#     event = graphene.Field(lambda: EventNode)
#
#     def mutate(self, args, context, info):
#         event_id = from_global_id(args.get('event'))[1]
#         community_id = from_global_id(args.get('community'))[1]
#         if args.get('user'):
#             user = User.objects.get(id=from_global_id(args.get('user'))[1])
#         else:
#             user = context.user
#         AttendeeModel.objects.get(user=user, community_id=community_id, event_id=event_id)
#         attendee.status = args.get('status')
#         attendee.save()
#         ok = True
#         return AttendEvent(attendee=attendee, event=event, ok=ok)
#
class Query(AbstractType):
    event = Node.Field(EventNode)
    all_events = DjangoFilterConnectionField(EventNode)
    # attendee = Node.Field(AttendeeNode)
    # all_attendees = DjangoFilterConnectionField(AttendeeNode)
    my_events = DjangoFilterConnectionField(EventNode)

    def resolve_my_events(self, args, context, info):
        if not context.user.is_authenticated():
            return EventModel.objects.none()
        else:
            return EventModel.objects.filter(attendee__user=context.user)

class Mutation(AbstractType):
    register_event = RegisterEvent.Field()
    modify_event = ModifyEvent.Field()
    # attend_event = AttendEvent.Field()
    # update_attendee_status = UpdateAttendeeStatus.Field()

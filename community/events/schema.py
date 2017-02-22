from .models import Event as EventModel, EventAttendee, EventImage
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
        image_upload = graphene.String(required=False)
        image = graphene.ID(required=False)

    ok = graphene.Boolean()
    event = graphene.Field(lambda: EventNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return False
        community_id = from_global_id(args.get('community'))[1]
        event_id = from_global_id(args.get('event'))[1]
        event = EventModel.objects.get(id=event_id, community=Community.objects.get(id=community_id))
        image_id = from_global_id(args.pop('image', None))[1]
        if context.user != event.creator:
            return ModifyEvent(event=None, ok=False)
        if image_id:
            image = EventImage.objects.get(event=event, id=image_id)
            event.image = image
        image_upload = args.pop('image_upload', None)
        if context.FILES and context.method == 'POST' and image_upload:
            image = EventImage(
                image=context.FILES[image_upload],
                event=event
            )
            image.save()
            event.image = image
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
        image = graphene.String(required=False)

    ok = graphene.Boolean()
    event = graphene.Field(lambda: EventNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return RegisterEvent(event=None, ok=False)
        community_id = from_global_id(args.get('community'))[1]
        event = EventModel(
            title = args.get('title'),
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
        image_upload = args.get('image')
        image = None
        if context.FILES and context.method == 'POST' and image_upload:
            image = EventImage(
                image=context.FILES[image_upload],
                group=group
            )
            event.image = image
        event.save()
        if image:
            image.save()
        ok = True
        return RegisterEvent(event=event, ok=ok)

class EventImageNode(DjangoObjectType):
    class Meta:
        model = EventImage
        filter_fields = ['event']
        interfaces = (Node,)

class UploadEventImage(Mutation):
    class Input:
        event = graphene.ID()
        community = graphene.ID()
        image = graphene.String()
        set_current = graphene.Boolean(required=False)

    ok = graphene.Boolean()
    event = graphene.Field(lambda: EventNode)
    image = graphene.Field(lambda: EventImageNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return UploadEventImage(event=None, image=None, ok=False)
        community_id = from_global_id(args.get('community'))[1]
        event_id = from_global_id(args.get('event'))[1]
        event = EventModel.objects.get(community__id=community_id, id=event_id)
        image_upload = args.get('image')
        if context.FILES and context.method == 'POST' and image_upload:
            image = EventImage(
                image=context.FILES[image_upload],
                event=event
            )
            image.save()
        if args.get('set_current'):
            event.image = image
            event.save()
        return UploadEventImage(event=event, image=image, ok=True)


class EventAttendeeNode(DjangoObjectType):
    class Meta:
        model = EventAttendee
        filter_fields = ['event', 'user', 'status']
        interfaces = (Node,)


class AttendEvent(Mutation):
    class Input:
        event = graphene.ID()
        status = graphene.String()
        community = graphene.ID()
        user = graphene.ID(required=False)

    ok = graphene.Boolean()
    attendee = graphene.Field(lambda: EventAttendeeNode)
    event = graphene.Field(lambda: EventNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return AttendEvent(ok=False, attendee=None, event=None)
        event_id = from_global_id(args.get('event'))[1]
        community_id = from_global_id(args.get('community'))[1]
        event = EventModel.objects.get(community_id=community_id, id=event_id)
        if args.get('user'):
            user = User.objects.get(id=from_global_id(args.get('user'))[1])
        else:
            user = context.user
        attendee = EventAttendee(
            event=event,
            user=user,
            status=args.get('status'),
            signup_time=timezone.now(),
            updated=timezone.now(),
        )
        attendee.save()
        ok = True
        return AttendEvent(attendee=attendee, event=event, ok=ok)


class UpdateAttendeeStatus(Mutation):
    class Input:
        event = graphene.ID()
        status = graphene.String()
        community = graphene.ID()
        user = graphene.ID(required=False)

    ok = graphene.Boolean()
    attendee = graphene.Field(lambda: EventAttendeeNode)
    event = graphene.Field(lambda: EventNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return AttendEvent(ok=False, attendee=None, event=None)
        event_id = from_global_id(args.get('event'))[1]
        community_id = from_global_id(args.get('community'))[1]
        if args.get('user'):
            user = User.objects.get(id=from_global_id(args.get('user'))[1])
        else:
            user = context.user
        EventAttendee.objects.get(user=user, community_id=community_id, event_id=event_id)
        attendee.status = args.get('status')
        attendee.save()
        ok = True
        return AttendEvent(attendee=attendee, event=event, ok=ok)


class Query(AbstractType):
    event = Node.Field(EventNode)
    all_events = DjangoFilterConnectionField(EventNode)
    event_attendee = Node.Field(EventAttendeeNode)
    all_event_attendees = DjangoFilterConnectionField(EventAttendeeNode)
    my_events = DjangoFilterConnectionField(EventNode)
    event_image = Node.Field(EventImageNode)
    all_event_images = DjangoFilterConnectionField(EventImageNode)

    def resolve_my_events(self, args, context, info):
        if not context.user.is_authenticated():
            return EventModel.objects.none()
        else:
            return EventModel.objects.filter(attendee__user=context.user)

class Mutation(AbstractType):
    register_event = RegisterEvent.Field()
    modify_event = ModifyEvent.Field()
    upload_event_image = UploadEventImage.Field()
    attend_event = AttendEvent.Field()
    update_event_attendee_status = UpdateAttendeeStatus.Field()

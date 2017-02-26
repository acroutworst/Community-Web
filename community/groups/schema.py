from community.communities.models import Community
from .models import Group, GroupMembers, GroupImage
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node, Mutation
from django.utils import timezone
import graphene
from graphql_relay.node.node import from_global_id


class GroupNode(DjangoObjectType):
    class Meta:
        model = Group
        filter_fields = ['community', 'title', 'current_leader', 'active',
                        'create_by', 'create_date']
        interfaces = (Node,)


class RegisterGroup(Mutation):
    class Input:
        community = graphene.ID()
        title = graphene.String()
        description = graphene.String(required=False)
        current_leader = graphene.ID()
        image = graphene.String(required=False)

    ok = graphene.Boolean()
    group = graphene.Field(lambda: GroupNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return RegisterGroup(group=None, ok=False)
        group = Group(
            title=args.get('title'),
            description=args.get('description'),
            create_by=context.user,
            create_date=timezone.now(),
            current_leader=context.user,
            active=True,
            community=Community.objects.get(id=from_global_id(args.pop('community', None))[1])
        )
        image_upload = args.get('image')
        image = None
        if context.FILES and context.method == 'POST' and image_upload:
            image = GroupImage(
                image=context.FILES[image_upload],
                group=group
            )
            group.image = image
        group.save()
        if image: image.save()
        ok = True
        return RegisterGroup(group=group, ok=ok)


class ModifyGroup(Mutation):
    class Input:
        community = graphene.ID()
        group = graphene.ID()
        description = graphene.String(required=False)
        current_leader = graphene.ID(required=False)
        active = graphene.Boolean(required=False)
        image_upload = graphene.String(required=False)
        image = graphene.ID(required=False)

    ok = graphene.Boolean()
    group = graphene.Field(lambda: GroupNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return ModifyGroup(group=None, ok=False)
        community_id = from_global_id(args.pop('community', None))[1]
        group_id = from_global_id(args.pop('group', None))[1]
        image_id = from_global_id(args.pop('image', None))[1]
        group = Group.objects.get(id=group_id, community__id=community_id)
        if context.user != group.create_by:
            return ModifyGroup(group=None, ok=False)
        if image_id:
            image = GroupImage.objects.get(group=group, id=image_id)
            group.image = image
        image_upload = args.pop('image_upload', None)
        if context.FILES and context.method == 'POST' and image_upload:
            image = GroupImage(
                image=context.FILES['image_upload'],
                group=group
            )
            image.save()
            group.image = image
        group.__dict__.update(args)
        group.save()
        return ModifyGroup(group=group, ok=True)

class GroupImageNode(DjangoObjectType):
    class Meta:
        model = GroupImage
        filter_fields = ['group']
        interfaces = (Node,)

class UploadGroupImage(Mutation):
    class Input:
        group = graphene.ID()
        community = graphene.ID()
        image = graphene.String()
        set_current = graphene.Boolean(required=False)

    ok = graphene.Boolean()
    group = graphene.Field(lambda: GroupNode)
    image = graphene.Field(lambda: GroupImageNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return UploadGroupImage(group=None, image=None, ok=False)
        community_id = from_global_id(args.get('community'))[1]
        group_id = from_global_id(args.get('group'))[1]
        group = Group.objects.get(community__id=community_id, id=group_id)
        image_upload = args.get('image')
        if context.FILES and context.method == 'POST' and image_upload:
            image = GroupImage(
                image=context.FILES[image_upload],
                group=group
            )
            image.save()
            if args.get('set_current'):
                group.image = image
                group.save()
        return UploadGroupImage(group=group, image=image, ok=True)

class GroupMembersNode(DjangoObjectType):
    class Meta:
        model = GroupMembers
        filter_fields = ['group', 'user', 'active']
        interfaces = (Node,)


class JoinGroup(Mutation):
    class Input:
        community = graphene.ID()
        group = graphene.ID()
        position = graphene.String(required=False)

    ok = graphene.Boolean()
    group = graphene.Field(lambda: GroupNode)
    group_member = graphene.Field(lambda: GroupMembersNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return JoinGroup(group=None, group_member=None, ok=False)
        community = Community.objects.get(id=from_global_id(args.pop('community', None))[1])
        group = Group.objects.get(id=from_global_id(args.pop('group', None))[1], community=community)
        member = GroupMembers.objects.filter(group=group, user=context.user).first()
        if member and not member.active:
            member.active = True #reactivate membership
        else:
            member = GroupMembers(
            user=context.user,
            group=group,
            community=community,
            position=args.get('position'),
            join_date=timezone.now(),
            last_activity=timezone.now(),
            active=True
            )
        member.save()
        return JoinGroup(group=group, group_member=member, ok=True)


class ModifyGroupMembership(Mutation):
    class Input:
        community = graphene.ID()
        group = graphene.ID()
        position = graphene.String(required=False)
        active = graphene.Boolean(required=False)

    ok = graphene.Boolean()
    group = graphene.Field(lambda: GroupNode)
    group_member = graphene.Field(lambda: GroupMembersNode)

    def mutate(self, args, context, info):
        if not context.user.is_authenticated():
            return ModifyGroupMembership(group=None, group_member=None, ok=False)
        community = Community.objects.get(id=from_global_id(args.pop('community', None))[1])
        group = Group.objects.get(id=from_global_id(args.pop('group', None))[1], community=community)
        member = GroupMembers.objects.filter(group=group, user=context.user).first()
        if not member:
            return ModifyGroupMembership(group=None, group_member=None, ok=False)
        else:
            member.position = args.get('position')
            member.active = args.get('active')
            member.save()
        return ModifyGroupMembership(group=group, group_member=member, ok=True)


class Query(AbstractType):
    group = Node.Field(GroupNode)
    group_image = Node.Field(GroupImageNode)
    all_group_images = DjangoFilterConnectionField(GroupImageNode)
    all_groups = DjangoFilterConnectionField(GroupNode)
    my_groups = DjangoFilterConnectionField(GroupNode)
    group_members = Node.Field(GroupMembersNode)
    all_group_members = DjangoFilterConnectionField(GroupMembersNode)

    def resolve_my_groups(self, args, context, info):
        if not context.user.is_authenticated():
            return Group.objects.none()
        else:
            return Group.objects.filter(groupmembers__user=context.user, groupmembers__active=True)


class Mutation(AbstractType):
    register_group = RegisterGroup.Field()
    join_group = JoinGroup.Field()
    modify_group_membership = ModifyGroupMembership.Field()
    modify_group = ModifyGroup.Field()
    upload_group_image = UploadGroupImage.Field()

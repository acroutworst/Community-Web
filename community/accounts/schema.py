from .models import Profile as ProfileModel, ProfileImage as ProfileImageModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node


class ProfileNode(DjangoObjectType):
    class Meta:
        model = ProfileModel
        filter_fields = ['user', 'interests']
        interfaces = (Node,)


class ProfileImageNode(DjangoObjectType):
    class Meta:
        model = ProfileImageModel
        filter_fields = ['profile']
        interfaces = (Node,)


class Query(AbstractType):
    profile = Node.Field(ProfileNode)
    all_profile = DjangoFilterConnectionField(ProfileNode)
    profile_image = Node.Field(ProfileImageNode)
    all_profile_images = DjangoFilterConnectionField(ProfileImageNode)

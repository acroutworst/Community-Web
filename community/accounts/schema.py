from .models import Profile as ProfileModel, ProfileImage as ProfileImageModel
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import AbstractType, Node
from oauth2_provider.models import AccessToken
import graphene


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
    all_profiles = DjangoFilterConnectionField(ProfileNode)
    my_profile = graphene.Field(ProfileNode)
    profile_image = Node.Field(ProfileImageNode)
    all_profile_images = DjangoFilterConnectionField(ProfileImageNode)

    def resolve_my_profile(self, args, context, info):
        if not context.user.is_authenticated():
            return ProfileModel.objects.none()
        else:
            print (context.user)
            return ProfileModel.objects.get(user=context.user)

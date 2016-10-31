from community.web.models import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ('user', 'position', 'department', 'interests', 'transportation')

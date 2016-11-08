from rest_framework import serializers

from community.accounts.models import Profile


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance

    class Meta:
        model = Profile
        fields = ('user', 'position', 'department', 'interests', 'transportation')

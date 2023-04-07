from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','email']

    def create(self, validated_data):

        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('username 존재')
        else:
            user = User.objects.create(
                username=validated_data['username'],
            )
            user.set_password(validated_data['password'])
            user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)

    class Meta:
        model=Profile
        fields=['id', 'user','nickname', 'university','enter_year','created_at','updated_at']


    def create(self, validated_data):
        if Profile.objects.filter(nickname=validated_data['nickname']).exists():
            raise serializers.ValidationError('nickname 존재')
        else:
            profile = Profile.objects.create(
                nickname=validated_data['nickname'],
                university=validated_data['university'],
                enter_year=validated_data['enter_year']
            )
            profile.save()
        return profile


class FriendSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model=Friend
        fields=['id','user','friend']

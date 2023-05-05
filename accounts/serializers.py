from rest_framework import serializers
from .models import *

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'nickname', 'university','enter_year','created_at','updated_at']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            university=validated_data['university'],
            enter_year=validated_data['enter_year'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호입니다.')
            else:
                return data
        else:
            raise serializers.ValidationError('존재하지 않는 사용자입니다.')


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=['id', 'user','nickname', 'university','enter_year','created_at','updated_at']
#
#
#     def create(self, validated_data):
#         if Profile.objects.filter(nickname=validated_data['nickname']).exists():
#             raise serializers.ValidationError('nickname 존재')
#         else:
#             profile = Profile.objects.create(
#                 nickname=validated_data['nickname'],
#                 university=validated_data['university'],
#                 enter_year=validated_data['enter_year']
#             )
#             profile.save()
#         return profile


class FriendSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model=Friend
        fields=['id','user','friend']




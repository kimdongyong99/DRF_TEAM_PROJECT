from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class Userserializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators = [validate_password])
    checkpassword = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        if data['password'] != data['checkpassword']:
            raise serializers.ValidationError("똑같은 비밀번호를 입력하세요.")
        return data
    
    def create(self, data):
        data.pop('checkpassword')
        
        user = User.objects.create_user(
            username = data['username'],
            email = data['email'],
            password = data['password'],
        )
        return user
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'checkpassword']
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        

class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['image_field', 'email']
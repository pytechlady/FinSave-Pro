from rest_framework import serializers
from .models import User
import re


class RegisterUser(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'password')
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        
        print(email + '.............'+ password)
        
        if not email or not password:
            raise serializers.ValidationError("Email and password are required for registration")
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@-_]).{8,}$"
        if re.match(pattern, password) is None:
            raise serializers.ValidationError('''
            * Password must be at least 8 characters long
            * Must include at least one uppercase letter
            * Must include at least one lowercase
            * Must include a number between 0 and 9
            * Must include at least one character between @ and _''') 
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    

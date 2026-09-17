from rest_framework.serializers import *
from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    password = CharField(write_only=True,required=True)
    confirm_password = CharField(write_only=True,required=True)
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password","confirm_password","phone","profile"]
    
    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise ValidationError("Passwords Miss Match")
        return data
    
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user
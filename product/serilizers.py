from rest_framework.serializers import *
from .models import *

class CategorySerilizer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]
    def create(self, validated_data):
        category_name = validated_data.get("name")
        category = Category.objects.create(name=category_name)
        return category
        
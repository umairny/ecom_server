from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import FileField
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ("pk", "image", "thumb")
        read_only_fields = ("thumb",)


class ProductSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=100, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )

    class Meta:
        model = Products
        fields = ["id", "title", "detail", "qty", "price", "images", "upload_images"]

    def create(self, validated_data):
        # images_data = self.context.get('view').request.FILES
        images_data = validated_data.pop("upload_images")
        product = Products.objects.create(**validated_data)
        for image in images_data:
            print(image)
            Images.objects.create(product=product, image=image)
        return product

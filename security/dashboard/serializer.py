from .models import ImageUpload
from rest_framework import serializers

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('image', 'name')
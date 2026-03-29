from rest_framework import serializers
from .models import QuranResource


class QuranResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuranResource
        fields = "__all__"

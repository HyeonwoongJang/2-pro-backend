from rest_framework import serializers
from wishes.models import Wish

class WishCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ("title", "wish_name", "content", "wish_img")


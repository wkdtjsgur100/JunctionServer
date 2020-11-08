from rest_framework import serializers

from aitojunction.models import Place, UserLike


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class UserLikeSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)

    class Meta:
        model = UserLike
        fields = '__all__'

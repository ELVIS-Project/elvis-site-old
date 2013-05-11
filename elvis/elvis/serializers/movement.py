from rest_framework import serializers
from elvis.models.movement import Movement


class MovementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movement

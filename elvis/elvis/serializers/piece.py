from rest_framework import serializers
from elvis.models.piece import Piece


class PieceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Piece

from rest_framework import serializers
from .models import *


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"





class GamerCardSerializer(serializers.ModelSerializer):
    card_id = serializers.ReadOnlyField(source='card.id')
    title = serializers.ReadOnlyField(source='card.title')
    lvl = serializers.ReadOnlyField(source='card.rarity')
    img = serializers.ReadOnlyField(source='card.img.url')
    suit = serializers.ReadOnlyField(source='card.type.id')
    class Meta:
      model = GamerCard
      exclude = ['user', 'card']




class GamesSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()

    class Meta:
        model = Gamer
        fields = ('nickname', 'coins', 'cards')

    def get_cards(self, obj):
        queryset = GamerCard.objects.filter(user=obj)
        return [GamerCardSerializer(m).data for m in queryset]
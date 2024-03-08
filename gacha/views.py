from .models import Card, GamerCard, Gamer
from .serializers import CardSerializer, GamerCardSerializer, GamesSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, ParseError


from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle
import random

class GetCardInfoView(APIView):
    def get(self, request):
        queryset =  Card.objects.all()
        serializer_for_queryset =  CardSerializer(
            instance=queryset,
            many=True,
        )
        return Response(serializer_for_queryset.data)


class CurrentUserView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        serializer_for_queryset =  GamesSerializer(
             instance= Gamer.objects.get(user=request.user)
        )
        return Response(serializer_for_queryset.data)


class OncePerHourUserThrottle(UserRateThrottle):
    rate = '1/hour'

@api_view(['POST'])
# @throttle_classes([OncePerHourUserThrottle])
def free_coins(request):
    gamer = Gamer.objects.get(user=request.user)
    gamer.coins += 1000;
    gamer.save();
    return Response({"msg":"Теперь у тебя "+ str(gamer.coins) +" монет. Еще бесплатные монеты Ты можешь получить через час.", "coins": gamer.coins})


class Combine(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cardIds = request.data.get("cardIds")
        gamer = Gamer.objects.get(user=request.user)
        rarity = GamerCard.objects.get(id=cardIds[0]).card.rarity
        maxLevel = 4
        if(rarity==maxLevel):
            raise ValidationError({"msg":"Максимальный уровень карт"})
        # проверка подходят ли карты
        cards = []
        for id in cardIds:
            card = GamerCard.objects.filter(id=id, user=gamer)
            if(rarity != card.first().card.rarity):
                raise ValidationError({"msg":"Разный уровень карт"})
            if(card.exists()):
                cards.append(card.first())
            else:
                raise ValidationError({"msg":"Не подходящие карты"})

        for card in cards:
            card.delete()

        # новая карта нужного уровня
        rand = random.randint(0, 2)
        newCard = Card.objects.filter(rarity=rarity+1)[rand]
        newGamerCard = GamerCard.objects.create(user=gamer, card=newCard)
        serializer_for_queryset = GamerCardSerializer(instance=newGamerCard)
        return Response({"card": serializer_for_queryset.data})


class Buy(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # raise ValidationError({"msg":"тест ошибки"})
        gamer = Gamer.objects.get(user=request.user)
        if(gamer.coins<100):
            raise ValidationError({"msg":"Недостаточно монет"})
        # случайная карта начального уровня
        rand = random.randint(0, 2)
        newCard = Card.objects.filter(rarity=1)[rand]
        # добавить выбор не случайной масти
        newGamerCard = GamerCard.objects.create(user=gamer, card=newCard)
        gamer.coins -= 100;
        gamer.save();
        serializer_for_queryset = GamerCardSerializer(instance=newGamerCard )
        return Response( {"coins": gamer.coins, "card": serializer_for_queryset.data})


class Destroy(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cardId = request.data.get("cardId")
        gamer = Gamer.objects.get(user=request.user)
        card = GamerCard.objects.filter(id=cardId, user=gamer).first()
        cardPrice = card.getPrice();
        card.delete()
        gamer.coins += cardPrice;
        gamer.save();
        return Response({"coins": gamer.coins, "cardId": cardId})
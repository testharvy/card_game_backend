from django.db import models
from django.contrib.auth.models import User as DjangoUser

class CardType(models.Model):
    name = models.CharField("название", max_length=255)

    def __str__(self):
        return self.name

class Card(models.Model):
    title = models.CharField("название", max_length=255)
    rarity = models.IntegerField("редкость", default=0)
    type = models.ForeignKey(CardType, on_delete=models.CASCADE, verbose_name='Тип', blank=True, null=True)
    img = models.ImageField(upload_to ='cards/', verbose_name='картинка', null=True, blank=True)

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

    def __str__(self):
        return self.title


class Gamer(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, verbose_name='Пользователь(djanga)')
    nickname = models.CharField("никнейм", max_length=255)
    coins = models.IntegerField("монеты", default=1000)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"

    def __str__(self):
        return self.nickname


class GamerCard(models.Model):
    user = models.ForeignKey(Gamer, on_delete=models.CASCADE, verbose_name='игрок')
    card =  models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name='карта')

    def getPrice(self):
        return self.card.rarity * 50


class ShopItem(models.Model):
    price = models.IntegerField("цена", default=1000)
    discountPrice = models.IntegerField("цена по скидке", default=0)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name='карта')

    def getBuyPrice(self):
        if self.discountPrice != 0:
            return self.discountPrice
        else:
            return self.price
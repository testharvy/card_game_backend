from django.contrib import admin
from .models import *


@admin.register(CardType)
class CardTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("title", "rarity", "type")


class GamerCardInline(admin.TabularInline):
    model = GamerCard

@admin.register(Gamer)
class CardAdmin(admin.ModelAdmin):
    inlines = [
        GamerCardInline,
    ]

@admin.register(GamerCard)
class GamerCardAdmin(admin.ModelAdmin):
    list_display = ("id","user", "card")
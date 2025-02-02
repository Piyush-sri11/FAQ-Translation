from django.contrib import admin
from .models import FAQ, FAQTranslation

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question",)
    search_fields = ("question", "answer")

@admin.register(FAQTranslation)
class FAQTranslationAdmin(admin.ModelAdmin):
    list_display = ("faq", "language", "question")
    search_fields = ("question",)
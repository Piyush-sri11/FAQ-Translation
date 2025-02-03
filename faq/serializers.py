from rest_framework import serializers
from .models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    translated_question = serializers.SerializerMethodField()
    translated_answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ["id", "translated_question", "translated_answer"]

    def get_translated_question(self, obj):
        request = self.context.get("request")
        lang = request.GET.get("lang", "en") if request else "en"
        return obj.get_translation(lang)["question"]

    def get_translated_answer(self, obj):
        request = self.context.get("request")
        lang = request.GET.get("lang", "en") if request else "en"
        return obj.get_translation(lang)["answer"]

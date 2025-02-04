from rest_framework import serializers
from .models import FAQ


class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ["id", "question", "answer"]

    def get_question(self, obj):
        request = self.context.get("request")
        lang = request.GET.get("lang", "en") if request else "en"
        return obj.get_translation(lang)["question"]

    def get_answer(self, obj):
        request = self.context.get("request")
        lang = request.GET.get("lang", "en") if request else "en"
        return obj.get_translation(lang)["answer"]

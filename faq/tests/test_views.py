import pytest
from rest_framework.test import APIClient
from faq.models import FAQ, FAQTranslation


@pytest.mark.django_db
def test_faq_list_api():
    client = APIClient()
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")

    response = client.get("/api/faqs/")
    assert response.status_code == 200
    assert response.data[0]["translated_question"] == "What is Django?"


@pytest.mark.django_db
def test_faq_translation_api():
    client = APIClient()
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")
    FAQTranslation.objects.create(faq=faq, language="fr", question="Qu'est-ce que Django?", answer="Django est un framework web.")

    response = client.get("/api/faqs/?lang=fr")
    assert response.status_code == 200
    assert response.data[0]["translated_question"] == "Qu'est-ce que Django?"

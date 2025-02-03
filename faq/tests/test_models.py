import pytest
from faq.models import FAQ, FAQTranslation
from django.core.cache import cache


@pytest.mark.django_db
def test_faq_creation():
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")
    assert FAQ.objects.count() == 1
    assert str(faq) == "What is Django?"


@pytest.mark.django_db
def test_translation_creation():
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")
    FAQTranslation.objects.create(faq=faq, language="fr", question="Qu'est-ce que Django?", answer="Django est un framework web.")

    translation = FAQTranslation.objects.get(faq=faq, language="fr")
    assert translation.question == "Qu'est-ce que Django?"


@pytest.mark.django_db
def test_get_translation():
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")
    FAQTranslation.objects.create(faq=faq, language="es", question="¿Qué es Django?", answer="Django es un framework web.")

    translation = faq.get_translation("es")
    assert translation["question"] == "¿Qué es Django?"
    assert translation["answer"] == "Django es un framework web."


@pytest.mark.django_db
def test_cache_translation():
    cache.clear()
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")
    FAQTranslation.objects.create(faq=faq, language="de", question="Was ist Django?", answer="Django ist ein Web-Framework.")

    faq.get_translation("de")  # This should store the translation in cache
    cached_data = cache.get(f"faq_{faq.id}_de")

    assert cached_data["question"] == "Was ist Django?"
    assert cached_data["answer"] == "Django ist ein Web-Framework."

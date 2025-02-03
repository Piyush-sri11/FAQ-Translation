import pytest
from django.core.cache import cache
from faq.models import FAQ, FAQTranslation


@pytest.mark.django_db
def test_cache_storage():
    cache.clear()
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")
    FAQTranslation.objects.create(faq=faq, language="hi", question="Django क्या है?", answer="Django एक वेब फ्रेमवर्क है।")

    faq.get_translation("hi")  # Fetch to store in cache
    cached_data = cache.get(f"faq_{faq.id}_hi")

    assert cached_data is not None
    assert cached_data["question"] == "Django क्या है?"


@pytest.mark.django_db
def test_cache_clear_on_update():
    cache.clear()
    faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")
    FAQTranslation.objects.create(faq=faq, language="bn", question="Django কি?", answer="Django একটি ওয়েব ফ্রেমওয়ার্ক।")

    faq.get_translation("bn")
    assert cache.get(f"faq_{faq.id}_bn") is not None

    # Updating FAQ should clear cache
    faq.question = "What is Flask?"
    faq.save()
    assert cache.get(f"faq_{faq.id}_bn") is None

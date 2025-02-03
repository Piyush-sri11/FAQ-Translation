from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from bs4 import BeautifulSoup, NavigableString
from django.core.cache import cache



class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    def __str__(self):
        return self.question[:50]
    
    def translate_html_content(self, content, lang):
        """Translate text while keeping HTML tags intact."""
        soup = BeautifulSoup(content, "html.parser")
        translator = Translator()

        for element in soup.recursiveChildGenerator():
            if isinstance(element, NavigableString) and element.strip():  # Ensure text is not empty
                translated_text = translator.translate(element, src="en", dest=lang).text
                if translated_text is None:  # Handle Google Translate returning None
                    translated_text = ""
                element.replace_with(translated_text)

        return str(soup) 

    def get_translation(self, lang="en"):
        """Retrieve translation from database or generate dynamically."""
        if lang == "en":
            return {"question": self.question, "answer": self.answer}
        
        cache_key = f"faq_{self.id}_{lang}"
        cached_translation = cache.get(cache_key)

        if cached_translation:
            return cached_translation
        
        # Check if translation exists in the database
        translation = FAQTranslation.objects.filter(faq=self, language=lang).first()
        if translation:
            data = {"question": translation.question, "answer": translation.answer}
            cache.set(cache_key, data, timeout=3600)  # Store in Redis for 1 hour
            return data

        # If translation does not exist, generate dynamically
        translator = Translator()
        try:
            translated_question = translator.translate(self.question, src="en", dest=lang).text
            translated_answer = self.translate_html_content(self.answer, lang)

                # Save to database
            FAQTranslation.objects.create(faq=self, language=lang, question=translated_question, answer=translated_answer)

            data = {"question": translated_question, "answer": translated_answer}

            # Store in Redis for faster access
            cache.set(cache_key, data, timeout=3600)
            return data
        
        except Exception as e:
            print(f"Translation Error: {e}")
            return {"question": self.question, "answer": self.answer}  # Fallback to English
        

    def clear_faq_cache(self):
        """Clear all cached translations for this FAQ."""
        # redis_conn = get_redis_connection("default")
        keys = cache.keys(f"faq_{self.id}_*")  # Find all keys for this FAQ
        if keys:
            cache.delete(*keys)  # Delete all keys

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clear_faq_cache()
        

    def delete(self, *args, **kwargs):
        self.clear_faq_cache()
        super().delete(*args, **kwargs)




class FAQTranslation(models.Model):
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=10)  # Language code (e.g., "fr", "es", "de")
    question = models.TextField()
    answer = RichTextField()

    def __str__(self):
        return f"{self.faq.question[:50]} ({self.language})"

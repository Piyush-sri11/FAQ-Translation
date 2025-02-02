from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from bs4 import BeautifulSoup, NavigableString
from django.core.cache import cache
from django_redis import get_redis_connection



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
        
        
        
        # Check if translation exists in the database
        translation = FAQTranslation.objects.filter(faq=self, language=lang).first()
        if translation:
            data = {"question": translation.question, "answer": translation.answer}
            
            return data

        # If translation does not exist, generate dynamically
        translator = Translator()
        try:
            translated_question = translator.translate(self.question, src="en", dest=lang).text
            translated_answer = self.translate_html_content(self.answer, lang)

                # Save to database
            FAQTranslation.objects.create(faq=self, language=lang, question=translated_question, answer=translated_answer)

            data = {"question": translated_question, "answer": translated_answer}

            
            return data
        
        except Exception as e:
            print(f"Translation Error: {e}")
            return {"question": self.question, "answer": self.answer}  # Fallback to English
        

    



class FAQTranslation(models.Model):
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=10)  # Language code (e.g., "fr", "es", "de")
    question = models.TextField()
    answer = RichTextField()

    def __str__(self):
        return f"{self.faq.question[:50]} ({self.language})"

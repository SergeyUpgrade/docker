from rest_framework.serializers import ValidationError

permitted_words = ["youtube.com"]

def validate_permitted_words(value):
    if value.lower() not in permitted_words:
        raise ValidationError("Запрещенная ссылка, можно ссылку только на youtube.com")
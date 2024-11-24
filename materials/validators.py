from rest_framework.serializers import ValidationError

def validate_permitted_words(value):
    if not value:
        return None
    elif 'youtube.com' not in value:
        raise ValidationError("Ссылка на видео разрешена только с сайта youtube.com")
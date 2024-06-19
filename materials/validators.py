from rest_framework.serializers import ValidationError

valid_link = "youtube.com"


def validate_link(value):
    if valid_link not in value:
        raise ValidationError("Некорректная ссылка")

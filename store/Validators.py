from django.core.exceptions import ValidationError

def image_validator(file):
    max_size=50
    if file.size>50*1024:
        raise ValidationError('Image size is greater than 50Kbs!!!!')

def Title_validator(title):
    if type(title)!=str or len(title)==0:
        raise ValidationError("InValid Title")
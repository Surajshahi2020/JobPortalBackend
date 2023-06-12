import re
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.utils.text import slugify
import string, random, re


PANEL_CHOICES = (
    ("Ab", "About Us"),
    ("Pr", "Privacy  and Policy"),
    ("Te", "Terms & Conditions"),
    ("Co", "Contact"),
    ("Na", "Navigation Bar"),
    ("Nl", "Navigation Logo"),
    ("Lc", "Location"),
    ("So", "Social account"),
    ("Fa", "FAQ / Help"),
    ("Fo", "Footer content"),
    ("Fg", "Footer logo"),
    ("Br", "Browse Job Logo"),
    ("No", "Notice"),
    ("E1", "Extra 1"),
    ("E2", "Extra 2"),
    ("E3", "Extra 3"),
)

MSG_TYPES = (
    ("TEXT", "TEXT"),
    ("FILE", "FILE"),
)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def TitleFieldSlug(instance):
    slug = slugify(instance.title[:50])
    Klass = instance.__class__
    if Klass.objects.filter(slug=slug).exists():
        slug = slug + "-" + random_string_generator(size=4)
    return slug


def validate_number(mobile):
    pattern = r"^(?:\+977|977|0)?(?:98[4-7]|97[7-8]|96[4-6]|985|984|980|981|982|961|962|988|960|972|963|972|973|974|975|976|977|978|980|981|982|983|984|985|986)\d{7}$"
    if not re.match(pattern, str(mobile)):
        return False
    return True


def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not re.match(pattern, password):
        raise serializers.ValidationError(
            {
                "title": "Account Registration",
                "message": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
            }
        )
    return password


def validate_image(image):
    pattern = r"^(?:.*\.(jpg|jpeg|png|gif))$"
    if not re.match(pattern, str(image)):
        return False
    return True


def validate_aimage(image):
    url_pattern = (
        "((http|https)://)(www.)?"
        + "[a-zA-Z0-9@:%._\\+~#?&//=]"
        + "{2,256}\\.[a-z]"
        + "{2,6}\\b([-a-zA-Z0-9@:%"
        + "._\\+~#?&//=]*)"
    )
    p = re.compile(url_pattern)
    if re.search(p, image):
        return True
    return False


def validate_date_format(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        return False


def validate_resume(value):
    try:
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                {
                    "title": "Job Apply",
                    "message": "File size should not exceed 10MB.",
                }
            )
        return value
    except AttributeError:
        raise serializers.ValidationError("Invalid file.")


def validate_uuid(id):
    uuid_pattern = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    p = re.compile(uuid_pattern)
    if re.match(p, id):
        return True
    return False

import re


def validate_number(mobile):
    pattern = r"^(?:\+977|977|0)?(?:98[4-7]|97[7-8]|96[4-6]|985|984|980|981|982|961|962|988|960|972|963|972|973|974|975|976|977|978|980|981|982|983|984|985|986)\d{7}$"
    if not re.match(pattern, str(mobile)):
        return False
    return True


def validate_image(image):
    pattern = r"^(?:.*\.(jpg|jpeg|png|gif))$"
    if not re.match(pattern, str(image)):
        return False
    return True

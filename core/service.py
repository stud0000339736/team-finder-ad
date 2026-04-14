import os
import random
import uuid
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from PIL import Image, ImageDraw, ImageFont

from core.constants import (BLACK, BLUE, FONT_SIZE, GREEN, IMAGE_COLOR_TYPE,
                            IMAGE_FORMAT, IMAGE_SIZE, OBJ_PER_PAGE,
                            PATH_TO_FONT, PURPLE, RED, WHITE, YELLOW)


def paginate_queryset(request, queryset, per_page=OBJ_PER_PAGE):
    page_number = request.GET.get('page')
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('avatars/', filename)


def generate_avatar(instance, letter):
    letter = letter.upper()

    size = (IMAGE_SIZE, IMAGE_SIZE)
    background_colors = [
        PURPLE, YELLOW, RED,
        GREEN, BLUE
    ]
    BLACK_COLORS_LETTER = [YELLOW, GREEN]

    back_color = random.choice(background_colors)

    if back_color in BLACK_COLORS_LETTER:
        letter_color = BLACK
    else:
        letter_color = WHITE

    image = Image.new(IMAGE_COLOR_TYPE, size, back_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(PATH_TO_FONT, FONT_SIZE)
    except Exception:
        font = ImageFont.load_default()

    start_pos = (0, 0)
    bbox = draw.textbbox(start_pos, letter, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (size[0] - text_w) / 2 - bbox[0]
    y = (size[1] - text_h) / 2 - bbox[1]
    letter_pos = (x, y)

    draw.text(letter_pos, letter, fill=letter_color, font=font)

    buffer = BytesIO()
    image.save(buffer, format=IMAGE_FORMAT)
    buffer.seek(0)

    file_name = f"{letter}.png"

    instance.avatar.save(file_name, ContentFile(buffer.read()), save=False)

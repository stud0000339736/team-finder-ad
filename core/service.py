import os
import uuid

from django.core.paginator import Paginator


def paginate_queryset(queryset, page_number, per_page):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('avatars/', filename)

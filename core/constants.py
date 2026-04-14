import os
import re

from django.conf import settings

# re
GITHUB_PROJECT_URL_REGEX = re.compile(r'^https://github\.com/[\w-]+/[\w.-]+/?$')
GITHUB_USER_REGEX = re.compile(r'^https://github.com/[\w-]+/?$')
PHONE_REGEX = re.compile(r'(^\+7\d{10}$)|(^8\d{10}$)')

# statuses
STATUS_OPEN = 'open'
STATUS_CLOSED = 'closed'

# max_length
MAX_LENGTH_STATUS = 6
MAX_LENGTH_NAME = 200
MAX_LENGTH_ABOUT = 256
MAX_LENGTH_PHONE = 12

# pagination
OBJ_PER_PAGE = 12

# sizes
IMAGE_SIZE = 128
FONT_SIZE = 64

# Colors
BLUE = '#005EFF'
GREEN = '#00FF48'
RED = '#FF1500'
YELLOW = '#FFC400'
PURPLE = '#8400FF'
BLACK = '#000000'
WHITE = '#FFFFFF'

# Paths
PATH_TO_FONT = os.path.join(
    settings.BASE_DIR,
    'static',
    'fonts',
    'Neue_Haas_Grotesk_Display_Pro_75_Bold.otf'
)

# Types
IMAGE_FORMAT = 'PNG'
IMAGE_COLOR_TYPE = 'RGB'

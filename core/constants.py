import re

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

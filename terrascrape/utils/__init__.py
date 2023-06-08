import uuid
from datetime import datetime

UUID_DATETIME_FORMAT = '%Y%m%d%H%M%S'


def generate_message_uuid():
    return f'{datetime.now().strftime(UUID_DATETIME_FORMAT)}:{uuid.uuid4()}'

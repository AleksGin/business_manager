from datetime import (
    datetime,
    timedelta,
)

import pytest
from uuid import uuid4
import jwt as pyjwt
from freezegun import freeze_time

from core.providers import JWTProvider


class TestJWTProvider:
    """Тестируем JWT Provider - сердце аутентификации"""
    
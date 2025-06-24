from users.interfaces.interfaces import (
    UserActivationManager,
    UserRepository,
)
from core.interfaces import JWTProviderInterface


class UserActivationManagerProvider(UserActivationManager):
    """Имплементация UserActivationManager с хранением токенов в БД"""

    def __init__(
        self,
        user_repo: UserRepository,
    ): ...

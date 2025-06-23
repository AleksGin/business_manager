from abc import abstractmethod
from datetime import datetime
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Protocol,
)
from uuid import UUID

from core.models.user_token import (
    TokenType,
    UserToken,
)


class JWTServiceInterface(Protocol):
    """Интерфейс для работы с JWT токенами"""

    @abstractmethod
    def create_access_token(
        self,
        user_uuid: UUID,
        user_tole: str,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Создать Access JWT токен"""
        ...

    @abstractmethod
    def create_refresh_token(self) -> str:
        """Создать Refresh токен"""
        ...

    @abstractmethod
    def verify_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Проверить и декодировать Access токен"""
        ...

    @abstractmethod
    def get_user_from_token(self, token: str) -> Optional[UUID]:
        """Извлечь UUID пользователя из токена"""
        ...

    @abstractmethod
    def get_user_role_from_token(self, token: str) -> Optional[str]:
        """Извлечь роль пользователя из токена"""
        ...

    @abstractmethod
    def hash_refresh_token(self, refresh_token: str) -> str:
        """Захешировать refresh токен для безопасного хранения в БД"""
        ...

    @abstractmethod
    def create_token_pair(
        self,
        user_uuid: UUID,
        user_role: str,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Создать пару токенов (access + refresh)"""
        ...

    @abstractmethod
    def get_refresh_token_expires_at(self) -> datetime:
        """Получить дату истечения refresh токена"""
        ...

    @abstractmethod
    def create_verification_token(self, purpose: str = "email_verification") -> str:
        """Создать токен для верификации (email, password reset)"""
        ...

    @abstractmethod
    def is_token_expired(self, token: str) -> bool:
        """Проверить истек ли access токен"""
        ...


class TokenRepository(Protocol):
    """Интерфейс для работы с пользовательскими токенами в БД"""

    @abstractmethod
    async def create_token(
        self,
        user_uuid: UUID,
        token_hash: str,
        token_type: TokenType,
        expires_at: datetime,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> UserToken:
        """Создать новый токен"""
        ...

    @abstractmethod
    async def get_token_by_hash(
        self,
        token_hash: str,
        token_type: TokenType,
    ) -> Optional[UserToken]:
        """Найти токен по хэшу или типу"""
        ...

    @abstractmethod
    async def deactivate_token(self, token: UserToken) -> bool:
        """Деактивировать токен"""
        ...

    @abstractmethod
    async def deactivate_user_tokens(
        self, user_uuid: UUID, token_type: TokenType
    ) -> int:
        """Деактивировать все токены пользователя определенного типа"""
        ...

    @abstractmethod
    async def cleanup_expired_tokens(self) -> int:
        """Удалить все просроченные токены"""
        ...

    @abstractmethod
    async def get_user_active_tokens(
        self,
        user_uuid: UUID,
        token_type: Optional[TokenType] = None,
    ) -> List[UserToken]:
        """Получить активные токены пользователя"""
        ...

    @abstractmethod
    async def rotate_refresh_token(
        self,
        old_token_hash: str,
        new_token_hash: str,
        new_expires_at: datetime,
        user_uuid: UUID,
    ) -> Optional[UserToken]:
        """Заменить старый refresh токен на новый"""
        ...

    @abstractmethod
    async def revoke_all_user_sessions(self, user_uuid: UUID) -> int:
        """Отозвать все сессии пользователя"""
        ...

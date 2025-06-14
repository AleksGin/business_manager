from abc import abstractmethod
from datetime import date
from typing import List, Optional, Protocol
from uuid import UUID

from users.models.user import User


class UserRepository(Protocol):
    @abstractmethod
    async def create_user(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_uuid(self, user_uuid: UUID) -> Optional[User]: ...

    @abstractmethod
    async def get_by_email(self, user_email: str) -> Optional[User]: ...

    @abstractmethod
    async def update_user(self, uuid: User) -> User: ...

    @abstractmethod
    async def delete_user(self, uuid: UUID) -> bool: ...

    @abstractmethod
    async def list_user(
        self,
        limit: int = 50,
        offset: int = 0,
        team_uuid: Optional[UUID] = None,
    ) -> List[User]: ...

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool: ...


class PasswordHasher(Protocol):
    @abstractmethod
    async def hash_password(self, password: str) -> str: ...

    @abstractmethod
    async def verify_password_by_hash(
        self,
        password: str,
        hashed_password: str,
    ) -> bool: ...


class UserValidaor(Protocol):
    @abstractmethod
    async def validate_email_unique(
        self,
        email: str,
        exclude_uuid: Optional[UUID] = None,
    ): ...

    @abstractmethod
    def validate_age(self, birth_date: date) -> bool: ...

    @abstractmethod
    def validate_password_strength(self, password: str) -> bool: ...


class UUIDGenerator(Protocol):
    def __call__(self) -> UUID: ...


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...

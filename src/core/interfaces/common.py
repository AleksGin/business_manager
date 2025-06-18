from abc import abstractmethod
from typing import (
    List,
    Protocol,
)
from uuid import UUID

from users.models import (
    RoleEnum,
)


class RoleManager(Protocol):
    """Интерфейс для управления ролями пользователей"""

    @abstractmethod
    async def assign_role(
        self,
        user_uuid: UUID,
        role: RoleEnum,
        assigned_by: UUID,
    ) -> bool:
        """
        Назначить роль пользователю.

        Args:
            user_uuid: кому назначается роль
            role: назначаемая роль
            assigned_by: кто назначает роль
        """
        ...

    @abstractmethod
    async def remove_role(
        self,
        user_uuid: UUID,
        removed_by: UUID,
    ) -> bool:
        """
        Убрать специальную роль пользователя (сделать обычным EMPLOYEE).

        Args:
            user_uuid: у кого убирается роль
            removed_by: кто убирает роль
        """
        ...

    @abstractmethod
    async def get_role_hierarchy(self) -> dict[RoleEnum, List[RoleEnum]]:
        """
        Получить иерархию ролей системы.
        Возвращает словарь: какие роли может назначать каждая роль.
        """
        ...


class UUIDGenerator(Protocol):
    """Интерфейс для генерации уникальных идентификаторов"""

    def __call__(self) -> UUID:
        """Сгенерировать новый UUID"""
        ...


class DBSession(Protocol):
    """Интерфейс для управления транзакциями базы данных"""

    @abstractmethod
    async def commit(self) -> None:
        """Подтвердить все изменения в текущей транзакции"""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Отменить все изменения в текущей транзакции"""
        ...

    @abstractmethod
    async def flush(self) -> None:
        """Отправить изменения в БД без подтверждения транзакции"""
        ...

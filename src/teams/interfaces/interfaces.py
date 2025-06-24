from abc import abstractmethod
from typing import (
    Protocol,
)
from uuid import UUID


class TeamMembershipManager(Protocol):
    """Интерфейс для управления членством пользователей в командах"""

    @abstractmethod
    async def add_user_to_team(
        self,
        user_uuid: UUID,
        team_uuid: UUID,
        added_by: UUID,
    ) -> bool:
        """
        Добавить пользователя в команду.

        Args:
            user_uuid: кого добавляем
            team_uuid: в какую команду
            added_by: кто добавляет
        """
        ...

    @abstractmethod
    async def remove_user_from_team(
        self,
        user_uuid: UUID,
        team_uuid: UUID,
        removed_by: UUID,
    ) -> bool:
        """
        Удалить пользователя из команды.

        Args:
            user_uuid: кого удаляем
            team_uuid: из какой команды
            removed_by: кто удаляет
        """
        ...

    @abstractmethod
    async def transfer_team_ownership(
        self,
        team_uuid: UUID,
        new_owner_uuid: UUID,
        current_owner_uuid: UUID,
    ) -> bool:
        """
        Передать владение командой другому пользователю.

        Args:
            team_uuid: команда для передачи
            new_owner_uuid: новый владелец
            current_owner_uuid: текущий владелец (для проверки прав)
        """
        ...

    @abstractmethod
    async def generate_team_invite_code(
        self,
        team_uuid: UUID,
        created_by: UUID,
    ) -> str:
        """
        Создать код приглашения в команду.

        Returns:
            строка-код для присоединения к команде
        """
        ...

    @abstractmethod
    async def join_team_by_code(
        self,
        user_uuid: UUID,
        invite_code: str,
    ) -> bool:
        """
        Присоединиться к команде используя код приглашения.

        Args:
            user_uuid: кто присоединяется
            invite_code: код приглашения
        """
        ...

from abc import abstractmethod
from datetime import date
from typing import (
    List,
    Optional,
    Protocol,
)
from uuid import UUID

from users.models import (
    RoleEnum,
    User,
)


class UserRepository(Protocol):
    """Интерфейс для работы с пользователями в хранилище данных"""

    @abstractmethod
    async def create_user(self, user: User) -> User:
        """Создать нового пользователя в системе"""
        ...

    @abstractmethod
    async def get_by_uuid(self, user_uuid: UUID) -> Optional[User]:
        """Получить пользователя по UUID. Возвращает None если не найден"""
        ...

    @abstractmethod
    async def get_by_email(self, user_email: str) -> Optional[User]:
        """Получить пользователя по email. Возвращает None если не найден"""
        ...

    @abstractmethod
    async def update_user(self, user: User) -> User:
        """Обновить данные существующего пользователя"""
        ...

    @abstractmethod
    async def delete_user(self, user_uuid: UUID) -> bool:
        """Удалить пользователя. Возвращает True если удален успешно"""
        ...

    @abstractmethod
    async def list_users(
        self,
        limit: int = 50,
        offset: int = 0,
        team_uuid: Optional[UUID] = None,
    ) -> List[User]:
        """Получить список пользователей с пагинацией и фильтрацией по команде"""
        ...

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Проверить существование пользователя с указанным email"""
        ...

    @abstractmethod
    async def get_by_role(
        self,
        role: RoleEnum,
        team_uuid: Optional[UUID] = None,
    ) -> List[User]:
        """Получить пользователей по роли, опционально в конкретной команде"""
        ...

    @abstractmethod
    async def get_team_members(self, team_uuid: UUID) -> List[User]:
        """Получить всех участников указанной команды"""
        ...

    @abstractmethod
    async def get_users_without_team(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> List[User]:
        """Получить пользователей, не состоящих ни в одной команде"""
        ...

    @abstractmethod
    async def search_users(
        self,
        query: str,
        team_uuid: Optional[UUID] = None,
        exclude_team: bool = False,
        limit: int = 50,
    ) -> List[User]:
        """
        Поиск пользователей по имени, фамилии или email.

        Args:
            query: поисковая строка
            team_uuid: ограничить поиск определенной командой
            exclude_team: исключить пользователей из указанной команды
            limit: максимальное количество результатов
        """
        ...


class PasswordHasher(Protocol):
    """Интерфейс для работы с хешированием и проверкой паролей"""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Захешировать пароль для безопасного хранения"""
        ...

    @abstractmethod
    def verify_password_by_hash(
        self,
        password: str,
        hashed_password: str,
    ) -> bool:
        """Проверить соответствие пароля его хешу"""
        ...


class UserValidator(Protocol):
    """Интерфейс для бизнес-валидации пользователей"""

    @abstractmethod
    async def validate_email_unique(
        self,
        email: str,
        exclude_uuid: Optional[UUID] = None,
    ) -> bool:
        """
        Проверить уникальность email адреса.

        Args:
            email: проверяемый email
            exclude_uuid: исключить пользователя с этим UUID из проверки
                         (полезно при обновлении профиля)
        """
        ...

    @abstractmethod
    def validate_age(self, birth_date: date) -> bool:
        """Проверить соответствие возраста минимальным требованиям (например, 16+ лет)"""
        ...

    @abstractmethod
    def validate_password_strength(self, password: str) -> bool:
        """Проверить соответствие пароля требованиям безопасности"""
        ...


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
            assigned_by: кто назначает роль (для аудита)
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
            removed_by: кто убирает роль (для аудита)
        """
        ...

    @abstractmethod
    async def get_role_hierarchy(self) -> dict[RoleEnum, List[RoleEnum]]:
        """
        Получить иерархию ролей системы.
        Возвращает словарь: какие роли может назначать каждая роль.
        """
        ...


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
            added_by: кто добавляет (для аудита)
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
            removed_by: кто удаляет (для аудита)
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


class UserActivationManager(Protocol):
    """Интерфейс для управления активацией и верификацией пользователей"""

    @abstractmethod
    async def activate_user(
        self,
        user_uuid: UUID,
        activated_by: UUID,
    ) -> bool:
        """
        Активировать пользователя (разрешить доступ к системе).

        Args:
            user_uuid: кого активируем
            activated_by: кто активирует (для аудита)
        """
        ...

    @abstractmethod
    async def deactivate_user(
        self,
        user_uuid: UUID,
        deactivated_by: UUID,
    ) -> bool:
        """
        Деактивировать пользователя (заблокировать доступ).

        Args:
            user_uuid: кого деактивируем
            deactivated_by: кто деактивирует (для аудита)
        """
        ...

    @abstractmethod
    async def verify_user_email(
        self,
        user_uuid: UUID,
        verification_token: str,
    ) -> bool:
        """
        Подтвердить email пользователя с помощью токена верификации.

        Args:
            user_uuid: чей email подтверждается
            verification_token: токен из письма подтверждения
        """
        ...

    @abstractmethod
    async def generate_verification_token(self, user_uuid: UUID) -> str:
        """
        Создать токен для подтверждения email.

        Returns:
            токен для отправки в письме подтверждения
        """
        ...

    @abstractmethod
    async def reset_password_request(self, email: str) -> str:
        """
        Создать запрос на сброс пароля.

        Args:
            email: email пользователя, запросившего сброс

        Returns:
            токен для сброса пароля
        """
        ...

    @abstractmethod
    async def reset_password_confirm(
        self,
        token: str,
        new_password: str,
    ) -> bool:
        """
        Подтвердить сброс пароля и установить новый.

        Args:
            token: токен из письма сброса пароля
            new_password: новый пароль пользователя
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

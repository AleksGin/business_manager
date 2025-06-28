from abc import abstractmethod
from typing import (
    Protocol,
)
from uuid import UUID


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

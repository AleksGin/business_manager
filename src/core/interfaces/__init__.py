from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol
from uuid import UUID

if TYPE_CHECKING:
    from meetings.models import Meeting
    from tasks.models import Task
    from teams.models import Team
    from users.models import User


class PermissionValidator(Protocol):
    """Интерфейс для проверки прав доступа"""

    # ========== USER PERMISSIONS ==========

    @abstractmethod
    async def can_view_user(
        self,
        actor: "User",
        target_user: "User",
    ) -> bool:
        """Есть ли доступ у actor к просмотру пользователя"""
        ...

    @abstractmethod
    async def can_assign_user(
        self,
        actor: "User",
        target_user: "User",
        new_role: str,
    ) -> bool:
        """Есть ли права у actor менять/назачать роль пользователя"""
        ...

    @abstractmethod
    async def can_delete_user(
        self,
        actor: "User",
        target_user: "User",
    ) -> bool:
        """Есть ли возможность у actor удалять пользователя"""
        ...

    @abstractmethod
    async def can_update_user(
        self,
        actor: "User",
        target_user: "User",
    ) -> bool:
        """Есть ли возможность у actor обновлять информацию пользователя"""
        ...

    # ========== TEAM PERMISSIONS ==========

    @abstractmethod
    async def can_create_team(self, actor: "User") -> bool:
        """Есть ли возможность у actor создавать команду"""
        ...

    @abstractmethod
    async def can_view_team(
        self,
        actor: "User",
        team: "Team",
    ) -> bool:
        """Есть ли возможность у actor просматривать команду"""
        ...

    @abstractmethod
    async def can_update_team(
        self,
        actor: "User",
        team: "Team",
    ) -> bool:
        """Есть ли возможность у actor обновлять команду"""
        ...

    @abstractmethod
    async def can_delete_team(
        self,
        actor: "User",
        team: "Team",
    ) -> bool:
        """Есть ли возможность у actor удалять команду"""
        ...

    @abstractmethod
    async def can_add_team_member(
        self,
        actor: "User",
        team: "Team",
    ) -> bool:
        """Есть ли возможность у actor добавлять участников в команду"""
        ...

    @abstractmethod
    async def can_remove_team_member(
        self,
        actor: "User",
        team: "Team",
    ) -> bool:
        """Есть ли возможность у actor удалять участников из команды"""
        ...

    # ========== TASK PERMISSIONS ==========

    @abstractmethod
    async def can_create_task(
        self,
        actor: "User",
        team: "Team",
    ) -> bool:
        """Может ли actor создавать задачи в команде"""
        ...

    @abstractmethod
    async def can_view_task(
        self,
        actor: "User",
        task: "Task",
    ) -> bool:
        """Может ли actor просматривать задачи"""
        ...

    @abstractmethod
    async def can_delete_task(
        self,
        actor: "User",
        task: "Task",
    ) -> bool:
        """Может ли actor удалять задачу"""
        ...

    @abstractmethod
    async def can_assign_task(
        self,
        actor: "User",
        task: "Task",
        assignee: "User",
    ) -> bool:
        """Может ли actor обновлять информацию задачу"""
        ...

    @abstractmethod
    async def can_update_task(
        self,
        actor: "User",
        task: "Task",
    ) -> bool:
        """Может ли actor обновлять информацию задачу"""
        ...

    @abstractmethod
    async def can_change_task_status(
        self,
        actor: "User",
        task: "Task",
    ) -> bool:
        """Может ли actor менять статус задачи"""
        ...

    # ========== TASK PERMISSIONS ==========

    @abstractmethod
    async def can_create_meetings(
        self,
        actor: "User",
        team: "Team",
    ) -> bool:
        """Может ли actor созадвать встречи в команде"""
        ...

    @abstractmethod
    async def can_update_meeting(
        self,
        actor: "User",
        meeting: "Meeting",
    ) -> bool:
        """Может ли actor обновлять информацию встречи"""
        ...

    @abstractmethod
    async def can_delete_meeting(
        self,
        actor: "User",
        meeting: "Meeting",
    ) -> bool:
        """Может ли actor удалить встречу"""
        ...

    @abstractmethod
    async def can_add_meeting_participant(
        self,
        actor: "User",
        meeting: "Meeting",
    ) -> bool:
        """Может ли actor добавлять участников во встречу"""
        ...

    # ========== EVALUATION PERMISSIONS ==========

    @abstractmethod
    async def can_create_evaluation(
        self,
        actor: "User",
        task: "Task",
    ) -> bool:
        """Может ли actor создавать оценку для задачи"""
        ...

    @abstractmethod
    async def can_view_evaluation(
        self,
        actor: "User",
        task: "Task",
    ) -> bool:
        """Может ли actor просматривать оценку задачи"""
        ...

    @abstractmethod
    async def can_update_evaluation(
        self,
        actor: "User",
        task: "Task",
    ) -> bool:
        """Может ли actor обновлять оценку"""
        ...

    # ========== SYSTEM PERMISSIONS ==========

    @abstractmethod
    async def is_system_admin(self, actor: "User") -> bool:
        """Является ли actor системных администратором"""
        ...

    @abstractmethod
    async def is_team_admin(self, actor: "User", team: "Team") -> bool:
        """Является ли actor администратором команды"""
        ...

    @abstractmethod
    async def is_team_manager(self, actor: "User", team: "Team") -> bool:
        """Является ли actor менеджером команды"""
        ...

    @abstractmethod
    async def is_team_member(self, actor: "User", team: "Team") -> bool:
        """Является ли actor участником команды"""
        ...

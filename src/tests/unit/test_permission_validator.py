from unittest.mock import AsyncMock

import pytest

from core.interfaces import PermissionValidator
from core.providers import PermissionValidatorProvider
from teams.models import Team
from users.models import (
    RoleEnum,
    User,
)


@pytest.mark.unit
class TestPermissionValidator:
    """Unit тесты для PermissionValidator"""

    @pytest.fixture
    def permission_validator(self) -> PermissionValidator:
        return PermissionValidatorProvider()

    @pytest.fixture
    def admin_user(self) -> AsyncMock:
        """Мок админа"""
        user = AsyncMock(sepc=User)
        user.uuid = "admin-uuid"
        user.role = RoleEnum.ADMIN
        user.team_uuid = "team-1"
        return user

    @pytest.fixture
    def employee_user(self) -> AsyncMock:
        """Мок работника"""
        user = AsyncMock(sepc=User)
        user.uuid = "employee-uuid"
        user.role = RoleEnum.EMPLOYEE
        user.team_uuid = "team-1"
        return user

    @pytest.fixture
    def manager_user(self) -> AsyncMock:
        """Мок менеджера"""
        user = AsyncMock(sepc=User)
        user.uuid = "manager-uuid"
        user.role = RoleEnum.MANAGER
        user.team_uuid = "team-1"
        return user

    @pytest.fixture
    def test_team(self) -> AsyncMock:
        """Мок команды"""
        team = AsyncMock(spec=Team)
        team.uuid = "team-1"
        team.owner_uuid = "admin-uuid"
        return team

    @pytest.mark.asyncio
    async def test_can_view_user_admin_can_view_anyone(
        self,
        permission_validator: PermissionValidator,
        admin_user,
        employee_user,
        manager_user,
    ) -> None:
        """Тест: админ может просматривать любого пользователя"""

        admin_for_employee = await permission_validator.can_view_user(
            admin_user,
            employee_user,
        )
        admin_for_manager = await permission_validator.can_view_user(
            admin_user,
            manager_user,
        )

        assert admin_for_employee is True
        assert admin_for_manager is True

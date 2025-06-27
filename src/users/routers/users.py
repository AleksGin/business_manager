from typing import (
    Dict,
    List,
    Optional,
)
from uuid import UUID

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status,
)

from core.dependencies.depends import (
    CurrentUserDep,
    PasswordHasherDep,
    SessionDep,
    UserActivationDep,
    UserRepoDep,
    UserValidatorDep,
    UUIDGeneratorDep,
)
from users.models import RoleEnum
from users.interactors.user_interactos import (
    CreateUserDTO,
    CreateUserInteractor,
    DeleteUserInteractor,
    GetUserInteractor,
    GetUsersWithoutTeamInteractor,
    QueryUserInteractor,
    UpdateUserInteractor,
)
from users.schemas.user import (
    UserCreate,
    UserInTeam,
    UserResponse,
    UserUpdate,
)

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreate,
    current_user: CurrentUserDep,
    session: SessionDep,
    user_repo: UserRepoDep,
    password_hasher: PasswordHasherDep,
    user_validator: UserValidatorDep,
    uuid_generator: UUIDGeneratorDep,
    activation_manager: UserActivationDep,
) -> UserResponse:
    """Создание нового пользователя"""

    dto = CreateUserDTO(
        email=user_data.email,
        name=user_data.name,
        surname=user_data.surname,
        gender=user_data.gender,
        birth_date=user_data.birth_date,
        password=user_data.password,
    )

    create_user_interactor = CreateUserInteractor(
        user_repo=user_repo,
        password_hasher=password_hasher,
        user_validator=user_validator,
        permission_validator=None,
        uuid_generator=uuid_generator,
        db_session=session,
        activate_manager=activation_manager,
    )

    try:
        user = await create_user_interactor(
            actor_uuid=current_user.uuid,
            dto=dto,
        )
        return UserResponse.model_validate(user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=List[UserInTeam],
    status_code=status.HTTP_200_OK,
)
async def list_users(
    current_user: CurrentUserDep,
    user_repo: UserRepoDep,
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
    team_uuid: Optional[UUID] = Query(default=None),
) -> List[UserInTeam]:
    """Получить список пользователей"""

    get_list_users_interactor = QueryUserInteractor(
        user_repo=user_repo,
        permission_validator=None,
    )

    try:
        users = await get_list_users_interactor(
            actor_uuid=current_user.uuid,
            limit=limit,
            offset=offset,
            team_uuid=team_uuid,
        )
        return [UserInTeam.model_validate(user) for user in users]

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get(
    "/{user_uuid}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_uuid: UUID,
    current_user: CurrentUserDep,
    user_repo: UserRepoDep,
) -> UserResponse:
    """Получить пользователя по UUID"""

    get_user_interactor = GetUserInteractor(
        user_repo=user_repo,
        permission_validator=None,
    )

    try:
        user = await get_user_interactor.get_by_uuid(
            actor_uuid=current_user.uuid,
            target_uuid=user_uuid,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        return UserResponse.model_validate(user)

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.patch(
    "/{user_uuid}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_uuid: UUID,
    update_data: UserUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
    user_repo: UserRepoDep,
    user_validator: UserValidatorDep,
) -> UserResponse:
    """Обновить пользователя"""

    update_user_interactor = UpdateUserInteractor(
        user_repo=user_repo,
        user_validator=user_validator,
        permission_validator=None,
        db_session=session,
    )

    try:
        user = await update_user_interactor(
            actor_uuid=current_user.uuid,
            target_uuid=user_uuid,
            update_data=update_data,
        )

        return UserResponse.model_validate(user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.delete(
    "/{user_uuid}",
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_uuid: UUID,
    current_user: CurrentUserDep,
    session: SessionDep,
    user_repo: UserRepoDep,
) -> Dict[str, str]:
    """Удалить пользователя"""

    delete_user_interactor = DeleteUserInteractor(
        user_repo=user_repo,
        permission_validator=None,
        db_session=session,
    )

    try:
        result = await delete_user_interactor(
            actor_uuid=current_user.uuid,
            target_uuid=user_uuid,
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        return {"message": "Пользователь успешно удален"}

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get(
    "/search/",
    response_model=List[UserInTeam],
    status_code=status.HTTP_200_OK,
)
async def search_users(
    current_user: CurrentUserDep,
    user_repo: UserRepoDep,
    limit: int = Query(default=20, le=50),
    team_uuid: Optional[UUID] = Query(default=None),
    exclude_team: bool = Query(default=False),
    q: str = Query(min_length=2, description="Поисковый запрос"),
) -> List[UserInTeam]:
    """Поиск пользователей"""

    search_user_interactor = QueryUserInteractor(
        user_repo=user_repo,
        permission_validator=None,
    )

    users = await search_user_interactor(
        actor_uuid=current_user.uuid,
        limit=limit,
        team_uuid=team_uuid,
        search_query=q,
        exclude_team=exclude_team,
    )

    return [UserInTeam.model_validate(user) for user in users]


@router.get(
    "/without-team/",
    response_model=List[UserInTeam],
    status_code=status.HTTP_200_OK,
)
async def get_users_without_team(
    current_user: CurrentUserDep,
    user_repo: UserRepoDep,
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
) -> List[UserInTeam]:
    """Получить пользователей без команды (только для админов/менеджеров)"""

    # Создаем интерактора
    interactor = GetUsersWithoutTeamInteractor(
        user_repo=user_repo,
        permission_validator=None,
    )
    try:
        users = await interactor(
            actor_uuid=current_user.uuid,
            limit=limit,
            offset=offset,
        )

        return [UserInTeam.model_validate(user) for user in users]

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# TODO УДАЛИТЬ ЭТОТ ЭНДПОИНТ
@router.post("/make-first-admin")
async def make_admin(
    current_user: CurrentUserDep,
    session: SessionDep,
    user_repo: UserRepoDep,
):
    """Сделать первого админа"""

    current_user.role = RoleEnum.ADMIN
    await user_repo.update_user(current_user)
    await session.commit()

    return {"message": f"Вы теперь администратор {current_user.email}"}

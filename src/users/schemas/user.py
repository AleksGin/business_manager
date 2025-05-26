from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


class BaseFields:
    email = Field(description="Ваша электронная почта")
    password = Field(
        min_length=10, description="Пароль должен быть содержать минимум 10 символов"
    )


class BaseUser(BaseModel): ...


class CreateUser(BaseUser):
    name: str
    sur_name: str
    gender: str
    email: EmailStr = BaseFields.email
    password: str = BaseFields.password


class DeleteUser(BaseUser):
    user_work_id: int


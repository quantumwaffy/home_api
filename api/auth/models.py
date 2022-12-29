from core import base, mixins
from tortoise import fields


class Role(base.BaseModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)

    class PydanticMeta:
        exclude = ["id"]

    def __str__(self):
        return self.name


class User(base.BaseModel, mixins.TimeStamp):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    password_hash = fields.CharField(max_length=128)
    roles: fields.ManyToManyRelation["Role"] = fields.ManyToManyField(
        "models.Role", related_name="users", through="auth__user_role"
    )
    disabled = fields.BooleanField(default=False)

    def __str__(self) -> str:
        return f"#{self.id} ({self.full_name()})"

    def full_name(self) -> str:
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return self.username

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash", "created_at", "updated_at"]

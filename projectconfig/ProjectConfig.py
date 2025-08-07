import os, typing as t

import pydantic, yaml


class DatabaseConfig(pydantic.BaseModel):
    url: str


class EmailConfig(pydantic.BaseModel):
    user: str
    password: str

class ProjectConfig(pydantic.BaseModel):
    email: EmailConfig
    database: DatabaseConfig
    logging: dict

    is_dev_mode_on: bool = pydantic.Field(os.environ.get("DEV_MODE", "True") == "True")

    instance_: t.ClassVar[t.Optional["ProjectConfig"]] = None

    def __new__(cls, *args, **kwargs):
        if cls.instance_ is None:
            cls.instance_ = super().__new__(cls)

        return cls.instance_

    @classmethod
    def instance(cls) -> "ProjectConfig":
        if cls.instance_ is None:
            with open(os.environ["PROJECT_CONFIG_PATH"], "r") as f:
                data = yaml.safe_load(f)

            cls.instance_ = cls(**data)

        return cls.instance_

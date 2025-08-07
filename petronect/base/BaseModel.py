import pydantic


class BaseModel(pydantic.BaseModel):

    model_config = {
        "from_attributes": True
    }

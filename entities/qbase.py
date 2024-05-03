from pydantic import BaseModel


class QBaseModel(BaseModel):
    """
    QBaseModels are required to identity custom models.
    Custom models are used across applications. Custom models are identified via fining all subclasses.
    Use QBaseModel for all custom base classes.

    Apart from imports custom model definitions are being made available in a dictionary,
     see ALL_BASE_MODELS in __init__
    """

    pass

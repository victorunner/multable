import enum

import pydantic


class Language(enum.Enum):
    ARABIC = enum.auto()
    SLAVIC = enum.auto()


class Arguments(pydantic.BaseModel):
    max_number: int = pydantic.Field(10, description='max number', ge=0, le=10)
    show_arabic: bool = pydantic.Field(
        True, description='show arabic transcript for nonarabic numbers'
    )
    language: Language = pydantic.Field(Language.ARABIC, description='language')
    verbose: bool = pydantic.Field(False, description='verbose output')

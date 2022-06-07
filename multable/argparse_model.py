from enum import Enum
from pathlib import Path
from typing import Optional

import pydantic


class Language(str, Enum):
    ARABIC = 'ARABIC'
    SLAVIC = 'SLAVIC'


class Arguments(pydantic.BaseModel):
    max_number: int = pydantic.Field(10, description='max number', ge=0, le=10)
    show_arabic: bool = pydantic.Field(
        True, description='show arabic transcript for nonarabic numbers'
    )
    language: Language = pydantic.Field(
        Language.ARABIC, description='language'
    )
    verbose: bool = pydantic.Field(False, description='verbose output')
    output: Optional[Path] = pydantic.Field(
        description='output PDF file, ommiting means STDOUT'
    )

    class Config:
        use_enum_values = True

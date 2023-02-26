from pydantic import BaseModel
from typing import List, Dict


class OriginMapping(BaseModel):
    database: str
    name: str
    select: str


class DestinyMapping(BaseModel):
    database: str
    name: str
    table: str


class ExtractLoadMapping(BaseModel):
    origin: OriginMapping
    destiny: DestinyMapping
    row_count: int

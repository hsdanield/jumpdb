from typing import List, Dict

from pydantic import BaseModel


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


class ExtractSelectMapping(BaseModel):
    columns: List[str]
    data: List[Dict]
    row_count: int

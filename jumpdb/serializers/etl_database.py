from pydantic import BaseModel


class OriginMapping(BaseModel):
    database: str
    name: str
    select: str


class DestinyMapping(BaseModel):
    database: str
    name: str
    table: str


class ExtractLoadMappingIn(BaseModel):
    origin: OriginMapping
    destiny: DestinyMapping


class ExtractLoadMappingOut(BaseModel):
    origin: OriginMapping
    destiny: DestinyMapping
    row_count: int

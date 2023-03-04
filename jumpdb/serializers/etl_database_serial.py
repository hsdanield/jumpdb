from typing import List, Dict, Optional

from pydantic import BaseModel


class OriginMap(BaseModel):
    database: str
    name: str
    select: str


class DestinyMap(BaseModel):
    database: str
    name: str
    table: str


class ExtLoadInMap(BaseModel):
    origin: OriginMap
    destiny: DestinyMap


class ExtLoadOutMap(BaseModel):
    origin: OriginMap
    destiny: DestinyMap
    row_count: int


class ExtSltMap(BaseModel):
    columns: List[str]
    data: List[Dict]
    row_count: int


class FileMap(BaseModel):
    path_file: str
    format_file: str


class ExtSltMapSaveFileIn(BaseModel):
    origin: OriginMap
    file: FileMap


class ExtSltMapSaveFileOut(BaseModel):
    is_write: bool
    format_file: str

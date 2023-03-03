from pydantic import BaseModel
from typing import Optional, List, Dict


class InspectorIn(BaseModel):
    database: str
    name: str
    table_name: str


class ColumnsIn(BaseModel):
    database: str
    name: str
    table_name: str
    filter_columns: Optional[List[str]]


class ColumnsOut(BaseModel):
    name: str
    precision: str
    type: str
    nullable: bool
    default: str
    comment: str


class ConstraintOut(BaseModel):
    database: str
    name: str
    table_name: str
    constraint_name: Optional[str]
    constrained_columns: Optional[List[str]]


class FkConstraintOut(BaseModel):
    constraint_out: ConstraintOut
    referred_schema: Optional[str]
    referred_table: Optional[str]
    referred_columns: Optional[List[str]]
    options: Optional[Dict]


class IndexConstraintOut(BaseModel):
    constraint_out: ConstraintOut
    index_name: str
    dialect_options: Dict
    unique: bool


class SummaryTableOut(BaseModel):
    columns_out: List[ColumnsOut]
    constraint_out: ConstraintOut
    fk_out: List[FkConstraintOut]
    index_out: List[IndexConstraintOut]

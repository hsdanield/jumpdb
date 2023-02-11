from dataclasses import dataclass


def header_columns():
    return [
        "name",
        "precision",
        "type",
        "nullable",
        "default",
        "comment"
    ]


def header_pks():
    return [
        "name",
        "constrained_columns"
    ]


def header_fks():
    return [
        "name",
        "constrained_columns",
        "referred_schema",
        "referred_table",
        "referred_columns",
        "options"
    ]


def header_indexes():
    return [
        "name",
        "column_names",
        "dialect_options",
        "unique"
    ]

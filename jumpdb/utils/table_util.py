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


def header_constraints():
    return [
        "database",
        "name",
        "table_name",
        "constraint_name",
        "constrained_columns"
    ]


def header_indexes():
    return [
        "index_name",
        "dialect_options",
        "unique"
    ]


def header_fks():
    return [
        "referred_schema",
        "referred_table",
        "referred_columns",
        "options"
    ]

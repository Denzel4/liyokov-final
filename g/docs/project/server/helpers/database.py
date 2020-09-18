from sqlalchemy import (column, func, or_)
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.sqltypes import String, Enum

from project.server.helpers import array


def full_text_search(query, q, columns):
    if q is not None:
        return query.filter(or_(searchColumn.like('%{}%'.format(q)) for searchColumn in columns))
    return query


def get_list(query, pagination):
    pagination.total_count = query.count()
    if pagination.limit != 0:
        query = query.offset(pagination.offset).limit(pagination.limit)
    return query.all()


def get_order_by(model, columns):
    result = []
    for col in columns:
        direction = columns[col]
        path = array.split_or_none(col, '.')
        attr = getattr(model, path[0])
        if len(path) > 1:
            for p in path[1:]:
                attr = getattr(attr.property.argument(), p)
        if isinstance(attr.property, ColumnProperty):
            if isinstance(attr.property.columns[0].type, String) and not isinstance(attr.property.columns[0].type, Enum):
                attr = func.lower(attr)
            result.append(getattr(attr, direction)())
        elif isinstance(attr.property, RelationshipProperty) and attr.key in columns:
            result.append(getattr(func.coalesce(column(attr.key + '_count'), 0), direction)())
    return result

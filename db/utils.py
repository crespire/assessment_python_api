def to_camel_case(snake_str):
    components = snake_str.split("_")
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + "".join(x.title() for x in components[1:])


def row_to_dict(row):
    result = {}
    for column in row.__table__.columns:
        result[to_camel_case(column.name)] = getattr(row, column.name)

    return result


def rows_to_list(rows):
    results = []
    for row in rows:
        results.append(row_to_dict(row))
    return results

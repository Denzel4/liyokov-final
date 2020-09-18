def __filter_by_fields(data, fields):
    x = {}
    for datum in data:
        if isinstance(data[datum], (dict, list)) and datum in fields:
            new_fields = fields if isinstance(fields[datum], bool) and fields[datum] else fields[datum]
            if len(new_fields) == 0:
                x[datum] = data[datum]
            else:
                x[datum] = marshal(data[datum], new_fields)
        elif datum in fields:
            x[datum] = marshal(data[datum], fields[datum])
        elif fields == '*':
            x[datum] = marshal(data[datum], '*')
    return x


def __for_each_item(data, fields):
    x = []
    for datum in data:
        x.append(marshal(datum, fields))
    return x


def __merge_relationships(data, fields):
    if 'children' in data:
        for child in data['children']:
            __merge_relationships(child, fields)
    if 'relationships' in data:
        for datum in data['relationships']:
            obj = data['relationships'][datum]['object']
            if fields is None or (datum in fields and len(fields[datum]) == 0):
                if isinstance(obj, dict):
                    data[datum] = marshal(obj, dict())
                elif isinstance(obj, list):
                    obj_id = data['relationships'][datum]['id']
                    data[datum] = map(lambda y: y[obj_id], obj)
            elif datum in fields and len(fields[datum]) != 0:
                data[datum] = marshal(obj, fields[datum])
            else:
                data[datum] = marshal(obj, fields)
        del data['relationships']
    return data


def marshal(data, fields):
    if isinstance(data, dict):
        if len(fields) > 0:
            __merge_relationships(data, fields)
            return __filter_by_fields(data, fields)
        else:
            return __merge_relationships(data, None)
    elif isinstance(data, list):
        return __for_each_item(data, fields)
    return data

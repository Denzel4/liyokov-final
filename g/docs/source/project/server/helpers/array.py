def join_or_none(data, delimiter):
    if data is not None:
        return delimiter.join(data)
    return None


def split_or_none(data, delimiter):
    if data is not None:
        return data.split(delimiter)
    return None

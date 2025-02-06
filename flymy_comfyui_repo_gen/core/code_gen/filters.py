def j2_remove_prefix(value, prefix):
    if value.startswith(prefix):
        return value[len(prefix):]
    return value

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def copy_dict(some_dict):
    new_copy = dict()
    for k in some_dict.keys():
        new_copy[k] = some_dict[k]
    return new_copy
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
        if type(some_dict[k]) == dict:
            new_copy[k] = copy_dict(some_dict[k])
        elif type(some_dict[k]) == list:
            new_copy[k] = some_dict[k].copy()
        else:
            new_copy[k] = some_dict[k]
    return new_copy
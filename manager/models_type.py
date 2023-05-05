
def parse_type_to_db(_class_type):
    if _class_type is int:
        return 'int'
    elif _class_type is str:
        return 'varchar'
    else:
        assert False, f'type{_class_type} not supported'
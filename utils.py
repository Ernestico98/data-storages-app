import json
from prettytable import PrettyTable
from datetime import datetime

def desearialize_json_prettytable(data_str):
    data = json.loads(data_str)
    table = PrettyTable(data[0])
    for row in data[1:]:
        reordered_row = [ row[ variable ] for variable in data[0]] 
        table.add_row(reordered_row)
    return table

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()

def datetime_deserializer(obj):
    if 'datetime' in obj:
        return datetime.fromisoformat(obj['datetime'])
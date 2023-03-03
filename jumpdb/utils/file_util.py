from datetime import datetime
import json
import csv
from typing import List, Dict


class DateTimeJSONEncoderUtil(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def read_file(path_file: str):
    with open(path_file, "r") as file:
        content = file.read()
        file.close()

    return content


def write_json(path_file: str, dict_data: List[Dict]):
    try:
        json_data = json.dumps(dict_data, cls=DateTimeJSONEncoderUtil)
        with open(path_file, "w", newline="") as jsonfile:
            jsonfile.write(json_data)
            jsonfile.close()
            return True
    except Exception as e:
        print(f"Erro em write_json... Erro: {e}")
        return False


def write_csv(path_file: str, dict_data: Dict, columns: List):
    fieldnames = {a: b for a, b in zip(columns, columns)}
    try:
        with open(path_file, "w", newline="") as csvfile:
            write = csv.DictWriter(csvfile, fieldnames=fieldnames)
            write.writerow(fieldnames)
            write.writerows(dict_data)
            csvfile.close()
            return True
    except Exception as e:
        print(f"Erro em write_csv... Erro: {e}")
        return False

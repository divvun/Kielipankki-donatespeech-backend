import json
from pathlib import Path


def collect_values(
    obj,
    target_keys={"title", "body1", "body2"},
    result=None,
):
    if result is None:
        result = set()

    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in target_keys:
                result.add(v.values())
            collect_values(v, target_keys, result)
    elif isinstance(obj, list):
        for item in obj:
            collect_values(item, target_keys, result)
    return result


def read_json(input_json: Path):
    data = json.loads(input_json.read_text())
    return collect_values(
            data
        )

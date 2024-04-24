import json
from datetime import datetime

from typing import Any


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return _format_datetime(obj)
        else:
            return super().default(obj)


def _format_datetime(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

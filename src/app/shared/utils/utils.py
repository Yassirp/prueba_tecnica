import sys
from pprint import pprint
from typing import Any, Dict, List, Optional
from datetime import datetime


def dd(var: Any) -> None:
    pprint(var)
    sys.exit()


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()


def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    if dt_str is None:
        return None
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        return None


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]

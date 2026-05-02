import json
import logging
from datetime import datetime
from typing import Optional

import boto3

ssm = boto3.client("ssm")


def get_parameter_datetime(name: str) -> Optional[datetime]:
    try:
        response = ssm.get_parameter(Name=name)
        value = json.loads(response["Parameter"]["Value"])
        last_invoked = value.get("last_invoked")
        if last_invoked:
            return datetime.fromisoformat(last_invoked.replace("Z", "+00:00"))
        return None
    except Exception:
        logging.exception(f"Failed to read parameter {name} from SSM")
        return None


def put_parameter_datetime(name: str, dt: datetime) -> None:
    try:
        ssm.put_parameter(
            Name=name,
            Value=json.dumps({"last_invoked": dt.isoformat()}),
            Type="String",
            Overwrite=True,
        )
    except Exception:
        logging.exception(f"Failed to write parameter {name} to SSM")

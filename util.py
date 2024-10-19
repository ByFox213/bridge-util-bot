import logging
from typing import TypeVar

import nats
import yaml
from nats.aio.client import Client
from nats.js import JetStreamContext

DataClassT = TypeVar("DataClassT", bound="BaseModel")
_log = logging.getLogger(__name__)


__all__ = (
    "load_yaml",
    "nats_connect"
)


def load_yaml(filename: str, modal: DataClassT) -> DataClassT:
    with open(filename, encoding="utf-8") as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)
    _yaml = modal(**data) if data is not None else None
    if _yaml is not None:
        return _yaml


async def nats_connect(env: DataClassT) -> tuple[Client, JetStreamContext]:
    nc = await nats.connect(
        servers=env.nats_server,
        user=env.nats_user,
        password=env.nats_password
    )
    js = nc.jetstream()
    _log.info("nats connected")
    return nc, js

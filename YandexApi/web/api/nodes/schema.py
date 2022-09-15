from typing import List, Union

from pydantic import BaseModel


class NodeSchema(BaseModel):
    id: str
    type: str
    children: List["NodeSchema"]
    size: Union[int, None]
    url: Union[str, None]

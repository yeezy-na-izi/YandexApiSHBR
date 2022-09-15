from typing import List, Union

from pydantic import BaseModel


class NodeSchema(BaseModel):
    id: str
    type: str
    parentId: Union[str, None]
    size: Union[int, None]
    url: Union[str, None]


class ImportNodeSchema(BaseModel):
    items: List[NodeSchema]
    updateDate: str

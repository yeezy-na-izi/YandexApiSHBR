from fastapi import APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

from YandexApi.db.models import Node

router = APIRouter()


@router.get("/nodes/{node_id}", status_code=200)
async def get_node(node_id: str) -> dict:
    """Get info about node by id"""
    output = await get_output(node_id)
    return output[0]


async def get_output(node_id: str):
    try:
        node = await Node.get(id=node_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")

    size = node.size if node.type == "FILE" else 0
    children_list = []
    if node.type == "FOLDER":
        children = await Node.filter(parent_id=node_id)

        if children:
            for child in children:
                child_out, child_size = await get_output(child.id)
                children_list.append(child_out)
                size += child_size

    output = {
        "id": node.id,
        "url": node.url,
        "type": node.type,
        "parentId": node.parent_id if node.parent else None,
        "date": str(node.date).replace("+00:00", "Z").replace(" ", "T"),
        "size": size,
        "children": children_list if children_list else None,
    }

    return output, size

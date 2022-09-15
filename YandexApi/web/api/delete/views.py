# delete node by id

from fastapi import APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

from YandexApi.db.models import Node

router = APIRouter()


@router.delete("/delete/{node_id}", status_code=200)
async def delete_node(node_id: str) -> dict:
    """Delete node by id"""

    try:
        node = await Node.get(id=node_id)
        if node.type == "FOLDER":
            children = await Node.filter(parent_id=node_id)
            if children:
                for child in children:
                    await delete_node(child.id)
        await node.delete()
        return {
            "code": 200,
        }
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")

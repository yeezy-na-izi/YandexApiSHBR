from fastapi import APIRouter

from YandexApi.db.models import Node

router = APIRouter()


# get info about node by id
@router.get("/nodes/{node_id}", status_code=200)
async def get_node(node_id: str) -> dict:
    output = await get_output(node_id)
    return output[0]


async def get_output(node_id: str):
    node = await Node.get(id=node_id)
    if node.type == "FOLDER":
        children = await Node.filter(parent_id=node_id)
        size = 0
        children_list = []
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
    else:
        output = {
            "id": node.id,
            "url": node.url,
            "type": node.type,
            "parentId": node.parent_id if node.parent else None,
            "date": str(node.date).replace("+00:00", "Z").replace(" ", "T"),
            "size": node.size,
            "children": None,
        }
        size = node.size
    return output, size

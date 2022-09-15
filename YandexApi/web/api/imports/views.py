from datetime import datetime

from fastapi import APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

from YandexApi.db.models import Node, NodeHistory
from YandexApi.web.api.imports.schema import ImportNodeSchema

router = APIRouter()


@router.post("/imports")
async def imports_nodes(import_value: ImportNodeSchema):
    """Import nodes"""
    # check date format
    try:
        datetime.fromisoformat(import_value.updateDate[:-1])
    except ValueError:
        raise HTTPException(status_code=400, detail="Validation Failed")

    parents_for_update = set()
    import_value.items.sort(key=lambda x: x.type, reverse=True)

    try:
        for item in import_value.items:

            # check parent or set None
            if item.parentId:
                parent = await Node.get(id=item.parentId)
                if parent.type == "FILE":
                    raise HTTPException(status_code=400, detail="Validation Failed")
                parents_for_update.add(item.parentId)
            else:
                parent = None

            # create or update node
            try:
                folder_id = await update_node(item, import_value.updateDate, parent)
            except DoesNotExist:
                folder_id = await create_node(item, import_value.updateDate, parent)
            except Exception as e:
                raise HTTPException(status_code=400, detail="Validation Failed")

            if folder_id:
                parents_for_update.add(folder_id)

        # update date for parents and create history
        for parent_id in parents_for_update:
            await update_date_for_folders(parent_id, import_value.updateDate)

    except Exception:
        raise HTTPException(status_code=400, detail="Validation Failed")


async def update_node(item, date, parent):
    node = await Node.get(id=item.id)
    if node.type != item.type:
        raise HTTPException(status_code=400, detail="Validation Failed")

    if item.type == "FILE":
        if item.size < 1:
            raise HTTPException(status_code=400, detail="Validation Failed")

    await node.update_from_dict(
        {
            "type": item.type,
            "parent": parent,
            "size": item.size if item.type == "FILE" else None,
            "url": item.url if item.type == "FILE" else None,
            "date": date,
        },
    )
    await node.save()
    if node.type == "FILE":
        size = item.size
        await NodeHistory.create(
            node=node,
            type=node.type,
            parent=node.parent,
            size=size,
            url=node.url,
            date=node.date,
        )
        return None
    else:
        return node.id


async def create_node(item, date, parent):
    if item.type == "FOLDER":
        node = await Node.create(
            id=item.id,
            type=item.type,
            parent=parent,
            date=date,
        )
    else:
        if item.size < 1:
            raise HTTPException(status_code=400, detail="Validation Failed")

        node = await Node.create(
            id=item.id,
            type=item.type,
            parent=parent,
            size=item.size,
            url=item.url,
            date=date,
        )

    if node.type == "FILE":
        size = item.size
        await NodeHistory.create(
            node=node,
            type=node.type,
            parent=node.parent,
            size=size,
            url=node.url,
            date=node.date,
        )
        return None
    else:
        return node.id


async def update_date_for_folders(node_id: str, date):
    node = await Node.get(id=node_id)
    await node.update_from_dict(
        {
            "date": date,
        },
    )
    await node.save(update_fields=["date"])

    try:
        await NodeHistory.get(node_id=node.id, date=node.date)
    except DoesNotExist:
        await NodeHistory.create(
            node=node,
            type=node.type,
            parent=await Node.get(id=node.parent_id) if node.parent_id else None,
            size=await get_size_for_folder(node.id),
            url=node.url,
            date=node.date,
        )

    if node.parent:
        await update_date_for_folders(node.parent_id, date)


async def get_size_for_folder(node_id: str):
    size = 0
    for node in await Node.filter(parent_id=node_id):
        if node.type == "FILE":
            size += node.size
        else:
            size += await get_size_for_folder(node.id)
    return size

from fastapi import APIRouter
from tortoise.exceptions import DoesNotExist

from YandexApi.db.models import Node
from YandexApi.web.api.imports.schema import ImportNodeSchema

router = APIRouter()


@router.post("/imports", status_code=200)
async def imports_nodes(
    import_value: ImportNodeSchema,
) -> dict:
    """
    {
        "items": [
            {
                "type": "FOLDER",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "FILE",
                "url": "/file/url3",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 512
            },
            {
                "type": "FILE",
                "url": "/file/url4",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "size": 1024
            }
        ],
        "updateDate": "2022-02-03T12:00:00Z"
    }
    """
    parents_for_update = set()
    try:
        for item in import_value.items:
            if item.parentId:
                parent = await Node.get(id=item.parentId)
                if parent.type == "FILE":
                    return {
                        "code": 400,
                        "message": "Validation Failed",
                    }
                parents_for_update.add(item.parentId)
            else:
                parent = None

            try:
                node = await Node.get(id=item.id)
                if node.type != item.type:
                    return {
                        "code": 400,
                        "message": "Validation Failed",
                    }

                if item.type == "FILE":
                    if item.size < 1:
                        return {
                            "code": 400,
                            "message": "Validation Failed",
                        }

                node.parent = parent
                node.date = import_value.updateDate
                await node.update_from_dict(
                    {
                        "type": item.type,
                        "parent": parent,
                        "size": item.size if item.type == "FILE" else None,
                        "url": item.url if item.type == "FILE" else None,
                        "date": import_value.updateDate,
                    },
                )
            except DoesNotExist:
                if item.type == "FOLDER":
                    await Node.create(
                        id=item.id,
                        type=item.type,
                        parent=parent,
                        date=import_value.updateDate,
                    )
                else:
                    if item.size < 1:
                        return {
                            "code": 400,
                            "message": "Validation Failed",
                        }
                    await Node.create(
                        id=item.id,
                        type=item.type,
                        parent=parent,
                        size=item.size,
                        url=item.url,
                        date=import_value.updateDate,
                    )

            except Exception as e:

                print("Что за херь?", e)

        for parent_id in parents_for_update:
            await update_date_for_folders(parent_id, import_value.updateDate)
        print()
        return {
            "code": 200,
        }
    except Exception:
        return {
            "code": 400,
            "message": "Validation Failed",
        }


async def update_date_for_folders(node_id: str, date):
    node = await Node.get(id=node_id)
    await node.update_from_dict(
        {
            "date": date,
        },
    )
    await node.save(update_fields=["date"])

    if node.parent:
        await update_date_for_folders(node.parent_id, date)

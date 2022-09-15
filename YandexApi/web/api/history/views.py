from datetime import datetime

from fastapi import APIRouter, HTTPException

from YandexApi.db.models import NodeHistory

router = APIRouter()


# get node history by date from date to date
@router.get("/node/{node_id}/history", status_code=200)
async def get_node_history(
    node_id: str, dateStart: str = None, dateEnd: str = None
) -> list:
    """Get node history"""
    output = await get_output(node_id, dateStart, dateEnd)
    return output


async def get_output(node_id, from_date, to_date):
    # date to datetime

    try:
        if from_date:
            from_date = datetime.fromisoformat(from_date[:-1])
        if to_date:
            to_date = datetime.fromisoformat(to_date[:-1])
    except ValueError:
        raise HTTPException(status_code=400, detail="Validation Failed")

    output = []
    nodes_history = await NodeHistory.filter(
        node_id=node_id,
        date__gte=from_date if from_date else None,
        date__lte=to_date if to_date else None,
    )
    for node in nodes_history:
        output.append(
            {
                "id": node.node_id,
                "url": node.url,
                "parentId": node.parent_id if node.parent else None,
                "type": node.type,
                "size": node.size,
                "date": str(node.date).replace("+00:00", "Z").replace(" ", "T"),
            }
        )

    return output

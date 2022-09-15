from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

from YandexApi.db.models import Node
import pytz

router = APIRouter()


# get files witch updated for 24 hours
@router.get("/updates", status_code=200)
async def get_updated_files(date: str) -> list:
    """Get info about updated files"""
    output = await get_output(date[:-1])
    return output


async def get_output(date):
    # date to datetime
    try:
        date = pytz.utc.localize(datetime.fromisoformat(date))
    except ValueError:
        raise HTTPException(status_code=400, detail="Validation Failed")

    output = []
    try:
        nodes = await Node.filter(type="FILE")
        left_date = date - timedelta(days=1)
        for node in nodes:
            if left_date <= node.date <= date:
                output.append(
                    {
                        "id": node.id,
                        "url": node.url,
                        "parentId": node.parent_id if node.parent else None,
                        "type": node.type,
                        "size": node.size,
                        "date": str(node.date).replace("+00:00", "Z").replace(" ", "T"),
                    }
                )

    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")

    return output

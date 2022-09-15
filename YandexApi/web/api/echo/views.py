from fastapi import APIRouter

from YandexApi.web.api.echo.schema import Message

router = APIRouter()


@router.get("/")
async def send_echo_message():
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """
    return {"message": 'Hello World'}

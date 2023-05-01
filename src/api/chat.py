from fastapi import APIRouter, Request, WebSocket

router = APIRouter()

@router.get('/current-user')
def get_user(request: Request):
    return request.cookies.get('X-Authorization')


@router.websocket('/ws')
async def chat_ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    # TODO: Complete
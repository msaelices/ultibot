from fastapi import APIRouter, Request

router = APIRouter()

@router.get('/current-user')
def get_user(request: Request):
    return request.cookies.get('X-Authorization')
from ninja import Router

router = Router(tags=["Auth"])


@router.get("")
def auth_root(request):
    return {"message": "auth ok"}

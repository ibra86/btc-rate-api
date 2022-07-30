from http.client import HTTPException


class SubscribedAgainException(HTTPException):
    code = 409
    description = (
        "email is already subscribed"
    )

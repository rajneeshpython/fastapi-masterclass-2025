from jose import jwt
from starlette import status
from fastapi import HTTPException
import pytest

from .utils import *
from ..routers.auth import get_db, authenticate_user,get_current_user ,create_access_token, SECRET_KEY, ALGORITHM
from datetime import timedelta


app.dependency_overrides[get_db] = override_get_db


def test_authenticated_user(test_user):
    db = TestSessionLocal()
    authenticated_test_user = authenticate_user(test_user.username, "test", db)
    assert authenticated_test_user is not None
    assert authenticated_test_user.username == test_user.username

    non_existing_test_user = authenticate_user("wronguser", "example", db)
    assert non_existing_test_user is False

    wrong_password_test_user = authenticate_user("test", "wrongpassord", db)
    assert wrong_password_test_user is False


def test_create_access_token():
    username = "test_user"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)

    access_token = create_access_token(username,user_id, role, expires_delta)

    decoded_token = jwt.decode(access_token, SECRET_KEY,
                               algorithms=[ALGORITHM],
                               options={"verify_signature": False})

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub":"test", "id":1, "role":"admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {"username": "test", "id": 1, "user_role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exif:
        await get_current_user(token=token)

    assert exif.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exif.value.detail == "Could not validate user."


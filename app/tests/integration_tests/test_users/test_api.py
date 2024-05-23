import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('email, password, status_code', [
        ('L6vXJ@example.com', 'password', 200),
        ('L6vXJ@example.com', 'wrong_password', 409),
        ('L6vXJexamplecom', 'wrong_password', 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        '/auth/register', json={
            'email': email,
            'password': password
        })

    assert response.status_code == status_code


@pytest.mark.parametrize('email, password, status_code', [
    ('test@test.com', 'test', 200),
    ('test@test.com', 'wrong_password', 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        '/auth/login', json={
            'email': email,
            'password': password
        })

    assert response.status_code == status_code

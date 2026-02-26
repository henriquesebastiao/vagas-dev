from fastapi import status


async def test_health_return_200(client):
    response = await client.get('/health')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == 'ok'

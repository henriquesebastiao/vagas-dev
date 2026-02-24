from fastapi import status


async def test_list_jobs(client):
    response = await client.get('/jobs/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


async def test_list_sources(client):
    response = await client.get('/jobs/sources')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


async def test_trigger_sync(client):
    response = await client.post('/jobs/sync/gupy')
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert 'iniciado em background' in response.json().get('message', '')


async def test_trigger_sync_not_found(client):
    response = await client.post('/jobs/sync/unknown_source')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.json().get('detail')
        == "Source 'unknown_source' não suportado."
    )

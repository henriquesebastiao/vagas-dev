from fastapi import status


async def test_list_jobs(client):
    response = await client.get('/jobs/')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


async def test_list_jobs_with_source_return_200(client):
    response = await client.get('/jobs/?source=gupy')
    assert response.status_code == status.HTTP_200_OK


async def test_list_jobs_with_keyword_return_200(client):
    response = await client.get('/jobs/?keyword=python')
    assert response.status_code == status.HTTP_200_OK


async def test_list_jobs_with_location_return_200(client):
    response = await client.get('/jobs/?location=Brasil')
    assert response.status_code == status.HTTP_200_OK


async def test_list_jobs_with_workplace_type_return_200(client):
    response = await client.get('/jobs/?workplace_type=remote')
    assert response.status_code == status.HTTP_200_OK


async def test_list_jobs_with_for_pcd_return_200(client):
    response = await client.get('/jobs/?for_pcd=true')
    assert response.status_code == status.HTTP_200_OK


async def test_list_jobs_with_level_return_200(client):
    response = await client.get('/jobs/?level=senior')
    assert response.status_code == status.HTTP_200_OK


async def test_list_jobs_with_level_does_not_return_other_levels(client):
    response = await client.get('/jobs/?level=senior')
    assert response.status_code == status.HTTP_200_OK
    jobs = response.json()
    for job in jobs:
        assert job['level'] == 'senior'


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

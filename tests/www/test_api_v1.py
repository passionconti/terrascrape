def test_api_health(test_client):
    response = test_client.get('/v1/health')
    assert response.status_code == 200
    assert response.json['status'] == 'OK'

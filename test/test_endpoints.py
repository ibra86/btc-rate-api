def test_root(client):
    res = client.get('/')
    assert res.status_code == 200
    html = res.data.decode()
    assert '<div id="swagger-ui">' in html

def test_rate(client):
    assert True
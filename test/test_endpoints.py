from unittest.mock import PropertyMock


def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    html = res.data.decode()
    assert '<div id="swagger-ui">' in html


def test_get_rate(client, mocker):
    mock_msg_api = mocker.patch('app.api.get_msg', autospec=True)
    mock_msg_api.return_value = {'test_msg': True}

    res = client.get('/api/rate')

    mock_msg_api.assert_called_once()
    assert res.status_code == 200
    assert 'test_msg' in res.text


def test_subscribe_success(client, mocker):
    mocker.patch('app.email_registry', autospec=True)

    form_data = {'email': 'test_email@test.com'}
    res = client.post('/api/subscribe', data=form_data)

    assert res.status_code == 200
    assert 'test_email@test.com' in res.text


def test_subscribe_conflict(client, mocker):
    mock_email_registry = mocker.patch('app.email_registry', autospec=True)
    type(mock_email_registry).emails = PropertyMock(return_value=['test_email@test.com'])

    form_data = {'email': 'test_email@test.com'}
    res = client.post('/api/subscribe', data=form_data)

    assert res.status_code == 409
    assert 'test_email@test.com' in res.text


def test_send_emails(client, mocker):
    mock_msg_api = mocker.patch('app.api.get_msg', autospec=True)
    mock_msg_api.return_value = {'test_msg': True}

    mock_mail_send = mocker.patch('app.mail.send', autospec=True)
    res = client.post('/api/sendEmails')

    mock_mail_send.assert_called_once()
    assert res.status_code == 200

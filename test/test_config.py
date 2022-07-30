from src.config.config import CONFIG


def test_config():
    assert 'url' in CONFIG.get_config('api')
    assert 'api_key' in CONFIG.get_config('api')
    assert 'default_currency_from' in CONFIG.get_config('api')
    assert 'default_currency_from' in CONFIG.get_config('api')
    assert 'user' in CONFIG.get_config('email')
    assert 'pass' in CONFIG.get_config('email')
    assert 'csv' in CONFIG.get_config('db')

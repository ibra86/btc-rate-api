import os

import pytest

from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

    # clean up
    from src.config.config import CONFIG
    db_file = CONFIG.get_config('db').get('csv').get('dir_path')
    if os.path.exists(db_file):
        import shutil
        shutil.rmtree(db_file)

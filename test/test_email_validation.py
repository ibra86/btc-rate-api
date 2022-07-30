import pytest

from src.helpers import email_validation

test_valid_email = ['vvv@gmail.com',
                    'anonymous123@ukr.net',
                    'myemail@outlook.sdf']
test_invalid_email = ['vvv@gmail',
                      'anonymous123@..urk.net',
                      'myemail@outlook.']


@pytest.mark.parametrize('email', test_valid_email)
def test_email_valid(email):
    assert email_validation(email)


@pytest.mark.parametrize('email', test_invalid_email)
def test_email_invalid(email):
    assert not email_validation(email)

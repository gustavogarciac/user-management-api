import pytest

from src.adapters.auth.pwdlib_password_hasher import PwdlibPasswordHasher


@pytest.fixture
def hasher():
    return PwdlibPasswordHasher()


def test_pwdlib_password_hasher_hash_password(hasher):
    password = 'test_password'
    hashed_password = hasher.hash_password(password)

    assert hashed_password is not None
    assert hashed_password != password


def test_pwdlib_password_hasher_verify_password_success(hasher):
    password = 'test_password'
    hashed_password = hasher.hash_password(password)

    assert hasher.verify_password(password, hashed_password)

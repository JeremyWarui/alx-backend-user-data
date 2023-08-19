#!/usr/bin/env python3
"""
Integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    """ add a new user """
    req = requests.post("http://localhost:5000/users", data={
        "email": email,
        "password": password
    })
    assert req.status_code == 200, "Test fail"
    assert req.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ login test for wrong password """
    req = requests.post("http://localhost:5000/sessions", data={
        "email": email,
        "password": password
    })
    assert req.status_code == 401, "Test fail"


def log_in(email: str, password: str) -> str:
    """ login test with right password """
    req = requests.post("http://localhost:5000/sessions", data={
        "email": email,
        "password": password
    })
    assert req.status_code == 200, "Test fail"
    assert req.json() == {"email": email, "message": "logged in"}
    return req.cookies.get("session_id")


def profile_unlogged() -> None:
    """ tests unlogged in profile """
    res = requests.get("http://localhost:5000/profile")
    assert res.status_code == 403, "Test fail"


def profile_logged(session_id: str) -> None:
    """ check if profile is logged in """
    res = requests.get("http://localhost:5000/profile", cookies={
        "session_id": session_id
    })
    assert res.status_code == 200, "Test failed"
    assert res.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """ test id loggout function is good """
    res = requests.delete("http://localhost:5000/sessions", cookies={
        "session_id": session_id
    })
    assert res.status_code == 200, "Test fail"


def reset_password_token(email: str) -> str:
    """ test a reset password token function """
    res = requests.post("http://localhost:5000/reset_password", data={
        "email": email
    })
    assert res.status_code == 200, "Test fail"
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test update password function"""
    res = requests.put("http://localhost:5000/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert res.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

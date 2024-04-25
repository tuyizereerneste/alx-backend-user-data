#!/usr/bin/env python3
"""
Main file
"""

import requests


def register_user(email: str, password: str) -> None:
    """
    Method that test for user registration
    Parameters:
        email(str): email of the user.
        password(str): password of the user.
    Returns:
        None
    """
    req = requests.post('http://127.0.0.1:5000/users',
                         data={'email': email, 'password': password})
    if req.status_code == 200:
        assert (req.json() == {"email": email, "message": "user created"})
    else:
        assert(req.status_code == 400)
        assert (req.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Method that test for user log in.
    Parameters:
        email(str): email of the user.
        password(str): password of the user.
    Returns:
        None
    """
    r = requests.post('http://127.0.0.1:5000/sessions',
                      data={'email': email, 'password': password})
    assert (r.status_code == 401)


def profile_unlogged() -> None:
    """
    Methos that test for profile without being logged in.
    Returns:
        None
    """
    p = requests.get('http://127.0.0.1:5000/profile')
    assert(p.status_code == 403)


def log_in(email: str, password: str) -> str:
    """
    Method that test log in with the given correct email and password.
    Parameters:
        email(str): The email of the user.
        password(str): The password of the user.
    Returns:
        The session_id of the user.
    """
    req = requests.post('http://127.0.0.1:5000/sessions',
                         data={'email': email, 'password': password})
    assert (req.status_code == 200)
    assert(req.json() == {"email": email, "message": "logged in"})
    return req.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """
    Method that test for profile of a user logged in with session_id.
    Parameter:
        session_id: session_id of the user.
    Returns:
        None
    """
    cookies = {'session_id': session_id}
    r = requests.get('http://127.0.0.1:5000/profile',
                     cookies=cookies)
    assert(r.status_code == 200)


def log_out(session_id: str) -> None:
    """
    Method that test for log out with the given session_id.
    Parameter:
        session_id: session_id of the user.
    Returns:
        None
    """
    cookies = {'session_id': session_id}
    r = requests.delete('http://127.0.0.1:5000/sessions',
                        cookies=cookies)
    if r.status_code == 302:
        assert(r.url == 'http://127.0.0.1:5000/')
    else:
        assert(r.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    Method that test for reset password token with the given email.
    Parameter:
        email(str): The email of the user.
    Returns:
        reset_token of the user.
    """
    r = requests.post('http://127.0.0.1:5000/reset_password',
                      data={'email': email})
    if r.status_code == 200:
        return r.json()['reset_token']
    assert(r.status_code == 401)

def update_password(email: str,
                    reset_token: str,
                    new_password: str) -> None:
    """ Method that Test for update password with the given email
    Parameters:
        email: email of the user
        reset_token: reset_token of the user
        new_password: new password of the user
    Return:
        None
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    req = requests.put('http://127.0.0.1:5000/reset_password',
                     data=data)
    if req.status_code == 200:
        assert(req.json() == {"email": email, "message": "Password updated"})
    else:
        assert(req.status_code == 403)


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

import re

import requests


# Invalid auth exception
class InvalidAuth(Exception):
    pass


class LoginCreds:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


# Auth information
class Student:
    """Student Information"""

    _first_name: str = ""
    _has_school_today: bool = False
    _last_login_time: str = ""
    _student_number: int = 0
    _session = None

    def getFirstName(self) -> str:
        """Gets the student's first name

        Returns:
            str: First name
        """
        return self._first_name

    def hasSchoolToday(self) -> bool:
        """Get if the student has school today

        Returns:
            bool: has school today?
        """
        return self._has_school_today

    def getLastLoginTime(self) -> str:
        """Get the student's last login time

        Returns:
            str: Last login time
        """
        return self._last_login_time

    def getStudentNumber(self) -> int:
        """Get the student's student number

        Returns:
            int: Student number
        """
        return self._student_number

    def __str__(self):
        return str(
            {
                "first_name": self.getFirstName(),
                "has_school_today": self.hasSchoolToday(),
                "last_login_time": self.getLastLoginTime(),
                "student_number": self.getStudentNumber(),
            }
        )


def _webpageToAuthInfo(data: str) -> Student:
    # Output
    out = Student()

    # Pase Login info
    lgnInfo = re.findall(
        r"Good Morning, (.*)\.&nbsp;&nbsp;Today is .*, (.*).<br>\(Last Login Time (.*)\)",
        data,
        re.M,
    )
    if len(lgnInfo) == 1:
        out._first_name = lgnInfo[0][0]
        out._has_school_today = lgnInfo[0][1] != "a day off of school"
        out._last_login_time = lgnInfo[0][2]

    # Parse student auth info
    authInfo = re.findall(r"student_no=(.*)&code=(.*)&k=(.*)", data, re.M)
    if len(authInfo) == 1:
        out._student_number = int(authInfo[0][0])

    return out


# Login
def getStudent(creds: LoginCreds) -> Student:
    session = requests.Session()

    # Make primary request to read auth secrets embedded in the response
    data = session.get("https://schoolapps2.tvdsb.ca/students/student_login/lgn.aspx")

    # Read all secrets
    secrets = re.findall(
        r'input type="hidden" name="(.*)" id=".*" value="(.*)"', data.text, re.M
    )

    # Build HTTP request
    request_body = {
        "txtUserID": creds.username,
        "txtPwd": creds.password,
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "btnSubmit": "Login",
    }

    # Add all secrets
    for secret in secrets:
        request_body[secret[0]] = secret[1]

    # Make request to schoolapps2 server
    data = session.post(
        "https://schoolapps2.tvdsb.ca/students/student_login/lgn.aspx",
        data=request_body,
    )

    # Handle invalid auth
    # We just search for a word that only exists in the authenticated parts of the site
    if "Google" not in data.text:
        raise InvalidAuth("Login invalid")

    # Get student info
    studentInfo = _webpageToAuthInfo(data.text)

    # Get session data
    studentInfo._session = session

    # Return auth info
    return studentInfo

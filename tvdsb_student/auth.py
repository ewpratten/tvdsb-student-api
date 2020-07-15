import requests
import re

# Invalid auth exception
class InvalidAuth(Exception):
    pass

# Auth information
class AuthInfo:
    first_name: str
    has_school_today: bool
    last_login_time: str
    student_number: int
    session: dict

    def __str__(self):
        return str({
            "first_name": self.first_name,
            "has_school_today": self.has_school_today,
            "last_login_time": self.last_login_time,
            "student_number": self.student_number,
            "session": self.session
        })

def _webpageToAuthInfo(data: str) -> AuthInfo:
    # Output
    out = AuthInfo()

    # Pase Login info
    lgnInfo = re.findall(r'Good Morning, (.*)\.&nbsp;&nbsp;Today is .*, (.*).<br>\(Last Login Time (.*)\)', data, re.M)
    if len(lgnInfo) == 1:
        out.first_name = lgnInfo[0][0]
        out.has_school_today = lgnInfo[0][1] != "a day off of school"
        out.last_login_time = lgnInfo[0][2]

    # Parse student auth info
    authInfo = re.findall(r"student_no=(.*)&code=(.*)&k=(.*)", data, re.M)
    if len(authInfo) == 1:
        out.student_number = int(authInfo[0][0])

    return out

# Login
def getAuthInfo(username, password) -> str:
    session = requests.Session()

    # Make primary request to read auth secrets embedded in the response
    data = session.get("https://schoolapps2.tvdsb.ca/students/student_login/lgn.aspx")

    # Read all secrets
    secrets = re.findall(r'input type="hidden" name="(.*)" id=".*" value="(.*)"', data.text, re.M)
    
    # Build HTTP request
    request_body = {
        "txtUserID": username,
        "txtPwd": password,
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "btnSubmit":"Login"
    }

    # Add all secrets
    for secret in secrets:
        request_body[secret[0]] = secret[1]

    # Make request to schoolapps2 server
    data = session.post("https://schoolapps2.tvdsb.ca/students/student_login/lgn.aspx", data=request_body)

    # Handle invalid auth
    # We just search for a word that only exists in the authenticated parts of the site
    if "Google" not in data.text:
        raise InvalidAuth("Login invalid")

    # Get student info
    studentInfo = _webpageToAuthInfo(data.text)

    # Get session data
    studentInfo.session = session.cookies.get_dict()

    # Return auth info
    return studentInfo
    
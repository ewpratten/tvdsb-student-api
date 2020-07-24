import re
from typing import List

import requests

from .auth import LoginCreds, Student, getStudent


def getMarkHistory(creds: LoginCreds) -> List[dict]:

    # Make auth to get student info
    student: Student = getStudent(creds)

    # Make marks request
    data = student._session.get(
        "https://schoolapps2.tvdsb.ca/students/portal_secondary/student_Info/stnt_transcript.asp"
    )

    # Parse out every entry
    raw_marks = re.findall(
        r"<tr valign='[a-z]*' bgcolor=['a-zA-Z0-9#]*><td>([^<]*)<\/td><td>([^<]*)<\/td><td>([^<]*)<\/td><td>([^<]*)<\/td><td>([^<]*)<\/td><td>([^<]*)<\/td><td>([^<]*)<\/td><td>([^<]*)<\/td><td>([^<]*)<\/td><\/tr>",
        data.text,
        re.M,
    )

    # Clean up marking info
    marks = {}
    for mark in raw_marks:
        m = {}
        m["date"] = mark[0].replace("&nbsp;", "").strip()
        m["course"] = mark[1].replace("&nbsp;", "").strip()
        m["mark"] = int(mark[2].replace("&nbsp;", "").strip())
        m["comment"] = mark[3].replace("&nbsp;", "").strip()
        m["skills"] = {}
        m["skills"]["independence"] = mark[4].replace("&nbsp;", "").strip()
        m["skills"]["teamwork"] = mark[5].replace("&nbsp;", "").strip()
        m["skills"]["organization"] = mark[6].replace("&nbsp;", "").strip()
        m["skills"]["homework"] = mark[7].replace("&nbsp;", "").strip()
        m["skills"]["initiative"] = mark[8].replace("&nbsp;", "").strip()

        # Determine year
        year = m["date"].split(".")[0]

        # Add to marks
        if year not in marks:
            marks[year] = []
        marks[year].append(m)

    return marks

import re
from typing import List

import requests

from .auth import LoginCreds, Student, getStudent


def getAttendanceRecords(creds: LoginCreds) -> List[dict]:

    # Make auth to get student info
    student: Student = getStudent(creds)

    # Make attendance request
    data = student._session.get(
        "https://schoolapps2.tvdsb.ca/students/portal_secondary/student_Info/stnt_attendance.asp"
    )

    # Parse out all record info
    raw_records = re.findall(
        r"<td>([0-9]*\/[0-9]*\/[0-9]*)<\/td><td>([0-9]*)<\/td><td>([A-Z0-9-]*)<\/td><td>([A-Z]*)<\/td><td> ([^<]*)<\/td>",
        data.text,
    )

    # Convert raw record data to AttendanceRecords
    records = []
    for record in raw_records:
        r = {}
        r["date"] = record[0].strip()
        r["period"] = int(record[1].strip())
        r["course_code"] = record[2].strip()
        r["code"] = record[3].strip()
        r["reason"] = record[4].strip()
        records.append(r)

    return records

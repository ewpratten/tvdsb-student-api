import re
from typing import List

import requests

from .auth import LoginCreds, Student, getStudent


def getTimetable(creds: LoginCreds) -> List[dict]:

    # Make auth to get student info
    student: Student = getStudent(creds)

    # Make marks request
    data = student._session.get(
        "https://schoolapps2.tvdsb.ca/students/portal_secondary/student_Info/timetable2.asp"
    )

    # Parse student info
    info = re.findall(
        r"<b>([a-zA-Z]*), ([a-zA-Z]*)<\/b><br>Student#: *([0-9]*)<br>OEN#: *([0-9]*)<\/td><td>Grade: ([0-9]*)<\/td><td>Locker #: ([0-9]*)",
        data.text,
        re.M,
    )[0]

    # Get info from info
    name = [info[1], info[0]]
    student_number = info[2]
    oen = info[3]
    grade = info[4]
    locker = info[5]

    # Read courses info
    courses = re.findall(
        r"Period:&nbsp;([0-9]*)<br>([0-9]*)-([0-9]*)<\/small><\/td><td>([^<]*)",
        data.text,
        re.M,
    )

    # This handles guessing which semester every course is in
    semesters = [[]]
    waiting_for_new_course = False

    def _courseInSemester(course, semester) -> bool:
        for _c in semester:
            if _c["course_code"] == course[3]:
                return True
        return False

    for course in courses:

        # Check if this course is a duplicate
        if _courseInSemester(course, semesters[-1]):
            waiting_for_new_course = True
            continue

        # Handle waiting (this should create a new semester)
        if waiting_for_new_course:
            semesters.append([])
            waiting_for_new_course = False

        # Write course to the latest semester
        semesters[-1].append(
            {
                "course_code": course[3],
                "period": int(course[0]),
                "start_time": int(course[1]),
                "end_time": int(course[2]),
            }
        )

    # Create output
    output = {
        "student_info": {
            "name": name,
            "student_number": int(student_number),
            "ontario_education_number": int(oen),
            "grade": int(grade),
            "locker_number": int(locker) if locker else None,
        },
        "course_semesters": semesters,
    }

    return output

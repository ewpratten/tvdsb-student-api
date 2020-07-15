import argparse
import getpass
import json
import pprint
from typing import List

import tvdsb_student

if __name__ == "__main__":

    # Create parser
    ap = argparse.ArgumentParser(
        description="Dumps all TVDSB Student info to STDOUT as JSON"
    )

    # Auth
    ap.add_argument("--user", help="TVDSB account username", required=True)
    ap.add_argument("--passwd", help="TVDSB account password", required=False)

    # Parse arguments
    args = ap.parse_args()

    # Handle auth
    if not args.passwd:
        print("Student information is password protected")
        args.passwd = getpass.getpass("TVDSB Password: ")

    # Log in
    creds = tvdsb_student.LoginCreds(args.user, args.passwd)

    # Build output
    output = {}

    # # Read attendance records
    attendance: List[dict] = tvdsb_student.getAttendanceRecords(creds)
    # print(attendance)
    output["attendance"] = attendance

    # # Read marking records
    marks: List[dict] = tvdsb_student.getMarkHistory(creds)
    # print(marks)
    output["marks"] = marks

    # Read student payment info
    payment: dict = tvdsb_student.getPaymentInfo(creds)
    # print(payment)
    output["payment"] = payment

    # Read timetable info
    timetable: dict = tvdsb_student.getTimetable(creds)
    # pprint.pprint(timetable)
    output["timetable"] = timetable

    print(json.dumps(output, indent=1, sort_keys=True))

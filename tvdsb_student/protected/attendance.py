import requests
import re
from typing import List
from ..auth import Student

class AttendanceRecord:
    """Attendance information"""
    _date: str
    _period: int
    _course_code: str
    _code: str
    _reason: str

    def getDate(self) -> str:
        """Get this record's date

        Returns:
            str: Date
        """
        return self._date
    
    def getPeriod(self) -> int:
        """Get this record's school period number

        Returns:
            int: Period number
        """
        return self._period

    def getCourseCode(self) -> str:
        """Get this record's coruse code

        Returns:
            str: Course code
        """
        return self._course_code
    
    def getAttendanceCode(self) -> str:
        """Get the internal attendance record type code

        Returns:
            str: Record code
        """
        return self._code

    def getReason(self) -> str:
        """Get this record's filed reason

        Returns:
            str: Reason
        """
        return self._reason
    
    def __str__(self):
        return str({
            "date": self._date,
            "period": self._period,
            "course_code": self._course_code,
            "code": self._code,
            "reason": self._reason
        })

def getAttendanceRecords(student: Student) -> List[AttendanceRecord]:
    session = requests.Session()

    # Update session cookies
    requests.utils.add_dict_to_cookiejar(session.cookies, student._session)

    # Make attendance request
    data = session.get("https://schoolapps2.tvdsb.ca/students/portal_secondary/student_Info/stnt_attendance.asp")

    # Parse out all record info
    raw_records = re.findall(r"<td>([0-9]*\/[0-9]*\/[0-9]*)<\/td><td>([0-9]*)<\/td><td>([A-Z0-9-]*)<\/td><td>([A-Z]*)<\/td><td> ([^<]*)<\/td>", data.text)
    
    # Convert raw record data to AttendanceRecords
    records = []
    for record in raw_records:
        r = AttendanceRecord()
        r._date = record[0]
        r._period = record[1]
        r._course_code = record[2]
        r._code = record[3]
        r._reason = record[4]
        records.append(r)

    return records
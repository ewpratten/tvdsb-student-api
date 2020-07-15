# tvdsb-student-api
A Python library and CLI tool for interacting with the TVDSB Student Portal service

## CLI tool usage

```
usage: python3 -m tvdsb_student [-h] --user USER [--passwd PASSWD]

Dumps all TVDSB Student info to STDOUT as JSON

optional arguments:
  -h, --help       show this help message and exit
  --user USER      TVDSB account username
  --passwd PASSWD  TVDSB account password
```

This script will dump JSON to STDOUT

## Library usage
```python
from typing import List
import tvdsb_student

# TVDSB Network auth
user = "lastfirst123"           # This is your network username
passwd = "mySecurePassw0rD!"    # This is your network password

# Create an auth object
creds = tvdsb_student.LoginCreds(user, passwd)

# Read student attendance records
attendance: List[dict] = tvdsb_student.getAttendanceRecords(creds)

# Read student mark history (all report card info)
marks: List[dict] = tvdsb_student.getMarkHistory(creds)

# Read student payment info
payment: dict = tvdsb_student.getPaymentInfo(creds)
```

### Data schemas

These are all examples of the datastructures generated from polling my student account

#### Attendance
```js
[
    {
        "code": "G",                                    // Single char denoting incident type
        "course_code": "SPH3UK-02",                     // Course code
        "date": "3/24/2020",                            // Date of incident
        "period": 2,                                    // School period
        "reason": "School Closure/Services Withdrawal"  // Notes about incident
    }
]
```

#### Marks
```js
{
    "2020": [ // Courses are grouped by year
        {
            "comment": ".",         // Teacher's comment. This may be a "." if the class finished during a teachers strike
            "course": "ICS4U1",     // Course code
            "date": "2020.06.26",   // Date the grade was last updated in MarkBook
            "mark": 100,            // Percent grade out of 100
            "skills": {             // Listing of all "skills" on a normal report card. Single char, one of [F, S, G, E]
                "homework": "E",
                "independence": "E",
                "initiative": "E",
                "organization": "E",
                "teamwork": "E"
            }
        }
    ]
}
```

#### Payment
```js
{
    "pin": 1234567890 // PIN number used to link a parent's payment account to a student (not my real pin)
}
```
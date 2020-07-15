# Student auth
from .auth import LoginCreds, Student, getStudent
# Getters about private information
from .protected.attendance import getAttendanceRecords
from .protected.marks import getMarkHistory
from .protected.payment import getPaymentInfo
from .protected.timetable import getTimetable

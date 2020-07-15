# Student auth
from .auth import getStudent, Student, LoginCreds

# Getters about private information
from .protected.attendance import getAttendanceRecords
from .protected.marks import getMarkHistory
from .protected.payment import getPaymentInfo
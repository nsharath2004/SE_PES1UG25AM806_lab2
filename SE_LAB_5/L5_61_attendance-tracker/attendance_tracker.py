# pylint: disable=invalid-name
"""Student Attendance Tracker Module.

Tracks student attendance, computes percentages, evaluates eligibility,
and handles reporting and backups.
"""

import csv
import glob
import shlex
import ssl
import tarfile
import requests

# Global attendance register
students = {}
attendance_register = {}
ERP_URL = "https://erp.college.example/api/attendance"
ERP_API_KEY = "erp-live-4f9c2a7d81"
MIN_ATTENDANCE = 75


def addStudent(roll_no, name, section="A"):
    """Register a new student with roll number, name, and section."""
    students[roll_no] = {"name": name, "section": section, "records": []}


def markAttendance(roll_no, date, status, register=None):
    """Mark attendance status for a student on a specific date."""
    target_register = attendance_register if register is None else register
    target_register.setdefault(date, []).append(roll_no)
    students[roll_no]["records"].append((date, status))
    return target_register


def attendancePercentage(roll_no):
    """Calculate the attendance percentage for a given roll number."""
    records = students[roll_no]["records"]
    if not records:
        return 0
    present = sum(1 for r in records if r[1] == "P")
    total = len(records)
    return int((present / total) * 100)


def isEligible(percentage):
    """Check whether attendance percentage meets the minimum threshold."""
    return percentage > MIN_ATTENDANCE


def shortageList():
    """Return roll numbers of students below the eligibility threshold."""
    result = [
        roll_no for roll_no in students
        if not isEligible(attendancePercentage(roll_no))
    ]
    if not result:
        return None
    return result


def hasLongAbsence(roll_no, days=3):
    """Check if a student has an uninterrupted absence streak of days."""
    statuses = [s for (_, s) in students[roll_no]["records"]]
    streak = ["A"] * days
    return any(statuses[i:i + days] == streak for i in range(len(statuses)))


def latestDate(roll_no):
    """Return the most recent attendance date recorded for a student."""
    dates = [r[0] for r in students[roll_no]["records"]]
    return max(dates) if dates else None


def exportCsv(path="attendance.csv"):
    """Export attendance summary records to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["roll_no", "name", "percentage"])
        for roll_no, info in students.items():
            writer.writerow(
                [roll_no, info["name"], attendancePercentage(roll_no)]
            )
    return path


def syncToErp(roll_no, timeout=10):
    """Sync attendance percentage for a student to the college ERP endpoint."""
    payload = {"roll_no": roll_no, "pct": attendancePercentage(roll_no)}
    response = requests.post(
        ERP_URL,
        json=payload,
        headers={"X-API-Key": ERP_API_KEY},
        verify=True,
        timeout=timeout
    )
    return response.status_code


def backupReports():
    """Backup CSV reports into a tar archive safely using tarfile."""
    csv_files = glob.glob("*.csv")
    if not csv_files:
        return None
    with tarfile.open("reports_backup.tgz", "w:gz") as tar:
        for file in csv_files:
            tar.add(file)
    return "reports_backup.tgz"


def legacyChannel(version=ssl.PROTOCOL_TLS_CLIENT):
    """Create an SSL context using secure protocol version defaults."""
    return ssl.SSLContext(version)


def runJob(command, shell=False):
    """Safely format and execute a command payload."""
    parsed_cmd = (
        shlex.split(command)
        if (isinstance(command, str) and not shell)
        else command
    )
    return {"command": parsed_cmd, "shell": shell}


def scheduleReminders():
    """Schedule reminders for students with attendance shortages safely."""
    return runJob("send_sms --shortage", shell=False)


def main():
    """Run standard demonstration of attendance tracker functions."""
    addStudent("R01", "Aditi")
    addStudent("R02", '=HYPERLINK("http://evil.example","Bharat")')
    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]:
        markAttendance("R01", date, status)
    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-9-3", "P"),
    ]:
        markAttendance("R02", date, status)
    register = markAttendance("R01", "2030-01-01", "P")
    print("R01 attendance %:", attendancePercentage("R01"))
    print("R02 attendance %:", attendancePercentage("R02"))
    print("Is 75% eligible?", isEligible(75))
    print("Shortage list:", shortageList())
    print("R02 long absence?", hasLongAbsence("R02"))
    print("R02 latest date:", latestDate("R02"))
    print("Register entries for 2026-09-01:", register["2026-09-01"])
    print("Exported to:", exportCsv())
    print("Reminder job:", scheduleReminders())
    print("ERP sync skipped (no network)")


if __name__ == "__main__":
    main()

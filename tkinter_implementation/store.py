"""
Store facade wrapping SchoolSystem.

- Always saves after a successful change.
- Adds CSV export for quick grading checks.
"""

from __future__ import annotations
import csv
from typing import List, Tuple
from school import SchoolSystem, Student, Instructor, Course

class SchoolStore:
    """Data access layer.

    :param jsonpath: file used for persistence (default: school_data.json)
    """

    def __init__(self, jsonpath: str = "school_data.json"):
        self.jsonpath = jsonpath
        self.system: SchoolSystem = SchoolSystem.load(jsonpath)

    # ----- create -----
    def addstudent(self, s: Student) -> bool:
        ok = self.system.addstudent(s)
        if ok:
            self.save()
        return ok

    def addinstructor(self, i: Instructor) -> bool:
        ok = self.system.addinstructor(i)
        if ok:
            self.save()
        return ok

    def addcourse(self, c: Course) -> bool:
        ok = self.system.addcourse(c)
        if ok:
            self.save()
        return ok

    # ----- delete -----
    def removestudent(self, sid: str) -> bool:
        ok = self.system.removestudent(sid)
        if ok:
            self.save()
        return ok

    def removeinstructor(self, iid: str) -> bool:
        ok = self.system.removeinstructor(iid)
        if ok:
            self.save()
        return ok

    def removecourse(self, cid: str) -> bool:
        ok = self.system.removecourse(cid)
        if ok:
            self.save()
        return ok

    # ----- relations -----
    def assigncourse(self, iid: str, cid: str) -> bool:
        ok = self.system.assign(iid, cid)
        if ok:
            self.save()
        return ok

    def joincourse(self, sid: str, cid: str) -> bool:
        ok = self.system.register(sid, cid)
        if ok:
            self.save()
        return ok

    # ----- search + export -----
    def search(self, q: str) -> List[Tuple[str, str, str, str]]:
        """Return rows as (Type, Name, Code, Info)."""
        return self.system.search(q)

    def exportcsv(self, path: str) -> None:
        """Write a wide CSV for all entities."""
        rows = []
        for s in self.system.students:
            rows.append([
                "Student", s.name, s.age, s.email, s.studentid,
                ", ".join(c.coursename for c in s.courses),
            ])
        for i in self.system.instructors:
            rows.append([
                "Instructor", i.name, i.age, i.email, i.instructorid,
                ", ".join(c.coursename for c in i.courses),
            ])
        for c in self.system.courses:
            rows.append([
                "Course", c.coursename, "", "", c.courseid,
                "Instructor: " + (c.instructor.name if c.instructor else "None") +
                " | Students: " + ", ".join(s.name for s in c.students),
            ])

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Type", "Name", "Age", "Email", "ID", "Info"])
            w.writerows(rows)

    # ----- save -----
    def save(self) -> None:
        self.system.save(self.jsonpath)

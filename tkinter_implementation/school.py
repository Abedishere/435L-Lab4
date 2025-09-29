"""
Model layer for the School Manager app.

It defines:
- Person (base)
- Student, Instructor
- Course
- SchoolSystem (registry/search + JSON I/O)

Simple, readable validation; minimal assumptions.
"""

from __future__ import annotations
import json
import re
from typing import List, Optional, Tuple

_email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Person:
    """Base person with name/age/email."""

    def __init__(self, name: str, age: int, email: str):
        if not name:
            raise ValueError("name must not be empty")
        if age is None or age < 0:
            raise ValueError("age must be >= 0")
        if email and not _email_re.match(email):
            raise ValueError("email format looks wrong")
        self.name = name
        self.age = int(age)
        self.email = email


class Student(Person):
    """Student with a unique string id and enrolled courses."""

    def __init__(self, name: str, age: int, email: str, studentid: str):
        super().__init__(name, age, email)
        if not studentid:
            raise ValueError("studentid must not be empty")
        self.studentid = studentid
        self.courses: List["Course"] = []

    def enroll(self, course: "Course") -> None:
        """Link this student to a course if not already linked."""
        if course not in self.courses:
            self.courses.append(course)


class Instructor(Person):
    """Instructor with a unique string id and assigned courses."""

    def __init__(self, name: str, age: int, email: str, instructorid: str):
        super().__init__(name, age, email)
        if not instructorid:
            raise ValueError("instructorid must not be empty")
        self.instructorid = instructorid
        self.courses: List["Course"] = []

    def take(self, course: "Course") -> None:
        """Link this instructor to a course if not already linked."""
        if course not in self.courses:
            self.courses.append(course)


class Course:
    """Course with id, name, optional instructor, and students."""

    def __init__(
        self, courseid: str, coursename: str, instructor: Optional[Instructor] = None
        ):
        if not courseid:
            raise ValueError("courseid must not be empty")
        if not coursename:
            raise ValueError("coursename must not be empty")
        self.courseid = courseid
        self.coursename = coursename
        self.instructor: Optional[Instructor] = instructor
        self.students: List[Student] = []

    def addstudent(self, s: Student) -> None:
        """Link this course to a student if not already linked."""
        if s not in self.students:
            self.students.append(s)


class SchoolSystem:
    """In-memory registry for students, instructors, and courses.

    Provides add/find/remove, relations (assign/register), a
    simple text search, and JSON load/save.
    """

    def __init__(self):
        self.students: List[Student] = []
        self.instructors: List[Instructor] = []
        self.courses: List[Course] = []

    # ---------- find ----------
    def findstudent(self, sid: str) -> Optional[Student]:
        return next((s for s in self.students if s.studentid == sid), None)

    def findinstructor(self, iid: str) -> Optional[Instructor]:
        return next((i for i in self.instructors if i.instructorid == iid), None)

    def findcourse(self, cid: str) -> Optional[Course]:
        return next((c for c in self.courses if c.courseid == cid), None)

    # ---------- add/remove ----------
    def addstudent(self, s: Student) -> bool:
        """Add a student if id is unique; returns True if added."""
        if self.findstudent(s.studentid):
            return False
        self.students.append(s)
        return True

    def addinstructor(self, i: Instructor) -> bool:
        if self.findinstructor(i.instructorid):
            return False
        self.instructors.append(i)
        return True

    def addcourse(self, c: Course) -> bool:
        if self.findcourse(c.courseid):
            return False
        self.courses.append(c)
        return True

    def removestudent(self, sid: str) -> bool:
        s = self.findstudent(sid)
        if not s:
            return False
        for c in self.courses:
            if s in c.students:
                c.students.remove(s)
        self.students.remove(s)
        return True

    def removeinstructor(self, iid: str) -> bool:
        i = self.findinstructor(iid)
        if not i:
            return False
        for c in self.courses:
            if c.instructor == i:
                c.instructor = None
        self.instructors.remove(i)
        return True

    def removecourse(self, cid: str) -> bool:
        c = self.findcourse(cid)
        if not c:
            return False
        for s in self.students:
            if c in s.courses:
                s.courses.remove(c)
        if c.instructor and c in c.instructor.courses:
            c.instructor.courses.remove(c)
        self.courses.remove(c)
        return True

    # ---------- relations ----------
    def assign(self, iid: str, cid: str) -> bool:
        """Set an instructor on a course and link both sides."""
        i, c = self.findinstructor(iid), self.findcourse(cid)
        if not i or not c:
            return False
        if c.instructor == i:
            return False
        c.instructor = i
        i.take(c)
        return True

    def register(self, sid: str, cid: str) -> bool:
        """Enroll a student in a course and link both sides."""
        s, c = self.findstudent(sid), self.findcourse(cid)
        if not s or not c:
            return False
        if s in c.students:
            return False
        c.addstudent(s)
        s.enroll(c)
        return True

    # ---------- search ----------
    def search(self, q: str) -> List[Tuple[str, str, str, str]]:
        """Basic search across all entities (case-insensitive)."""
        q = (q or "").strip().lower()
        rows: List[Tuple[str, str, str, str]] = []

        for s in self.students:
            if any(q in str(x).lower() for x in (s.name, s.email, s.studentid)):
                rows.append((
                    "Student", s.name, s.studentid,
                    ", ".join(c.coursename for c in s.courses)
                ))

        for i in self.instructors:
            if any(q in str(x).lower() for x in (i.name, i.email, i.instructorid)):
                rows.append((
                    "Instructor", i.name, i.instructorid,
                    ", ".join(c.coursename for c in i.courses)
                ))

        for c in self.courses:
            inst_name = c.instructor.name if c.instructor else "None"
            if any(q in str(x).lower() for x in (c.coursename, c.courseid, inst_name)):
                rows.append((
                    "Course", c.coursename, c.courseid,
                    f"Instructor: {inst_name}; Students: " +
                    ", ".join(s.name for s in c.students)
                ))
        return rows

    # ---------- JSON I/O ----------
    def tojson(self) -> dict:
        """Serialize to a JSON-serializable dict (by ids, not objects)."""
        return {
            "students": [
                {
                    "name": s.name, "age": s.age, "email": s.email,
                    "studentid": s.studentid,
                    "courses": [c.courseid for c in s.courses],
                } for s in self.students
            ],
            "instructors": [
                {
                    "name": i.name, "age": i.age, "email": i.email,
                    "instructorid": i.instructorid,
                    "courses": [c.courseid for c in i.courses],
                } for i in self.instructors
            ],
            "courses": [
                {
                    "courseid": c.courseid, "coursename": c.coursename,
                    "instructor": (c.instructor.instructorid if c.instructor else None),
                    "students": [s.studentid for s in c.students],
                } for c in self.courses
            ],
        }

    @classmethod
    def fromjson(cls, data: dict) -> "SchoolSystem":
        """Build an instance from a dict (links restored both ways)."""
        sysm = cls()
        sid_map: dict[str, Student] = {}
        iid_map: dict[str, Instructor] = {}
        # create persons
        for s in data.get("students", []):
            obj = Student(s["name"], int(s["age"]), s.get("email", ""), s["studentid"])
            sysm.students.append(obj)
            sid_map[obj.studentid] = obj
        for i in data.get("instructors", []):
            obj = Instructor(i["name"], int(i["age"]), i.get("email", ""), i["instructorid"])
            sysm.instructors.append(obj)
            iid_map[obj.instructorid] = obj
        # create courses (instructor linked later)
        for c in data.get("courses", []):
            inst = iid_map.get(c.get("instructor")) if c.get("instructor") else None
            obj = Course(c["courseid"], c["coursename"], inst)
            sysm.courses.append(obj)
            if inst:
                inst.take(obj)
        # link students <-> courses
        for c in data.get("courses", []):
            course = sysm.findcourse(c["courseid"])
            for sid in c.get("students", []):
                s = sid_map.get(sid)
                if s and course:
                    course.addstudent(s)
                    s.enroll(course)

        return sysm
    @classmethod
    def load(cls, path: str) -> "SchoolSystem":
        """Load from JSON file; return an empty system if file is missing."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return cls.fromjson(json.load(f))
        except FileNotFoundError:
            return cls()
    def save(self, path: str) -> None:
        """Write current state to the JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.tojson(), f, ensure_ascii=False, indent=2)

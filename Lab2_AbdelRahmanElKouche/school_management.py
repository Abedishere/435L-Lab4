import json
import re
from typing import List, Dict, Any


class Person:
    def __init__(self, name: str, age: int, email: str):
        if not self._validate_name(name):
            raise ValueError("Name must be a non-empty string")
        if not self._validate_age(age):
            raise ValueError("Age must be a non-negative integer")
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        
        self.name = name
        self.age = age
        self._email = email
    
    def introduce(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
    
    @staticmethod
    def _validate_name(name: str) -> bool:
        return isinstance(name, str) and len(name.strip()) > 0
    
    @staticmethod
    def _validate_age(age: int) -> bool:
        return isinstance(age, int) and age >= 0
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return isinstance(email, str) and re.match(pattern, email) is not None
    
    def get_email(self):
        return self._email
    
    def set_email(self, email: str):
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        self._email = email


class Student(Person):
    def __init__(self, name: str, age: int, email: str, student_id: str):
        super().__init__(name, age, email)
        if not self._validate_student_id(student_id):
            raise ValueError("Student ID must be a non-empty string")
        self.student_id = student_id
        self.registered_courses = []
    
    def register_course(self, course):
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)
    
    @staticmethod
    def _validate_student_id(student_id: str) -> bool:
        return isinstance(student_id, str) and len(student_id.strip()) > 0
    
    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email,
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses]
        }


class Instructor(Person):
    def __init__(self, name: str, age: int, email: str, instructor_id: str):
        super().__init__(name, age, email)
        if not self._validate_instructor_id(instructor_id):
            raise ValueError("Instructor ID must be a non-empty string")
        self.instructor_id = instructor_id
        self.assigned_courses = []
    
    def assign_course(self, course):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self
    
    @staticmethod
    def _validate_instructor_id(instructor_id: str) -> bool:
        return isinstance(instructor_id, str) and len(instructor_id.strip()) > 0
    
    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email,
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses]
        }


class Course:
    def __init__(self, course_id: str, course_name: str, instructor=None):
        if not self._validate_course_id(course_id):
            raise ValueError("Course ID must be a non-empty string")
        if not self._validate_course_name(course_name):
            raise ValueError("Course name must be a non-empty string")
        
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []
    
    def add_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
    
    @staticmethod
    def _validate_course_id(course_id: str) -> bool:
        return isinstance(course_id, str) and len(course_id.strip()) > 0
    
    @staticmethod
    def _validate_course_name(course_name: str) -> bool:
        return isinstance(course_name, str) and len(course_name.strip()) > 0
    
    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor_id': self.instructor.instructor_id if self.instructor else None,
            'enrolled_students': [student.student_id for student in self.enrolled_students]
        }


class SchoolManagementSystem:
    def __init__(self):
        self.students = []
        self.instructors = []
        self.courses = []
    
    def add_student(self, student: Student):
        self.students.append(student)
    
    def add_instructor(self, instructor: Instructor):
        self.instructors.append(instructor)
    
    def add_course(self, course: Course):
        self.courses.append(course)
    
    def find_student_by_id(self, student_id: str):
        return next((s for s in self.students if s.student_id == student_id), None)
    
    def find_instructor_by_id(self, instructor_id: str):
        return next((i for i in self.instructors if i.instructor_id == instructor_id), None)
    
    def find_course_by_id(self, course_id: str):
        return next((c for c in self.courses if c.course_id == course_id), None)
    
    def save_data(self, filename: str = "school_data.json"):
        data = {
            'students': [student.to_dict() for student in self.students],
            'instructors': [instructor.to_dict() for instructor in self.instructors],
            'courses': [course.to_dict() for course in self.courses]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self, filename: str = "school_data.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.students = []
            self.instructors = []
            self.courses = []
            
            for instructor_data in data.get('instructors', []):
                instructor = Instructor(
                    instructor_data['name'],
                    instructor_data['age'],
                    instructor_data['email'],
                    instructor_data['instructor_id']
                )
                self.add_instructor(instructor)
            
            for course_data in data.get('courses', []):
                instructor = None
                if course_data.get('instructor_id'):
                    instructor = self.find_instructor_by_id(course_data['instructor_id'])
                
                course = Course(
                    course_data['course_id'],
                    course_data['course_name'],
                    instructor
                )
                self.add_course(course)
                
                if instructor:
                    instructor.assign_course(course)
            
            for student_data in data.get('students', []):
                student = Student(
                    student_data['name'],
                    student_data['age'],
                    student_data['email'],
                    student_data['student_id']
                )
                self.add_student(student)
                
                for course_id in student_data.get('registered_courses', []):
                    course = self.find_course_by_id(course_id)
                    if course:
                        student.register_course(course)
            
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def remove_student(self, student_id: str):
        student = self.find_student_by_id(student_id)
        if student:
            for course in student.registered_courses[:]:
                if student in course.enrolled_students:
                    course.enrolled_students.remove(student)
            self.students.remove(student)
            return True
        return False
    
    def remove_instructor(self, instructor_id: str):
        instructor = self.find_instructor_by_id(instructor_id)
        if instructor:
            for course in instructor.assigned_courses[:]:
                course.instructor = None
            self.instructors.remove(instructor)
            return True
        return False
    
    def remove_course(self, course_id: str):
        course = self.find_course_by_id(course_id)
        if course:
            for student in course.enrolled_students[:]:
                if course in student.registered_courses:
                    student.registered_courses.remove(course)
            if course.instructor:
                if course in course.instructor.assigned_courses:
                    course.instructor.assigned_courses.remove(course)
            self.courses.remove(course)
            return True
        return False
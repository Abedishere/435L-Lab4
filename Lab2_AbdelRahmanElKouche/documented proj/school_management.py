"""School Management System Core Module

This module provides the core classes for managing a school system including
students, instructors, courses, and the overall school management system.
It includes comprehensive validation, data persistence, and relationship management.
"""

import json
import re
from typing import List, Dict, Any


class Person:
    """Base class representing a person in the school management system.
    
    This abstract base class provides common functionality for all person types
    in the system, including name, age, and email management with validation.
    
    :param name: The person's full name
    :type name: str
    :param age: The person's age in years
    :type age: int
    :param email: The person's email address
    :type email: str
    :raises ValueError: If any parameter fails validation
    """
    
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
        """Print a formatted introduction message for the person.
        
        Outputs a standardized greeting including the person's name and age.
        This method is primarily used for testing and demonstration purposes.
        """
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
    
    @staticmethod
    def _validate_name(name: str) -> bool:
        """Validate that a name is a non-empty string.
        
        :param name: The name to validate
        :type name: str
        :return: True if name is valid, False otherwise
        :rtype: bool
        """
        return isinstance(name, str) and len(name.strip()) > 0
    
    @staticmethod
    def _validate_age(age: int) -> bool:
        """Validate that age is a non-negative integer.
        
        :param age: The age to validate
        :type age: int
        :return: True if age is valid, False otherwise
        :rtype: bool
        """
        return isinstance(age, int) and age >= 0
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format using regex pattern matching.
        
        Uses a comprehensive regex pattern to validate email addresses
        according to standard email format requirements.
        
        :param email: The email address to validate
        :type email: str
        :return: True if email format is valid, False otherwise
        :rtype: bool
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return isinstance(email, str) and re.match(pattern, email) is not None
    
    def get_email(self):
        """Get the person's email address.
        
        :return: The person's email address
        :rtype: str
        """
        return self._email
    
    def set_email(self, email: str):
        """Set a new email address for the person.
        
        :param email: The new email address
        :type email: str
        :raises ValueError: If the email format is invalid
        """
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        self._email = email


class Student(Person):
    """Class representing a student in the school management system.
    
    Extends the Person class to include student-specific functionality such as
    student ID management and course registration tracking.
    
    :param name: The student's full name
    :type name: str
    :param age: The student's age in years
    :type age: int
    :param email: The student's email address
    :type email: str
    :param student_id: Unique identifier for the student
    :type student_id: str
    :raises ValueError: If any parameter fails validation
    
    :ivar student_id: The student's unique identifier
    :vartype student_id: str
    :ivar registered_courses: List of courses the student is registered for
    :vartype registered_courses: List[Course]
    """
    
    def __init__(self, name: str, age: int, email: str, student_id: str):
        super().__init__(name, age, email)
        if not self._validate_student_id(student_id):
            raise ValueError("Student ID must be a non-empty string")
        self.student_id = student_id
        self.registered_courses = []
    
    def register_course(self, course):
        """Register the student for a course.
        
        Adds the course to the student's registered courses list and
        adds the student to the course's enrolled students list.
        Prevents duplicate registrations.
        
        :param course: The course to register for
        :type course: Course
        """
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)
    
    @staticmethod
    def _validate_student_id(student_id: str) -> bool:
        """Validate that a student ID is a non-empty string.
        
        :param student_id: The student ID to validate
        :type student_id: str
        :return: True if student ID is valid, False otherwise
        :rtype: bool
        """
        return isinstance(student_id, str) and len(student_id.strip()) > 0
    
    def to_dict(self):
        """Convert student object to dictionary representation.
        
        Creates a dictionary containing all student data including
        registered course IDs for serialization purposes.
        
        :return: Dictionary representation of the student
        :rtype: dict
        """
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email,
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses]
        }


class Instructor(Person):
    """Class representing an instructor in the school management system.
    
    Extends the Person class to include instructor-specific functionality such as
    instructor ID management and course assignment tracking.
    
    :param name: The instructor's full name
    :type name: str
    :param age: The instructor's age in years
    :type age: int
    :param email: The instructor's email address
    :type email: str
    :param instructor_id: Unique identifier for the instructor
    :type instructor_id: str
    :raises ValueError: If any parameter fails validation
    
    :ivar instructor_id: The instructor's unique identifier
    :vartype instructor_id: str
    :ivar assigned_courses: List of courses assigned to the instructor
    :vartype assigned_courses: List[Course]
    """
    
    def __init__(self, name: str, age: int, email: str, instructor_id: str):
        super().__init__(name, age, email)
        if not self._validate_instructor_id(instructor_id):
            raise ValueError("Instructor ID must be a non-empty string")
        self.instructor_id = instructor_id
        self.assigned_courses = []
    
    def assign_course(self, course):
        """Assign a course to the instructor.
        
        Adds the course to the instructor's assigned courses list and
        sets the instructor as the course's instructor.
        Prevents duplicate assignments.
        
        :param course: The course to assign
        :type course: Course
        """
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self
    
    @staticmethod
    def _validate_instructor_id(instructor_id: str) -> bool:
        """Validate that an instructor ID is a non-empty string.
        
        :param instructor_id: The instructor ID to validate
        :type instructor_id: str
        :return: True if instructor ID is valid, False otherwise
        :rtype: bool
        """
        return isinstance(instructor_id, str) and len(instructor_id.strip()) > 0
    
    def to_dict(self):
        """Convert instructor object to dictionary representation.
        
        Creates a dictionary containing all instructor data including
        assigned course IDs for serialization purposes.
        
        :return: Dictionary representation of the instructor
        :rtype: dict
        """
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email,
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses]
        }


class Course:
    """Class representing a course in the school management system.
    
    Manages course information, instructor assignment, and student enrollment.
    Provides validation for course data and maintains bidirectional relationships
    with instructors and students.
    
    :param course_id: Unique identifier for the course
    :type course_id: str
    :param course_name: The name/title of the course
    :type course_name: str
    :param instructor: The instructor assigned to teach this course, defaults to None
    :type instructor: Instructor, optional
    :raises ValueError: If course_id or course_name fail validation
    
    :ivar course_id: The course's unique identifier
    :vartype course_id: str
    :ivar course_name: The course's name
    :vartype course_name: str
    :ivar instructor: The assigned instructor
    :vartype instructor: Instructor or None
    :ivar enrolled_students: List of students enrolled in the course
    :vartype enrolled_students: List[Student]
    """
    
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
        """Add a student to the course enrollment.
        
        Adds the student to the enrolled students list.
        Prevents duplicate enrollments.
        
        :param student: The student to enroll
        :type student: Student
        """
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
    
    @staticmethod
    def _validate_course_id(course_id: str) -> bool:
        """Validate that a course ID is a non-empty string.
        
        :param course_id: The course ID to validate
        :type course_id: str
        :return: True if course ID is valid, False otherwise
        :rtype: bool
        """
        return isinstance(course_id, str) and len(course_id.strip()) > 0
    
    @staticmethod
    def _validate_course_name(course_name: str) -> bool:
        """Validate that a course name is a non-empty string.
        
        :param course_name: The course name to validate
        :type course_name: str
        :return: True if course name is valid, False otherwise
        :rtype: bool
        """
        return isinstance(course_name, str) and len(course_name.strip()) > 0
    
    def to_dict(self):
        """Convert course object to dictionary representation.
        
        Creates a dictionary containing all course data including
        instructor ID and enrolled student IDs for serialization purposes.
        
        :return: Dictionary representation of the course
        :rtype: dict
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor_id': self.instructor.instructor_id if self.instructor else None,
            'enrolled_students': [student.student_id for student in self.enrolled_students]
        }


class SchoolManagementSystem:
    """Main class for managing the school management system.
    
    Provides centralized management of students, instructors, and courses.
    Handles data persistence, search functionality, and maintains system integrity.
    
    :ivar students: List of all students in the system
    :vartype students: List[Student]
    :ivar instructors: List of all instructors in the system
    :vartype instructors: List[Instructor]
    :ivar courses: List of all courses in the system
    :vartype courses: List[Course]
    """
    
    def __init__(self):
        self.students = []
        self.instructors = []
        self.courses = []
    
    def add_student(self, student: Student):
        """Add a student to the school management system.
        
        :param student: The student to add to the system
        :type student: Student
        """
        self.students.append(student)
    
    def add_instructor(self, instructor: Instructor):
        """Add an instructor to the school management system.
        
        :param instructor: The instructor to add to the system
        :type instructor: Instructor
        """
        self.instructors.append(instructor)
    
    def add_course(self, course: Course):
        """Add a course to the school management system.
        
        :param course: The course to add to the system
        :type course: Course
        """
        self.courses.append(course)
    
    def find_student_by_id(self, student_id: str):
        """Find a student by their unique student ID.
        
        :param student_id: The student ID to search for
        :type student_id: str
        :return: The student object if found, None otherwise
        :rtype: Student or None
        """
        return next((s for s in self.students if s.student_id == student_id), None)
    
    def find_instructor_by_id(self, instructor_id: str):
        """Find an instructor by their unique instructor ID.
        
        :param instructor_id: The instructor ID to search for
        :type instructor_id: str
        :return: The instructor object if found, None otherwise
        :rtype: Instructor or None
        """
        return next((i for i in self.instructors if i.instructor_id == instructor_id), None)
    
    def find_course_by_id(self, course_id: str):
        """Find a course by its unique course ID.
        
        :param course_id: The course ID to search for
        :type course_id: str
        :return: The course object if found, None otherwise
        :rtype: Course or None
        """
        return next((c for c in self.courses if c.course_id == course_id), None)
    
    def save_data(self, filename: str = "school_data.json"):
        """Save all system data to a JSON file.
        
        Serializes all students, instructors, and courses to a JSON file
        for persistent storage. Maintains relationships between objects.
        
        :param filename: Path to the output JSON file, defaults to "school_data.json"
        :type filename: str, optional
        """
        data = {
            'students': [student.to_dict() for student in self.students],
            'instructors': [instructor.to_dict() for instructor in self.instructors],
            'courses': [course.to_dict() for course in self.courses]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self, filename: str = "school_data.json"):
        """Load system data from a JSON file.
        
        Deserializes students, instructors, and courses from a JSON file
        and reconstructs all object relationships. Replaces current system state.
        
        :param filename: Path to the input JSON file, defaults to "school_data.json"
        :type filename: str, optional
        :return: True if loading was successful, False otherwise
        :rtype: bool
        """
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
        """Remove a student from the system by ID.
        
        Removes the student and cleans up all course registrations
        to maintain system integrity.
        
        :param student_id: The ID of the student to remove
        :type student_id: str
        :return: True if student was found and removed, False otherwise
        :rtype: bool
        """
        student = self.find_student_by_id(student_id)
        if student:
            for course in student.registered_courses[:]:
                if student in course.enrolled_students:
                    course.enrolled_students.remove(student)
            self.students.remove(student)
            return True
        return False
    
    def remove_instructor(self, instructor_id: str):
        """Remove an instructor from the system by ID.
        
        Removes the instructor and unassigns them from all courses
        to maintain system integrity.
        
        :param instructor_id: The ID of the instructor to remove
        :type instructor_id: str
        :return: True if instructor was found and removed, False otherwise
        :rtype: bool
        """
        instructor = self.find_instructor_by_id(instructor_id)
        if instructor:
            for course in instructor.assigned_courses[:]:
                course.instructor = None
            self.instructors.remove(instructor)
            return True
        return False
    
    def remove_course(self, course_id: str):
        """Remove a course from the system by ID.
        
        Removes the course and cleans up all student registrations and
        instructor assignments to maintain system integrity.
        
        :param course_id: The ID of the course to remove
        :type course_id: str
        :return: True if course was found and removed, False otherwise
        :rtype: bool
        """
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
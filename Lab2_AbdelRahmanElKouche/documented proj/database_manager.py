"""Database Management Module

This module provides database functionality for the school management system using SQLite.
It handles all database operations including CRUD operations, search functionality, 
backup/restore capabilities, and data synchronization with the core system objects.
"""

import sqlite3
import json
import shutil
from datetime import datetime
from typing import List, Tuple, Optional
from school_management import Student, Instructor, Course, SchoolManagementSystem


class DatabaseManager:
    """Database manager class for the school management system.
    
    Provides comprehensive database operations for managing students, instructors,
    courses, and their relationships using SQLite. Includes features like automatic
    timestamping, data integrity constraints, and backup functionality.
    
    :param db_path: Path to the SQLite database file, defaults to "school_management.db"
    :type db_path: str, optional
    
    :ivar db_path: Path to the database file
    :vartype db_path: str
    """
    
    def __init__(self, db_path: str = "school_management.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with all required tables and triggers.
        
        Creates the complete database schema including:
        - Students table with validation constraints
        - Instructors table with validation constraints
        - Courses table with foreign key relationships
        - Student-course registration junction table
        - Automatic timestamp update triggers
        
        All tables include created_at and updated_at timestamp fields.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL CHECK(age >= 0),
                    email TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS instructors (
                    instructor_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL CHECK(age >= 0),
                    email TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    course_id TEXT PRIMARY KEY,
                    course_name TEXT NOT NULL,
                    instructor_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id)
                        ON DELETE SET NULL ON UPDATE CASCADE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS student_course_registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    course_id TEXT NOT NULL,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (student_id)
                        ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses (course_id)
                        ON DELETE CASCADE ON UPDATE CASCADE,
                    UNIQUE(student_id, course_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS update_students_timestamp 
                AFTER UPDATE ON students
                BEGIN
                    UPDATE students SET updated_at = CURRENT_TIMESTAMP WHERE student_id = NEW.student_id;
                END;
            ''')
            
            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS update_instructors_timestamp 
                AFTER UPDATE ON instructors
                BEGIN
                    UPDATE instructors SET updated_at = CURRENT_TIMESTAMP WHERE instructor_id = NEW.instructor_id;
                END;
            ''')
            
            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS update_courses_timestamp 
                AFTER UPDATE ON courses
                BEGIN
                    UPDATE courses SET updated_at = CURRENT_TIMESTAMP WHERE course_id = NEW.course_id;
                END;
            ''')
            
            conn.commit()
    
    def add_student(self, student: Student) -> bool:
        """Add a new student to the database.
        
        Inserts a student record with all validation constraints applied.
        Handles duplicate student ID and email address errors gracefully.
        
        :param student: The student object to add to the database
        :type student: Student
        :return: True if student was added successfully, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO students (student_id, name, age, email)
                    VALUES (?, ?, ?, ?)
                ''', (student.student_id, student.name, student.age, student.get_email()))
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error adding student: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error adding student: {e}")
            return False
    
    def add_instructor(self, instructor: Instructor) -> bool:
        """Add a new instructor to the database.
        
        Inserts an instructor record with all validation constraints applied.
        Handles duplicate instructor ID and email address errors gracefully.
        
        :param instructor: The instructor object to add to the database
        :type instructor: Instructor
        :return: True if instructor was added successfully, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO instructors (instructor_id, name, age, email)
                    VALUES (?, ?, ?, ?)
                ''', (instructor.instructor_id, instructor.name, instructor.age, instructor.get_email()))
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error adding instructor: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error adding instructor: {e}")
            return False
    
    def add_course(self, course: Course) -> bool:
        """Add a new course to the database.
        
        Inserts a course record with optional instructor assignment.
        Validates foreign key relationships and handles constraint violations.
        
        :param course: The course object to add to the database
        :type course: Course
        :return: True if course was added successfully, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                instructor_id = course.instructor.instructor_id if course.instructor else None
                cursor.execute('''
                    INSERT INTO courses (course_id, course_name, instructor_id)
                    VALUES (?, ?, ?)
                ''', (course.course_id, course.course_name, instructor_id))
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error adding course: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error adding course: {e}")
            return False
    
    def register_student_to_course(self, student_id: str, course_id: str) -> bool:
        """Register a student for a course in the database.
        
        Creates a registration record linking a student to a course.
        Prevents duplicate registrations and validates foreign key relationships.
        
        :param student_id: The ID of the student to register
        :type student_id: str
        :param course_id: The ID of the course to register for
        :type course_id: str
        :return: True if registration was successful, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO student_course_registrations (student_id, course_id)
                    VALUES (?, ?)
                ''', (student_id, course_id))
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error registering student to course: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error registering student to course: {e}")
            return False
    
    def get_all_students(self) -> List[Tuple]:
        """Retrieve all students from the database.
        
        :return: List of tuples containing (student_id, name, age, email)
        :rtype: List[Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT student_id, name, age, email FROM students
                ORDER BY name
            ''')
            return cursor.fetchall()
    
    def get_all_instructors(self) -> List[Tuple]:
        """Retrieve all instructors from the database.
        
        :return: List of tuples containing (instructor_id, name, age, email)
        :rtype: List[Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT instructor_id, name, age, email FROM instructors
                ORDER BY name
            ''')
            return cursor.fetchall()
    
    def get_all_courses(self) -> List[Tuple]:
        """Retrieve all courses with instructor information from the database.
        
        :return: List of tuples containing (course_id, course_name, instructor_id, instructor_name)
        :rtype: List[Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.course_id, c.course_name, i.instructor_id, i.name as instructor_name
                FROM courses c
                LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
                ORDER BY c.course_name
            ''')
            return cursor.fetchall()
    
    def get_student_courses(self, student_id: str) -> List[Tuple]:
        """Get all courses registered by a specific student.
        
        :param student_id: The ID of the student
        :type student_id: str
        :return: List of tuples containing (course_id, course_name)
        :rtype: List[Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.course_id, c.course_name
                FROM courses c
                JOIN student_course_registrations scr ON c.course_id = scr.course_id
                WHERE scr.student_id = ?
                ORDER BY c.course_name
            ''', (student_id,))
            return cursor.fetchall()
    
    def get_course_students(self, course_id: str) -> List[Tuple]:
        """Get all students enrolled in a specific course.
        
        :param course_id: The ID of the course
        :type course_id: str
        :return: List of tuples containing (student_id, name)
        :rtype: List[Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT s.student_id, s.name
                FROM students s
                JOIN student_course_registrations scr ON s.student_id = scr.student_id
                WHERE scr.course_id = ?
                ORDER BY s.name
            ''', (course_id,))
            return cursor.fetchall()
    
    def get_instructor_courses(self, instructor_id: str) -> List[Tuple]:
        """Get all courses assigned to a specific instructor.
        
        :param instructor_id: The ID of the instructor
        :type instructor_id: str
        :return: List of tuples containing (course_id, course_name)
        :rtype: List[Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT course_id, course_name
                FROM courses
                WHERE instructor_id = ?
                ORDER BY course_name
            ''', (instructor_id,))
            return cursor.fetchall()
    
    def update_student(self, student_id: str, name: str = None, age: int = None, email: str = None) -> bool:
        """Update student information in the database.
        
        Updates only the specified fields, leaving others unchanged.
        Automatically updates the updated_at timestamp.
        
        :param student_id: The ID of the student to update
        :type student_id: str
        :param name: New name for the student, defaults to None
        :type name: str, optional
        :param age: New age for the student, defaults to None
        :type age: int, optional
        :param email: New email for the student, defaults to None
        :type email: str, optional
        :return: True if update was successful, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                updates = []
                params = []
                
                if name is not None:
                    updates.append("name = ?")
                    params.append(name)
                if age is not None:
                    updates.append("age = ?")
                    params.append(age)
                if email is not None:
                    updates.append("email = ?")
                    params.append(email)
                
                if updates:
                    params.append(student_id)
                    cursor.execute(f'''
                        UPDATE students SET {", ".join(updates)}
                        WHERE student_id = ?
                    ''', params)
                    conn.commit()
                    return cursor.rowcount > 0
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error updating student: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error updating student: {e}")
            return False
    
    def update_instructor(self, instructor_id: str, name: str = None, age: int = None, email: str = None) -> bool:
        """Update instructor information in the database.
        
        Updates only the specified fields, leaving others unchanged.
        Automatically updates the updated_at timestamp.
        
        :param instructor_id: The ID of the instructor to update
        :type instructor_id: str
        :param name: New name for the instructor, defaults to None
        :type name: str, optional
        :param age: New age for the instructor, defaults to None
        :type age: int, optional
        :param email: New email for the instructor, defaults to None
        :type email: str, optional
        :return: True if update was successful, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                updates = []
                params = []
                
                if name is not None:
                    updates.append("name = ?")
                    params.append(name)
                if age is not None:
                    updates.append("age = ?")
                    params.append(age)
                if email is not None:
                    updates.append("email = ?")
                    params.append(email)
                
                if updates:
                    params.append(instructor_id)
                    cursor.execute(f'''
                        UPDATE instructors SET {", ".join(updates)}
                        WHERE instructor_id = ?
                    ''', params)
                    conn.commit()
                    return cursor.rowcount > 0
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error updating instructor: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error updating instructor: {e}")
            return False
    
    def update_course(self, course_id: str, course_name: str = None, instructor_id: str = None) -> bool:
        """Update course information in the database.
        
        Updates only the specified fields, leaving others unchanged.
        Automatically updates the updated_at timestamp.
        
        :param course_id: The ID of the course to update
        :type course_id: str
        :param course_name: New name for the course, defaults to None
        :type course_name: str, optional
        :param instructor_id: New instructor ID for the course, defaults to None
        :type instructor_id: str, optional
        :return: True if update was successful, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                updates = []
                params = []
                
                if course_name is not None:
                    updates.append("course_name = ?")
                    params.append(course_name)
                if instructor_id is not None:
                    updates.append("instructor_id = ?")
                    params.append(instructor_id)
                
                if updates:
                    params.append(course_id)
                    cursor.execute(f'''
                        UPDATE courses SET {", ".join(updates)}
                        WHERE course_id = ?
                    ''', params)
                    conn.commit()
                    return cursor.rowcount > 0
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error updating course: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error updating course: {e}")
            return False
    
    def delete_student(self, student_id: str) -> bool:
        """Delete a student from the database.
        
        Removes the student record and all associated course registrations
        due to CASCADE constraints.
        
        :param student_id: The ID of the student to delete
        :type student_id: str
        :return: True if deletion was successful, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False
    
    def delete_instructor(self, instructor_id: str) -> bool:
        """Delete an instructor from the database.
        
        Removes the instructor record and sets instructor_id to NULL
        in associated courses due to SET NULL constraint.
        
        :param instructor_id: The ID of the instructor to delete
        :type instructor_id: str
        :return: True if deletion was successful, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM instructors WHERE instructor_id = ?", (instructor_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting instructor: {e}")
            return False
    
    def delete_course(self, course_id: str) -> bool:
        """Delete a course from the database.
        
        Removes the course record and all associated student registrations
        due to CASCADE constraints.
        
        :param course_id: The ID of the course to delete
        :type course_id: str
        :return: True if deletion was successful, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting course: {e}")
            return False
    
    def unregister_student_from_course(self, student_id: str, course_id: str) -> bool:
        """Unregister a student from a specific course.
        
        Removes the registration record linking the student to the course.
        
        :param student_id: The ID of the student to unregister
        :type student_id: str
        :param course_id: The ID of the course to unregister from
        :type course_id: str
        :return: True if unregistration was successful, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM student_course_registrations 
                    WHERE student_id = ? AND course_id = ?
                ''', (student_id, course_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error unregistering student from course: {e}")
            return False
    
    def search_students(self, search_term: str) -> List[Tuple]:
        """Search for students by name, ID, or email.
        
        Performs case-insensitive partial matching across all searchable fields.
        
        :param search_term: The term to search for
        :type search_term: str
        :return: List of tuples containing (student_id, name, age, email)
        :rtype: List[Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            search_pattern = f"%{search_term}%"
            cursor.execute('''
                SELECT student_id, name, age, email
                FROM students
                WHERE name LIKE ? OR student_id LIKE ? OR email LIKE ?
                ORDER BY name
            ''', (search_pattern, search_pattern, search_pattern))
            return cursor.fetchall()
    
    def search_instructors(self, search_term: str) -> List[Tuple]:
        """Search for instructors by name, ID, or email.
        
        Performs case-insensitive partial matching across all searchable fields.
        
        :param search_term: The term to search for
        :type search_term: str
        :return: List of tuples containing (instructor_id, name, age, email)
        :rtype: List[Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            search_pattern = f"%{search_term}%"
            cursor.execute('''
                SELECT instructor_id, name, age, email
                FROM instructors
                WHERE name LIKE ? OR instructor_id LIKE ? OR email LIKE ?
                ORDER BY name
            ''', (search_pattern, search_pattern, search_pattern))
            return cursor.fetchall()
    
    def search_courses(self, search_term: str) -> List[Tuple]:
        """Search for courses by name or ID.
        
        Performs case-insensitive partial matching and includes instructor information.
        
        :param search_term: The term to search for
        :type search_term: str
        :return: List of tuples containing (course_id, course_name, instructor_id, instructor_name)
        :rtype: List[Tuple]
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            search_pattern = f"%{search_term}%"
            cursor.execute('''
                SELECT c.course_id, c.course_name, i.instructor_id, i.name as instructor_name
                FROM courses c
                LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
                WHERE c.course_name LIKE ? OR c.course_id LIKE ?
                ORDER BY c.course_name
            ''', (search_pattern, search_pattern))
            return cursor.fetchall()
    
    def load_system_from_db(self) -> SchoolManagementSystem:
        """Load all data from database into a SchoolManagementSystem object.
        
        Reconstructs the complete object hierarchy with all relationships
        between students, instructors, and courses properly established.
        
        :return: A fully populated SchoolManagementSystem object
        :rtype: SchoolManagementSystem
        """
        system = SchoolManagementSystem()
        
        instructors_data = self.get_all_instructors()
        for instructor_id, name, age, email in instructors_data:
            instructor = Instructor(name, age, email, instructor_id)
            system.add_instructor(instructor)
        
        courses_data = self.get_all_courses()
        for course_id, course_name, instructor_id, instructor_name in courses_data:
            instructor = system.find_instructor_by_id(instructor_id) if instructor_id else None
            course = Course(course_id, course_name, instructor)
            system.add_course(course)
            
            if instructor:
                instructor.assign_course(course)
        
        students_data = self.get_all_students()
        for student_id, name, age, email in students_data:
            student = Student(name, age, email, student_id)
            system.add_student(student)
            
            student_courses = self.get_student_courses(student_id)
            for course_id, course_name in student_courses:
                course = system.find_course_by_id(course_id)
                if course:
                    student.register_course(course)
        
        return system
    
    def sync_system_to_db(self, system: SchoolManagementSystem) -> bool:
        """Synchronize a SchoolManagementSystem object to the database.
        
        Completely replaces all database contents with the data from the
        provided system object. This operation is destructive and irreversible.
        
        :param system: The system object to synchronize to the database
        :type system: SchoolManagementSystem
        :return: True if synchronization was successful, False otherwise
        :rtype: bool
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM student_course_registrations")
                cursor.execute("DELETE FROM courses")
                cursor.execute("DELETE FROM instructors")
                cursor.execute("DELETE FROM students")
                
                for student in system.students:
                    cursor.execute('''
                        INSERT INTO students (student_id, name, age, email)
                        VALUES (?, ?, ?, ?)
                    ''', (student.student_id, student.name, student.age, student.get_email()))
                
                for instructor in system.instructors:
                    cursor.execute('''
                        INSERT INTO instructors (instructor_id, name, age, email)
                        VALUES (?, ?, ?, ?)
                    ''', (instructor.instructor_id, instructor.name, instructor.age, instructor.get_email()))
                
                for course in system.courses:
                    instructor_id = course.instructor.instructor_id if course.instructor else None
                    cursor.execute('''
                        INSERT INTO courses (course_id, course_name, instructor_id)
                        VALUES (?, ?, ?)
                    ''', (course.course_id, course.course_name, instructor_id))
                
                for student in system.students:
                    for course in student.registered_courses:
                        cursor.execute('''
                            INSERT INTO student_course_registrations (student_id, course_id)
                            VALUES (?, ?)
                        ''', (student.student_id, course.course_id))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error syncing system to database: {e}")
            return False
    
    def backup_database(self, backup_path: str = None) -> bool:
        """Create a backup copy of the database file.
        
        Creates a timestamped backup copy of the database file for data recovery purposes.
        
        :param backup_path: Path for the backup file, defaults to auto-generated timestamped name
        :type backup_path: str, optional
        :return: True if backup was successful, False otherwise
        :rtype: bool
        """
        try:
            if backup_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"school_management_backup_{timestamp}.db"
            
            shutil.copy2(self.db_path, backup_path)
            print(f"Database backed up to: {backup_path}")
            return True
        except Exception as e:
            print(f"Error backing up database: {e}")
            return False
    
    def get_database_statistics(self) -> dict:
        """Generate comprehensive database statistics.
        
        Provides overview statistics including record counts and popular courses.
        
        :return: Dictionary containing database statistics
        :rtype: dict
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM students")
            student_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM instructors")
            instructor_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM courses")
            course_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM student_course_registrations")
            registration_count = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT c.course_name, COUNT(scr.student_id) as enrollment_count
                FROM courses c
                LEFT JOIN student_course_registrations scr ON c.course_id = scr.course_id
                GROUP BY c.course_id, c.course_name
                ORDER BY enrollment_count DESC
                LIMIT 5
            ''')
            popular_courses = cursor.fetchall()
            
            return {
                'total_students': student_count,
                'total_instructors': instructor_count,
                'total_courses': course_count,
                'total_registrations': registration_count,
                'popular_courses': popular_courses
            }
    
    def export_to_csv(self, table_name: str, output_path: str) -> bool:
        """Export database table to CSV format.
        
        Exports the specified table or view to a CSV file with proper headers.
        Supports exporting students, instructors, courses, and registrations.
        
        :param table_name: Name of the table to export ('students', 'instructors', 'courses', 'registrations')
        :type table_name: str
        :param output_path: Path to the output CSV file
        :type output_path: str
        :return: True if export was successful, False otherwise
        :rtype: bool
        """
        try:
            import csv
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if table_name == 'students':
                    cursor.execute("SELECT * FROM students")
                elif table_name == 'instructors':
                    cursor.execute("SELECT * FROM instructors")
                elif table_name == 'courses':
                    cursor.execute('''
                        SELECT c.*, i.name as instructor_name
                        FROM courses c
                        LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
                    ''')
                elif table_name == 'registrations':
                    cursor.execute('''
                        SELECT scr.*, s.name as student_name, c.course_name
                        FROM student_course_registrations scr
                        JOIN students s ON scr.student_id = s.student_id
                        JOIN courses c ON scr.course_id = c.course_id
                    ''')
                else:
                    return False
                
                data = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]
                
                with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(column_names)
                    writer.writerows(data)
                
                return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
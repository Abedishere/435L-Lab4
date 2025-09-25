import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, 
                             QFileDialog, QFormLayout, QGroupBox, QHeaderView,
                             QAbstractItemView, QTextEdit, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from school_management import SchoolManagementSystem, Student, Instructor, Course
from database_manager import DatabaseManager


class EditRecordDialog(QDialog):
    def __init__(self, record_type, record_data, parent=None):
        super().__init__(parent)
        self.record_type = record_type
        self.record_data = record_data
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Edit {self.record_type}")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        if self.record_type == "Student":
            self.name_edit = QLineEdit(self.record_data.get('name', ''))
            self.age_edit = QLineEdit(str(self.record_data.get('age', '')))
            self.email_edit = QLineEdit(self.record_data.get('email', ''))
            self.id_edit = QLineEdit(self.record_data.get('id', ''))
            self.id_edit.setReadOnly(True)
            
            form_layout.addRow("Name:", self.name_edit)
            form_layout.addRow("Age:", self.age_edit)
            form_layout.addRow("Email:", self.email_edit)
            form_layout.addRow("Student ID:", self.id_edit)
        
        elif self.record_type == "Instructor":
            self.name_edit = QLineEdit(self.record_data.get('name', ''))
            self.age_edit = QLineEdit(str(self.record_data.get('age', '')))
            self.email_edit = QLineEdit(self.record_data.get('email', ''))
            self.id_edit = QLineEdit(self.record_data.get('id', ''))
            self.id_edit.setReadOnly(True)
            
            form_layout.addRow("Name:", self.name_edit)
            form_layout.addRow("Age:", self.age_edit)
            form_layout.addRow("Email:", self.email_edit)
            form_layout.addRow("Instructor ID:", self.id_edit)
        
        elif self.record_type == "Course":
            self.name_edit = QLineEdit(self.record_data.get('name', ''))
            self.id_edit = QLineEdit(self.record_data.get('id', ''))
            self.id_edit.setReadOnly(True)
            
            form_layout.addRow("Course Name:", self.name_edit)
            form_layout.addRow("Course ID:", self.id_edit)
        
        layout.addLayout(form_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_data(self):
        if self.record_type in ["Student", "Instructor"]:
            return {
                'name': self.name_edit.text().strip(),
                'age': int(self.age_edit.text()) if self.age_edit.text().strip() else 0,
                'email': self.email_edit.text().strip(),
                'id': self.id_edit.text().strip()
            }
        elif self.record_type == "Course":
            return {
                'name': self.name_edit.text().strip(),
                'id': self.id_edit.text().strip()
            }


class IntegratedSchoolManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.system = self.db_manager.load_system_from_db()
        self.init_ui()
        self.refresh_displays()
    
    def init_ui(self):
        self.setWindowTitle("School Management System - Database Integrated")
        self.setGeometry(100, 100, 1400, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_registration_tab()
        self.create_display_tab()
        self.create_search_tab()
        self.create_admin_tab()
    
    def create_student_tab(self):
        student_tab = QWidget()
        self.tab_widget.addTab(student_tab, "Students")
        
        layout = QVBoxLayout(student_tab)
        
        title = QLabel("Add Student")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        form_group = QGroupBox("Student Information")
        form_layout = QFormLayout()
        
        self.student_name_edit = QLineEdit()
        self.student_age_edit = QLineEdit()
        self.student_email_edit = QLineEdit()
        self.student_id_edit = QLineEdit()
        
        form_layout.addRow("Name:", self.student_name_edit)
        form_layout.addRow("Age:", self.student_age_edit)
        form_layout.addRow("Email:", self.student_email_edit)
        form_layout.addRow("Student ID:", self.student_id_edit)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        button_layout = QHBoxLayout()
        
        add_student_btn = QPushButton("Add Student")
        add_student_btn.clicked.connect(self.add_student)
        clear_student_btn = QPushButton("Clear")
        clear_student_btn.clicked.connect(self.clear_student_form)
        
        button_layout.addWidget(add_student_btn)
        button_layout.addWidget(clear_student_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def create_instructor_tab(self):
        instructor_tab = QWidget()
        self.tab_widget.addTab(instructor_tab, "Instructors")
        
        layout = QVBoxLayout(instructor_tab)
        
        title = QLabel("Add Instructor")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        form_group = QGroupBox("Instructor Information")
        form_layout = QFormLayout()
        
        self.instructor_name_edit = QLineEdit()
        self.instructor_age_edit = QLineEdit()
        self.instructor_email_edit = QLineEdit()
        self.instructor_id_edit = QLineEdit()
        
        form_layout.addRow("Name:", self.instructor_name_edit)
        form_layout.addRow("Age:", self.instructor_age_edit)
        form_layout.addRow("Email:", self.instructor_email_edit)
        form_layout.addRow("Instructor ID:", self.instructor_id_edit)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        button_layout = QHBoxLayout()
        
        add_instructor_btn = QPushButton("Add Instructor")
        add_instructor_btn.clicked.connect(self.add_instructor)
        clear_instructor_btn = QPushButton("Clear")
        clear_instructor_btn.clicked.connect(self.clear_instructor_form)
        
        button_layout.addWidget(add_instructor_btn)
        button_layout.addWidget(clear_instructor_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def create_course_tab(self):
        course_tab = QWidget()
        self.tab_widget.addTab(course_tab, "Courses")
        
        layout = QVBoxLayout(course_tab)
        
        title = QLabel("Add Course")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        form_group = QGroupBox("Course Information")
        form_layout = QFormLayout()
        
        self.course_id_edit = QLineEdit()
        self.course_name_edit = QLineEdit()
        self.course_instructor_combo = QComboBox()
        
        form_layout.addRow("Course ID:", self.course_id_edit)
        form_layout.addRow("Course Name:", self.course_name_edit)
        form_layout.addRow("Instructor:", self.course_instructor_combo)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        button_layout = QHBoxLayout()
        
        add_course_btn = QPushButton("Add Course")
        add_course_btn.clicked.connect(self.add_course)
        clear_course_btn = QPushButton("Clear")
        clear_course_btn.clicked.connect(self.clear_course_form)
        
        button_layout.addWidget(add_course_btn)
        button_layout.addWidget(clear_course_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def create_registration_tab(self):
        registration_tab = QWidget()
        self.tab_widget.addTab(registration_tab, "Registration")
        
        layout = QVBoxLayout(registration_tab)
        
        student_reg_group = QGroupBox("Student Registration")
        student_reg_layout = QFormLayout()
        
        self.reg_student_combo = QComboBox()
        self.reg_course_combo = QComboBox()
        
        student_reg_layout.addRow("Student:", self.reg_student_combo)
        student_reg_layout.addRow("Course:", self.reg_course_combo)
        
        student_reg_group.setLayout(student_reg_layout)
        layout.addWidget(student_reg_group)
        
        register_btn = QPushButton("Register Student")
        register_btn.clicked.connect(self.register_student)
        layout.addWidget(register_btn)
        
        instructor_assign_group = QGroupBox("Instructor Assignment")
        instructor_assign_layout = QFormLayout()
        
        self.assign_instructor_combo = QComboBox()
        self.assign_course_combo = QComboBox()
        
        instructor_assign_layout.addRow("Instructor:", self.assign_instructor_combo)
        instructor_assign_layout.addRow("Course:", self.assign_course_combo)
        
        instructor_assign_group.setLayout(instructor_assign_layout)
        layout.addWidget(instructor_assign_group)
        
        assign_btn = QPushButton("Assign Instructor")
        assign_btn.clicked.connect(self.assign_instructor)
        layout.addWidget(assign_btn)
        
        layout.addStretch()
    
    def create_display_tab(self):
        display_tab = QWidget()
        self.tab_widget.addTab(display_tab, "Display Records")
        
        layout = QVBoxLayout(display_tab)
        
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_displays)
        save_btn = QPushButton("Save to JSON")
        save_btn.clicked.connect(self.save_to_json)
        load_btn = QPushButton("Load from JSON")
        load_btn.clicked.connect(self.load_from_json)
        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.edit_selected)
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_selected)
        export_csv_btn = QPushButton("Export to CSV")
        export_csv_btn.clicked.connect(self.export_to_csv)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(load_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(export_csv_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.display_tab_widget = QTabWidget()
        layout.addWidget(self.display_tab_widget)
        
        self.create_student_table()
        self.create_instructor_table()
        self.create_course_table()
    
    def create_student_table(self):
        student_widget = QWidget()
        self.display_tab_widget.addTab(student_widget, "Students")
        
        layout = QVBoxLayout(student_widget)
        
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels(["Name", "Age", "Email", "Student ID", "Registered Courses"])
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        layout.addWidget(self.student_table)
    
    def create_instructor_table(self):
        instructor_widget = QWidget()
        self.display_tab_widget.addTab(instructor_widget, "Instructors")
        
        layout = QVBoxLayout(instructor_widget)
        
        self.instructor_table = QTableWidget()
        self.instructor_table.setColumnCount(5)
        self.instructor_table.setHorizontalHeaderLabels(["Name", "Age", "Email", "Instructor ID", "Assigned Courses"])
        self.instructor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.instructor_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        layout.addWidget(self.instructor_table)
    
    def create_course_table(self):
        course_widget = QWidget()
        self.display_tab_widget.addTab(course_widget, "Courses")
        
        layout = QVBoxLayout(course_widget)
        
        self.course_table = QTableWidget()
        self.course_table.setColumnCount(4)
        self.course_table.setHorizontalHeaderLabels(["Course ID", "Course Name", "Instructor", "Enrolled Students"])
        self.course_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.course_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        layout.addWidget(self.course_table)
    
    def create_search_tab(self):
        search_tab = QWidget()
        self.tab_widget.addTab(search_tab, "Search")
        
        layout = QVBoxLayout(search_tab)
        
        title = QLabel("Search Records")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        search_layout = QHBoxLayout()
        
        search_layout.addWidget(QLabel("Search:"))
        self.search_edit = QLineEdit()
        self.search_edit.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_edit)
        
        search_layout.addWidget(QLabel("Filter by:"))
        self.search_filter_combo = QComboBox()
        self.search_filter_combo.addItems(["All", "Students", "Instructors", "Courses"])
        self.search_filter_combo.currentTextChanged.connect(self.on_search)
        search_layout.addWidget(self.search_filter_combo)
        
        search_layout.addStretch()
        
        layout.addLayout(search_layout)
        
        self.search_table = QTableWidget()
        self.search_table.setColumnCount(4)
        self.search_table.setHorizontalHeaderLabels(["Type", "Name", "ID", "Details"])
        self.search_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.search_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        layout.addWidget(self.search_table)
    
    def create_admin_tab(self):
        admin_tab = QWidget()
        self.tab_widget.addTab(admin_tab, "Administration")
        
        layout = QVBoxLayout(admin_tab)
        
        title = QLabel("Database Administration")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        stats_group = QGroupBox("Database Statistics")
        stats_layout = QVBoxLayout()
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(200)
        stats_layout.addWidget(self.stats_text)
        
        refresh_stats_btn = QPushButton("Refresh Statistics")
        refresh_stats_btn.clicked.connect(self.refresh_statistics)
        stats_layout.addWidget(refresh_stats_btn)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        backup_group = QGroupBox("Database Management")
        backup_layout = QHBoxLayout()
        
        backup_btn = QPushButton("Backup Database")
        backup_btn.clicked.connect(self.backup_database)
        export_all_csv_btn = QPushButton("Export All Tables to CSV")
        export_all_csv_btn.clicked.connect(self.export_all_to_csv)
        
        backup_layout.addWidget(backup_btn)
        backup_layout.addWidget(export_all_csv_btn)
        backup_layout.addStretch()
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        layout.addStretch()
        
        self.refresh_statistics()
    
    def add_student(self):
        try:
            name = self.student_name_edit.text().strip()
            age_text = self.student_age_edit.text().strip()
            email = self.student_email_edit.text().strip()
            student_id = self.student_id_edit.text().strip()
            
            if not all([name, age_text, email, student_id]):
                QMessageBox.warning(self, "Error", "Please fill in all fields")
                return
            
            try:
                age = int(age_text)
            except ValueError:
                QMessageBox.warning(self, "Error", "Age must be a valid integer")
                return
            
            student = Student(name, age, email, student_id)
            
            if self.db_manager.add_student(student):
                self.system.add_student(student)
                self.clear_student_form()
                self.refresh_displays()
                QMessageBox.information(self, "Success", "Student added successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to add student. Student ID or email may already exist.")
        
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def add_instructor(self):
        try:
            name = self.instructor_name_edit.text().strip()
            age_text = self.instructor_age_edit.text().strip()
            email = self.instructor_email_edit.text().strip()
            instructor_id = self.instructor_id_edit.text().strip()
            
            if not all([name, age_text, email, instructor_id]):
                QMessageBox.warning(self, "Error", "Please fill in all fields")
                return
            
            try:
                age = int(age_text)
            except ValueError:
                QMessageBox.warning(self, "Error", "Age must be a valid integer")
                return
            
            instructor = Instructor(name, age, email, instructor_id)
            
            if self.db_manager.add_instructor(instructor):
                self.system.add_instructor(instructor)
                self.clear_instructor_form()
                self.refresh_displays()
                QMessageBox.information(self, "Success", "Instructor added successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to add instructor. Instructor ID or email may already exist.")
        
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def add_course(self):
        try:
            course_id = self.course_id_edit.text().strip()
            course_name = self.course_name_edit.text().strip()
            instructor_selection = self.course_instructor_combo.currentText()
            
            if not all([course_id, course_name]):
                QMessageBox.warning(self, "Error", "Please fill in Course ID and Course Name")
                return
            
            instructor = None
            if instructor_selection and instructor_selection != "None":
                instructor_id = instructor_selection.split(" - ")[0]
                instructor = self.system.find_instructor_by_id(instructor_id)
            
            course = Course(course_id, course_name, instructor)
            
            if self.db_manager.add_course(course):
                self.system.add_course(course)
                if instructor:
                    instructor.assign_course(course)
                self.clear_course_form()
                self.refresh_displays()
                QMessageBox.information(self, "Success", "Course added successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to add course. Course ID may already exist.")
        
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def register_student(self):
        try:
            student_selection = self.reg_student_combo.currentText()
            course_selection = self.reg_course_combo.currentText()
            
            if not student_selection or not course_selection:
                QMessageBox.warning(self, "Error", "Please select both student and course")
                return
            
            student_id = student_selection.split(" - ")[0]
            course_id = course_selection.split(" - ")[0]
            
            student = self.system.find_student_by_id(student_id)
            course = self.system.find_course_by_id(course_id)
            
            if not student or not course:
                QMessageBox.warning(self, "Error", "Student or course not found")
                return
            
            if course in student.registered_courses:
                QMessageBox.information(self, "Warning", "Student is already registered for this course")
                return
            
            if self.db_manager.register_student_to_course(student_id, course_id):
                student.register_course(course)
                self.refresh_displays()
                QMessageBox.information(self, "Success", "Student registered successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to register student")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def assign_instructor(self):
        try:
            instructor_selection = self.assign_instructor_combo.currentText()
            course_selection = self.assign_course_combo.currentText()
            
            if not instructor_selection or not course_selection:
                QMessageBox.warning(self, "Error", "Please select both instructor and course")
                return
            
            instructor_id = instructor_selection.split(" - ")[0]
            course_id = course_selection.split(" - ")[0]
            
            instructor = self.system.find_instructor_by_id(instructor_id)
            course = self.system.find_course_by_id(course_id)
            
            if not instructor or not course:
                QMessageBox.warning(self, "Error", "Instructor or course not found")
                return
            
            if course.instructor:
                reply = QMessageBox.question(self, "Confirm", 
                                           f"Course already has instructor {course.instructor.name}. Replace?",
                                           QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return
                if course in course.instructor.assigned_courses:
                    course.instructor.assigned_courses.remove(course)
            
            if self.db_manager.update_course(course_id, instructor_id=instructor_id):
                instructor.assign_course(course)
                self.refresh_displays()
                QMessageBox.information(self, "Success", "Instructor assigned successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to assign instructor")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def refresh_displays(self):
        self.system = self.db_manager.load_system_from_db()
        
        self.student_table.setRowCount(len(self.system.students))
        for i, student in enumerate(self.system.students):
            courses = ", ".join([course.course_name for course in student.registered_courses])
            self.student_table.setItem(i, 0, QTableWidgetItem(student.name))
            self.student_table.setItem(i, 1, QTableWidgetItem(str(student.age)))
            self.student_table.setItem(i, 2, QTableWidgetItem(student.get_email()))
            self.student_table.setItem(i, 3, QTableWidgetItem(student.student_id))
            self.student_table.setItem(i, 4, QTableWidgetItem(courses))
        
        self.instructor_table.setRowCount(len(self.system.instructors))
        for i, instructor in enumerate(self.system.instructors):
            courses = ", ".join([course.course_name for course in instructor.assigned_courses])
            self.instructor_table.setItem(i, 0, QTableWidgetItem(instructor.name))
            self.instructor_table.setItem(i, 1, QTableWidgetItem(str(instructor.age)))
            self.instructor_table.setItem(i, 2, QTableWidgetItem(instructor.get_email()))
            self.instructor_table.setItem(i, 3, QTableWidgetItem(instructor.instructor_id))
            self.instructor_table.setItem(i, 4, QTableWidgetItem(courses))
        
        self.course_table.setRowCount(len(self.system.courses))
        for i, course in enumerate(self.system.courses):
            instructor_name = course.instructor.name if course.instructor else "None"
            students = ", ".join([student.name for student in course.enrolled_students])
            self.course_table.setItem(i, 0, QTableWidgetItem(course.course_id))
            self.course_table.setItem(i, 1, QTableWidgetItem(course.course_name))
            self.course_table.setItem(i, 2, QTableWidgetItem(instructor_name))
            self.course_table.setItem(i, 3, QTableWidgetItem(students))
        
        self.course_instructor_combo.clear()
        self.course_instructor_combo.addItem("None")
        for instructor in self.system.instructors:
            self.course_instructor_combo.addItem(f"{instructor.instructor_id} - {instructor.name}")
        
        self.assign_instructor_combo.clear()
        for instructor in self.system.instructors:
            self.assign_instructor_combo.addItem(f"{instructor.instructor_id} - {instructor.name}")
        
        self.reg_student_combo.clear()
        for student in self.system.students:
            self.reg_student_combo.addItem(f"{student.student_id} - {student.name}")
        
        self.reg_course_combo.clear()
        self.assign_course_combo.clear()
        for course in self.system.courses:
            course_text = f"{course.course_id} - {course.course_name}"
            self.reg_course_combo.addItem(course_text)
            self.assign_course_combo.addItem(course_text)
        
        self.on_search()
    
    def on_search(self):
        self.search_table.setRowCount(0)
        
        search_term = self.search_edit.text().lower()
        filter_type = self.search_filter_combo.currentText()
        
        results = []
        
        if filter_type in ["All", "Students"]:
            for student in self.system.students:
                if (search_term in student.name.lower() or 
                    search_term in student.student_id.lower() or
                    search_term in student.get_email().lower()):
                    courses = ", ".join([course.course_name for course in student.registered_courses])
                    results.append(["Student", student.name, student.student_id, f"Email: {student.get_email()}, Courses: {courses}"])
        
        if filter_type in ["All", "Instructors"]:
            for instructor in self.system.instructors:
                if (search_term in instructor.name.lower() or 
                    search_term in instructor.instructor_id.lower() or
                    search_term in instructor.get_email().lower()):
                    courses = ", ".join([course.course_name for course in instructor.assigned_courses])
                    results.append(["Instructor", instructor.name, instructor.instructor_id, f"Email: {instructor.get_email()}, Courses: {courses}"])
        
        if filter_type in ["All", "Courses"]:
            for course in self.system.courses:
                if (search_term in course.course_name.lower() or 
                    search_term in course.course_id.lower()):
                    instructor_name = course.instructor.name if course.instructor else "None"
                    students = ", ".join([student.name for student in course.enrolled_students])
                    results.append(["Course", course.course_name, course.course_id, f"Instructor: {instructor_name}, Students: {students}"])
        
        self.search_table.setRowCount(len(results))
        for i, result in enumerate(results):
            for j, value in enumerate(result):
                self.search_table.setItem(i, j, QTableWidgetItem(str(value)))
    
    def edit_selected(self):
        current_tab = self.display_tab_widget.currentIndex()
        
        if current_tab == 0:  # Students
            current_row = self.student_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Warning", "Please select a student to edit")
                return
            
            student_data = {
                'name': self.student_table.item(current_row, 0).text(),
                'age': int(self.student_table.item(current_row, 1).text()),
                'email': self.student_table.item(current_row, 2).text(),
                'id': self.student_table.item(current_row, 3).text()
            }
            
            dialog = EditRecordDialog("Student", student_data, self)
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_data()
                if self.db_manager.update_student(student_data['id'], new_data['name'], new_data['age'], new_data['email']):
                    self.refresh_displays()
                    QMessageBox.information(self, "Success", "Student updated successfully")
                else:
                    QMessageBox.warning(self, "Error", "Failed to update student")
        
        elif current_tab == 1:  # Instructors
            current_row = self.instructor_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Warning", "Please select an instructor to edit")
                return
            
            instructor_data = {
                'name': self.instructor_table.item(current_row, 0).text(),
                'age': int(self.instructor_table.item(current_row, 1).text()),
                'email': self.instructor_table.item(current_row, 2).text(),
                'id': self.instructor_table.item(current_row, 3).text()
            }
            
            dialog = EditRecordDialog("Instructor", instructor_data, self)
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_data()
                if self.db_manager.update_instructor(instructor_data['id'], new_data['name'], new_data['age'], new_data['email']):
                    self.refresh_displays()
                    QMessageBox.information(self, "Success", "Instructor updated successfully")
                else:
                    QMessageBox.warning(self, "Error", "Failed to update instructor")
        
        elif current_tab == 2:  # Courses
            current_row = self.course_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Warning", "Please select a course to edit")
                return
            
            course_data = {
                'id': self.course_table.item(current_row, 0).text(),
                'name': self.course_table.item(current_row, 1).text()
            }
            
            dialog = EditRecordDialog("Course", course_data, self)
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_data()
                if self.db_manager.update_course(course_data['id'], new_data['name']):
                    self.refresh_displays()
                    QMessageBox.information(self, "Success", "Course updated successfully")
                else:
                    QMessageBox.warning(self, "Error", "Failed to update course")
    
    def delete_selected(self):
        current_tab = self.display_tab_widget.currentIndex()
        
        if current_tab == 0:  # Students
            current_row = self.student_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Warning", "Please select a student to delete")
                return
            
            student_id = self.student_table.item(current_row, 3).text()
            student_name = self.student_table.item(current_row, 0).text()
            
            reply = QMessageBox.question(self, "Confirm", f"Delete student {student_name}?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.db_manager.delete_student(student_id):
                    self.refresh_displays()
                    QMessageBox.information(self, "Success", "Student deleted successfully")
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete student")
        
        elif current_tab == 1:  # Instructors
            current_row = self.instructor_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Warning", "Please select an instructor to delete")
                return
            
            instructor_id = self.instructor_table.item(current_row, 3).text()
            instructor_name = self.instructor_table.item(current_row, 0).text()
            
            reply = QMessageBox.question(self, "Confirm", f"Delete instructor {instructor_name}?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.db_manager.delete_instructor(instructor_id):
                    self.refresh_displays()
                    QMessageBox.information(self, "Success", "Instructor deleted successfully")
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete instructor")
        
        elif current_tab == 2:  # Courses
            current_row = self.course_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Warning", "Please select a course to delete")
                return
            
            course_id = self.course_table.item(current_row, 0).text()
            course_name = self.course_table.item(current_row, 1).text()
            
            reply = QMessageBox.question(self, "Confirm", f"Delete course {course_name}?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.db_manager.delete_course(course_id):
                    self.refresh_displays()
                    QMessageBox.information(self, "Success", "Course deleted successfully")
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete course")
    
    def save_to_json(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", 
                                                    "JSON files (*.json);;All files (*.*)")
            if filename:
                self.system.save_data(filename)
                QMessageBox.information(self, "Success", "Data saved to JSON successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving data: {str(e)}")
    
    def load_from_json(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Load Data", "", 
                                                    "JSON files (*.json);;All files (*.*)")
            if filename:
                temp_system = SchoolManagementSystem()
                if temp_system.load_data(filename):
                    if self.db_manager.sync_system_to_db(temp_system):
                        self.refresh_displays()
                        QMessageBox.information(self, "Success", "Data loaded from JSON and synced to database successfully")
                    else:
                        QMessageBox.warning(self, "Error", "Failed to sync data to database")
                else:
                    QMessageBox.warning(self, "Error", "Failed to load data from JSON")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading data: {str(e)}")
    
    def export_to_csv(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", 
                                                    "CSV files (*.csv);;All files (*.*)")
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    writer.writerow(["Type", "Name", "Age", "Email", "ID", "Additional Info"])
                    
                    for student in self.system.students:
                        courses = "; ".join([course.course_name for course in student.registered_courses])
                        writer.writerow(["Student", student.name, student.age, student.get_email(), 
                                       student.student_id, f"Courses: {courses}"])
                    
                    for instructor in self.system.instructors:
                        courses = "; ".join([course.course_name for course in instructor.assigned_courses])
                        writer.writerow(["Instructor", instructor.name, instructor.age, instructor.get_email(), 
                                       instructor.instructor_id, f"Courses: {courses}"])
                    
                    for course in self.system.courses:
                        instructor_name = course.instructor.name if course.instructor else "None"
                        students = "; ".join([student.name for student in course.enrolled_students])
                        writer.writerow(["Course", course.course_name, "", "", course.course_id, 
                                       f"Instructor: {instructor_name}, Students: {students}"])
                
                QMessageBox.information(self, "Success", "Data exported to CSV successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting data: {str(e)}")
    
    def export_all_to_csv(self):
        try:
            folder = QFileDialog.getExistingDirectory(self, "Select Folder for CSV Export")
            if folder:
                tables = ['students', 'instructors', 'courses', 'registrations']
                for table in tables:
                    output_path = f"{folder}/{table}.csv"
                    self.db_manager.export_to_csv(table, output_path)
                
                QMessageBox.information(self, "Success", "All tables exported to CSV successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting tables: {str(e)}")
    
    def backup_database(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Backup Database", "", 
                                                    "Database files (*.db);;All files (*.*)")
            if filename:
                if self.db_manager.backup_database(filename):
                    QMessageBox.information(self, "Success", "Database backed up successfully")
                else:
                    QMessageBox.warning(self, "Error", "Failed to backup database")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error backing up database: {str(e)}")
    
    def refresh_statistics(self):
        try:
            stats = self.db_manager.get_database_statistics()
            
            stats_text = f"""Database Statistics:

Total Students: {stats['total_students']}
Total Instructors: {stats['total_instructors']}
Total Courses: {stats['total_courses']}
Total Registrations: {stats['total_registrations']}

Top 5 Popular Courses:
"""
            
            for i, (course_name, enrollment) in enumerate(stats['popular_courses'], 1):
                stats_text += f"{i}. {course_name}: {enrollment} students\n"
            
            self.stats_text.setText(stats_text)
        except Exception as e:
            self.stats_text.setText(f"Error loading statistics: {str(e)}")
    
    def clear_student_form(self):
        self.student_name_edit.clear()
        self.student_age_edit.clear()
        self.student_email_edit.clear()
        self.student_id_edit.clear()
    
    def clear_instructor_form(self):
        self.instructor_name_edit.clear()
        self.instructor_age_edit.clear()
        self.instructor_email_edit.clear()
        self.instructor_id_edit.clear()
    
    def clear_course_form(self):
        self.course_id_edit.clear()
        self.course_name_edit.clear()
        self.course_instructor_combo.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)
    window = IntegratedSchoolManagement()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
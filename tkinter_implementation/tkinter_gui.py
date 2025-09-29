import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from school_management import SchoolManagementSystem, Student, Instructor, Course


class SchoolManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("1000x700")
        
        self.system = SchoolManagementSystem()
        
        self.create_widgets()
        
        try:
            self.system.load_data("school_data.json")
            self.refresh_displays()
        except:
            pass
    
    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pifthinack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_student_tab(notebook)
        self.create_instructor_tab(notebook)
        self.create_course_tab(notebook)
        self.create_registration_tab(notebook)
        self.create_display_tab(notebook)
        self.create_search_tab(notebook)
    
    def create_student_tab(self, notebook):
        student_frame = ttk.Frame(notebook)
        notebook.add(student_frame, text="Students")
        
        ttk.Label(student_frame, text="Add Student", font=("Arial", 16, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(student_frame)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.student_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.student_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.student_age_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.student_age_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.student_email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.student_email_var, width=30).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Student ID:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.student_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.student_id_var, width=30).grid(row=3, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(student_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_student_form).pack(side="left", padx=5)
    
    def create_instructor_tab(self, notebook):
        instructor_frame = ttk.Frame(notebook)
        notebook.add(instructor_frame, text="Instructors")
        
        ttk.Label(instructor_frame, text="Add Instructor", font=("Arial", 16, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(instructor_frame)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.instructor_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.instructor_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.instructor_age_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.instructor_age_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.instructor_email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.instructor_email_var, width=30).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Instructor ID:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.instructor_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.instructor_id_var, width=30).grid(row=3, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(instructor_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Instructor", command=self.add_instructor).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_instructor_form).pack(side="left", padx=5)
    
    def create_course_tab(self, notebook):
        course_frame = ttk.Frame(notebook)
        notebook.add(course_frame, text="Courses")
        
        ttk.Label(course_frame, text="Add Course", font=("Arial", 16, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(course_frame)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Course ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.course_id_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.course_id_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Course Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.course_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.course_name_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Instructor:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.course_instructor_var = tk.StringVar()
        self.instructor_combobox = ttk.Combobox(form_frame, textvariable=self.course_instructor_var, width=28, state="readonly")
        self.instructor_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(course_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Course", command=self.add_course).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_course_form).pack(side="left", padx=5)
    
    def create_registration_tab(self, notebook):
        registration_frame = ttk.Frame(notebook)
        notebook.add(registration_frame, text="Registration")
        
        ttk.Label(registration_frame, text="Student Registration", font=("Arial", 16, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(registration_frame)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Student:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.reg_student_var = tk.StringVar()
        self.student_combobox = ttk.Combobox(form_frame, textvariable=self.reg_student_var, width=28, state="readonly")
        self.student_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Course:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.reg_course_var = tk.StringVar()
        self.course_combobox = ttk.Combobox(form_frame, textvariable=self.reg_course_var, width=28, state="readonly")
        self.course_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(registration_frame, text="Register Student", command=self.register_student).pack(pady=10)
        
        ttk.Separator(registration_frame, orient="horizontal").pack(fill="x", pady=20)
        
        ttk.Label(registration_frame, text="Instructor Assignment", font=("Arial", 16, "bold")).pack(pady=10)
        
        assign_frame = ttk.Frame(registration_frame)
        assign_frame.pack(pady=10)
        
        ttk.Label(assign_frame, text="Instructor:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.assign_instructor_var = tk.StringVar()
        self.assign_instructor_combobox = ttk.Combobox(assign_frame, textvariable=self.assign_instructor_var, width=28, state="readonly")
        self.assign_instructor_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(assign_frame, text="Course:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.assign_course_var = tk.StringVar()
        self.assign_course_combobox = ttk.Combobox(assign_frame, textvariable=self.assign_course_var, width=28, state="readonly")
        self.assign_course_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(registration_frame, text="Assign Instructor", command=self.assign_instructor).pack(pady=10)
    
    def create_display_tab(self, notebook):
        display_frame = ttk.Frame(notebook)
        notebook.add(display_frame, text="Display Records")
        
        button_frame = ttk.Frame(display_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Refresh", command=self.refresh_displays).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save Data", command=self.save_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Load Data", command=self.load_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=5)
        
        self.display_notebook = ttk.Notebook(display_frame)
        self.display_notebook.pack(fill="both", expand=True, pady=10)
        
        self.create_student_display()
        self.create_instructor_display()
        self.create_course_display()
    
    def create_student_display(self):
        student_display_frame = ttk.Frame(self.display_notebook)
        self.display_notebook.add(student_display_frame, text="Students")
        
        self.student_tree = ttk.Treeview(student_display_frame, columns=("Name", "Age", "Email", "ID", "Courses"), show="headings")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Age", text="Age")
        self.student_tree.heading("Email", text="Email")
        self.student_tree.heading("ID", text="Student ID")
        self.student_tree.heading("Courses", text="Registered Courses")
        
        self.student_tree.column("Name", width=150)
        self.student_tree.column("Age", width=50)
        self.student_tree.column("Email", width=200)
        self.student_tree.column("ID", width=100)
        self.student_tree.column("Courses", width=300)
        
        scrollbar_student = ttk.Scrollbar(student_display_frame, orient="vertical", command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar_student.set)
        
        self.student_tree.pack(side="left", fill="both", expand=True)
        scrollbar_student.pack(side="right", fill="y")
    
    def create_instructor_display(self):
        instructor_display_frame = ttk.Frame(self.display_notebook)
        self.display_notebook.add(instructor_display_frame, text="Instructors")
        
        self.instructor_tree = ttk.Treeview(instructor_display_frame, columns=("Name", "Age", "Email", "ID", "Courses"), show="headings")
        self.instructor_tree.heading("Name", text="Name")
        self.instructor_tree.heading("Age", text="Age")
        self.instructor_tree.heading("Email", text="Email")
        self.instructor_tree.heading("ID", text="Instructor ID")
        self.instructor_tree.heading("Courses", text="Assigned Courses")
        
        self.instructor_tree.column("Name", width=150)
        self.instructor_tree.column("Age", width=50)
        self.instructor_tree.column("Email", width=200)
        self.instructor_tree.column("ID", width=100)
        self.instructor_tree.column("Courses", width=300)
        
        scrollbar_instructor = ttk.Scrollbar(instructor_display_frame, orient="vertical", command=self.instructor_tree.yview)
        self.instructor_tree.configure(yscrollcommand=scrollbar_instructor.set)
        
        self.instructor_tree.pack(side="left", fill="both", expand=True)
        scrollbar_instructor.pack(side="right", fill="y")
    
    def create_course_display(self):
        course_display_frame = ttk.Frame(self.display_notebook)
        self.display_notebook.add(course_display_frame, text="Courses")
        
        self.course_tree = ttk.Treeview(course_display_frame, columns=("ID", "Name", "Instructor", "Students"), show="headings")
        self.course_tree.heading("ID", text="Course ID")
        self.course_tree.heading("Name", text="Course Name")
        self.course_tree.heading("Instructor", text="Instructor")
        self.course_tree.heading("Students", text="Enrolled Students")
        
        self.course_tree.column("ID", width=100)
        self.course_tree.column("Name", width=200)
        self.course_tree.column("Instructor", width=150)
        self.course_tree.column("Students", width=350)
        
        scrollbar_course = ttk.Scrollbar(course_display_frame, orient="vertical", command=self.course_tree.yview)
        self.course_tree.configure(yscrollcommand=scrollbar_course.set)
        
        self.course_tree.pack(side="left", fill="both", expand=True)
        scrollbar_course.pack(side="right", fill="y")
    
    def create_search_tab(self, notebook):
        search_frame = ttk.Frame(notebook)
        notebook.add(search_frame, text="Search")
        
        ttk.Label(search_frame, text="Search Records", font=("Arial", 16, "bold")).pack(pady=10)
        
        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(pady=10)
        
        ttk.Label(search_input_frame, text="Search:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_input_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Label(search_input_frame, text="Filter by:").pack(side="left", padx=5)
        self.search_filter_var = tk.StringVar(value="All")
        filter_combobox = ttk.Combobox(search_input_frame, textvariable=self.search_filter_var, 
                                     values=["All", "Students", "Instructors", "Courses"], 
                                     state="readonly", width=15)
        filter_combobox.pack(side="left", padx=5)
        filter_combobox.bind('<<ComboboxSelected>>', self.on_search)
        
        self.search_tree = ttk.Treeview(search_frame, columns=("Type", "Name", "ID", "Details"), show="headings")
        self.search_tree.heading("Type", text="Type")
        self.search_tree.heading("Name", text="Name")
        self.search_tree.heading("ID", text="ID")
        self.search_tree.heading("Details", text="Details")
        
        self.search_tree.column("Type", width=100)
        self.search_tree.column("Name", width=200)
        self.search_tree.column("ID", width=150)
        self.search_tree.column("Details", width=400)
        
        scrollbar_search = ttk.Scrollbar(search_frame, orient="vertical", command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar_search.set)
        
        self.search_tree.pack(side="left", fill="both", expand=True, pady=10)
        scrollbar_search.pack(side="right", fill="y", pady=10)
    
    def add_student(self):
        try:
            name = self.student_name_var.get().strip()
            age = int(self.student_age_var.get())
            email = self.student_email_var.get().strip()
            student_id = self.student_id_var.get().strip()
            
            if not all([name, email, student_id]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if self.system.find_student_by_id(student_id):
                messagebox.showerror("Error", "Student ID already exists")
                return
            
            student = Student(name, age, email, student_id)
            self.system.add_student(student)
            
            self.clear_student_form()
            self.refresh_displays()
            self.auto_save()
            messagebox.showinfo("Success", "Student added successfully")
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def add_instructor(self):
        try:
            name = self.instructor_name_var.get().strip()
            age = int(self.instructor_age_var.get())
            email = self.instructor_email_var.get().strip()
            instructor_id = self.instructor_id_var.get().strip()
            
            if not all([name, email, instructor_id]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if self.system.find_instructor_by_id(instructor_id):
                messagebox.showerror("Error", "Instructor ID already exists")
                return
            
            instructor = Instructor(name, age, email, instructor_id)
            self.system.add_instructor(instructor)
            
            self.clear_instructor_form()
            self.refresh_displays()
            self.auto_save()
            messagebox.showinfo("Success", "Instructor added successfully")
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def add_course(self):
        try:
            course_id = self.course_id_var.get().strip()
            course_name = self.course_name_var.get().strip()
            instructor_selection = self.course_instructor_var.get()
            
            if not all([course_id, course_name]):
                messagebox.showerror("Error", "Please fill in Course ID and Course Name")
                return
            
            if self.system.find_course_by_id(course_id):
                messagebox.showerror("Error", "Course ID already exists")
                return
            
            instructor = None
            if instructor_selection and instructor_selection != "None":
                instructor_id = instructor_selection.split(" - ")[0]
                instructor = self.system.find_instructor_by_id(instructor_id)
            
            course = Course(course_id, course_name, instructor)
            self.system.add_course(course)
            
            if instructor:
                instructor.assign_course(course)
            
            self.clear_course_form()
            self.refresh_displays()
            self.auto_save()
            messagebox.showinfo("Success", "Course added successfully")
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def register_student(self):
        try:
            student_selection = self.reg_student_var.get()
            course_selection = self.reg_course_var.get()
            
            if not student_selection or not course_selection:
                messagebox.showerror("Error", "Please select both student and course")
                return
            
            student_id = student_selection.split(" - ")[0]
            course_id = course_selection.split(" - ")[0]
            
            student = self.system.find_student_by_id(student_id)
            course = self.system.find_course_by_id(course_id)
            
            if not student or not course:
                messagebox.showerror("Error", "Student or course not found")
                return
            
            if course in student.registered_courses:
                messagebox.showwarning("Warning", "Student is already registered for this course")
                return
            
            student.register_course(course)
            self.refresh_displays()
            self.auto_save()
            messagebox.showinfo("Success", "Student registered successfully")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def assign_instructor(self):
        try:
            instructor_selection = self.assign_instructor_var.get()
            course_selection = self.assign_course_var.get()
            
            if not instructor_selection or not course_selection:
                messagebox.showerror("Error", "Please select both instructor and course")
                return
            
            instructor_id = instructor_selection.split(" - ")[0]
            course_id = course_selection.split(" - ")[0]
            
            instructor = self.system.find_instructor_by_id(instructor_id)
            course = self.system.find_course_by_id(course_id)
            
            if not instructor or not course:
                messagebox.showerror("Error", "Instructor or course not found")
                return
            
            if course.instructor:
                result = messagebox.askyesno("Confirm", f"Course already has instructor {course.instructor.name}. Replace?")
                if not result:
                    return
                if course in course.instructor.assigned_courses:
                    course.instructor.assigned_courses.remove(course)
            
            instructor.assign_course(course)
            self.refresh_displays()
            self.auto_save()
            messagebox.showinfo("Success", "Instructor assigned successfully")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def refresh_displays(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for item in self.instructor_tree.get_children():
            self.instructor_tree.delete(item)
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        for student in self.system.students:
            courses = ", ".join([course.course_name for course in student.registered_courses])
            self.student_tree.insert("", "end", values=(student.name, student.age, student.get_email(), student.student_id, courses))
        
        for instructor in self.system.instructors:
            courses = ", ".join([course.course_name for course in instructor.assigned_courses])
            self.instructor_tree.insert("", "end", values=(instructor.name, instructor.age, instructor.get_email(), instructor.instructor_id, courses))
        
        for course in self.system.courses:
            instructor_name = course.instructor.name if course.instructor else "None"
            students = ", ".join([student.name for student in course.enrolled_students])
            self.course_tree.insert("", "end", values=(course.course_id, course.course_name, instructor_name, students))
        
        instructor_options = ["None"] + [f"{instructor.instructor_id} - {instructor.name}" for instructor in self.system.instructors]
        self.instructor_combobox['values'] = instructor_options
        self.assign_instructor_combobox['values'] = [f"{instructor.instructor_id} - {instructor.name}" for instructor in self.system.instructors]
        
        student_options = [f"{student.student_id} - {student.name}" for student in self.system.students]
        self.student_combobox['values'] = student_options
        
        course_options = [f"{course.course_id} - {course.course_name}" for course in self.system.courses]
        self.course_combobox['values'] = course_options
        self.assign_course_combobox['values'] = course_options
        
        self.on_search()
    
    def on_search(self, event=None):
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        search_term = self.search_var.get().lower()
        filter_type = self.search_filter_var.get()
        
        if filter_type in ["All", "Students"]:
            for student in self.system.students:
                if (search_term in student.name.lower() or 
                    search_term in student.student_id.lower() or
                    search_term in student.get_email().lower()):
                    courses = ", ".join([course.course_name for course in student.registered_courses])
                    self.search_tree.insert("", "end", values=("Student", student.name, student.student_id, f"Email: {student.get_email()}, Courses: {courses}"))
        
        if filter_type in ["All", "Instructors"]:
            for instructor in self.system.instructors:
                if (search_term in instructor.name.lower() or 
                    search_term in instructor.instructor_id.lower() or
                    search_term in instructor.get_email().lower()):
                    courses = ", ".join([course.course_name for course in instructor.assigned_courses])
                    self.search_tree.insert("", "end", values=("Instructor", instructor.name, instructor.instructor_id, f"Email: {instructor.get_email()}, Courses: {courses}"))
        
        if filter_type in ["All", "Courses"]:
            for course in self.system.courses:
                if (search_term in course.course_name.lower() or 
                    search_term in course.course_id.lower()):
                    instructor_name = course.instructor.name if course.instructor else "None"
                    students = ", ".join([student.name for student in course.enrolled_students])
                    self.search_tree.insert("", "end", values=("Course", course.course_name, course.course_id, f"Instructor: {instructor_name}, Students: {students}"))
    
    def delete_selected(self):
        current_tab = self.display_notebook.tab(self.display_notebook.select(), "text")
        
        if current_tab == "Students":
            selection = self.student_tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a student to delete")
                return
            
            student_data = self.student_tree.item(selection[0])['values']
            student_id = student_data[3]
            
            result = messagebox.askyesno("Confirm", f"Delete student {student_data[0]}?")
            if result:
                self.system.remove_student(student_id)
                self.refresh_displays()
                self.auto_save()
                messagebox.showinfo("Success", "Student deleted successfully")
        
        elif current_tab == "Instructors":
            selection = self.instructor_tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select an instructor to delete")
                return
            
            instructor_data = self.instructor_tree.item(selection[0])['values']
            instructor_id = instructor_data[3]
            
            result = messagebox.askyesno("Confirm", f"Delete instructor {instructor_data[0]}?")
            if result:
                self.system.remove_instructor(instructor_id)
                self.refresh_displays()
                self.auto_save()
                messagebox.showinfo("Success", "Instructor deleted successfully")
        
        elif current_tab == "Courses":
            selection = self.course_tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a course to delete")
                return
            
            course_data = self.course_tree.item(selection[0])['values']
            course_id = course_data[0]
            
            result = messagebox.askyesno("Confirm", f"Delete course {course_data[1]}?")
            if result:
                self.system.remove_course(course_id)
                self.refresh_displays()
                self.auto_save()
                messagebox.showinfo("Success", "Course deleted successfully")
    
    def save_data(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.system.save_data(filename)
                messagebox.showinfo("Success", "Data saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")
    
    def load_data(self):
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                if self.system.load_data(filename):
                    self.refresh_displays()
                    messagebox.showinfo("Success", "Data loaded successfully")
                else:
                    messagebox.showerror("Error", "Failed to load data")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
    
    def clear_student_form(self):
        self.student_name_var.set("")
        self.student_age_var.set("")
        self.student_email_var.set("")
        self.student_id_var.set("")
    
    def clear_instructor_form(self):
        self.instructor_name_var.set("")
        self.instructor_age_var.set("")
        self.instructor_email_var.set("")
        self.instructor_id_var.set("")
    
    def clear_course_form(self):
        self.course_id_var.set("")
        self.course_name_var.set("")
        self.course_instructor_var.set("")
    
    def auto_save(self):
        try:
            self.system.save_data("school_data.json")
        except Exception as e:
            print(f"Auto-save failed: {e}")


def main():
    root = tk.Tk()
    app = SchoolManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
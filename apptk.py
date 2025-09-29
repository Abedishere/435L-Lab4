"""
Tk/ttk GUI for the School Manager app.

Three tabs:
- Add   (create students, instructors, courses; register/assign)
- View  (three tables + delete + CSV export)
- Search (live filter across all data)

Uses SchoolStore for persistence (JSON) and export (CSV).
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from school import Student, Instructor, Course
from store import SchoolStore


class TkApp(ttk.Frame):
    """Main Tk application placed inside a root window."""

    def __init__(self, master: tk.Tk):
        super().__init__(master)
        master.title("School Manager (Tk)")
        master.geometry("950x600")
        self.pack(fill="both", expand=True)

        # data access
        self.store = SchoolStore()
        self.sys = self.store.system

        # notebook with three pages
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)
        self.pg_add = ttk.Frame(self.tabs)
        self.pg_view = ttk.Frame(self.tabs)
        self.pg_find = ttk.Frame(self.tabs)
        self.tabs.add(self.pg_add, text="Add")
        self.tabs.add(self.pg_view, text="View")
        self.tabs.add(self.pg_find, text="Search")

        # build UI
        self._build_add()
        self._build_view()
        self._build_find()

        # initial data fill
        self.refresh()

    # ---------- UI: Add ----------
    def _build_add(self) -> None:
        outer = ttk.Frame(self.pg_add)
        outer.pack(fill="both", expand=True)
        inner = ttk.Frame(outer)
        inner.place(relx=.5, rely=.02, anchor="n")

        def box(title: str) -> ttk.Labelframe:
            f = ttk.Labelframe(inner, text=title)
            f.pack(pady=6, ipadx=10, ipady=6, fill="x")
            return f

        # student form
        bs = box("Add Student")
        self.sname = ttk.Entry(bs, width=40)
        self.sage = ttk.Entry(bs, width=12)
        self.semail = ttk.Entry(bs, width=40)
        self.sid = ttk.Entry(bs, width=20)
        for i, (lbl, w) in enumerate((
            ("Name", self.sname), ("Age", self.sage),
            ("Email", self.semail), ("ID", self.sid)
        )):
            ttk.Label(bs, text=lbl).grid(row=i, column=0, sticky="e", padx=6, pady=3)
            w.grid(row=i, column=1, sticky="w", padx=6, pady=3)
        ttk.Button(bs, text="Add Student", command=self.addstudent)\
           .grid(row=4, column=0, columnspan=2, pady=6)

        # instructor form
        bi = box("Add Instructor")
        self.iname = ttk.Entry(bi, width=40)
        self.iage = ttk.Entry(bi, width=12)
        self.iemail = ttk.Entry(bi, width=40)
        self.iid = ttk.Entry(bi, width=20)
        for i, (lbl, w) in enumerate((
            ("Name", self.iname), ("Age", self.iage),
            ("Email", self.iemail), ("ID", self.iid)
        )):
            ttk.Label(bi, text=lbl).grid(row=i, column=0, sticky="e", padx=6, pady=3)
            w.grid(row=i, column=1, sticky="w", padx=6, pady=3)
        ttk.Button(bi, text="Add Instructor", command=self.addinstructor)\
           .grid(row=4, column=0, columnspan=2, pady=6)

        # course form
        bc = box("Add Course")
        self.cid = ttk.Entry(bc, width=20)
        self.cname = ttk.Entry(bc, width=40)
        self.cinst = ttk.Combobox(bc, width=40, state="readonly")
        for i, (lbl, w) in enumerate((
            ("Course ID", self.cid), ("Course Name", self.cname),
            ("Instructor", self.cinst)
        )):
            ttk.Label(bc, text=lbl).grid(row=i, column=0, sticky="e", padx=6, pady=3)
            w.grid(row=i, column=1, sticky="w", padx=6, pady=3)
        ttk.Button(bc, text="Add Course", command=self.addcourse)\
           .grid(row=3, column=0, columnspan=2, pady=6)

        # register student to course
        br = box("Register Student to Course")
        self.rsid = ttk.Combobox(br, width=40, state="readonly")
        self.rcid = ttk.Combobox(br, width=40, state="readonly")
        ttk.Label(br, text="Student").grid(row=0, column=0, sticky="e", padx=6, pady=3)
        self.rsid.grid(row=0, column=1, sticky="w", padx=6, pady=3)
        ttk.Label(br, text="Course").grid(row=1, column=0, sticky="e", padx=6, pady=3)
        self.rcid.grid(row=1, column=1, sticky="w", padx=6, pady=3)
        ttk.Button(br, text="Register", command=self.register)\
           .grid(row=2, column=0, columnspan=2, pady=6)

        # assign instructor to course
        ba = box("Assign Instructor to Course")
        self.aiid = ttk.Combobox(ba, width=40, state="readonly")
        self.acid = ttk.Combobox(ba, width=40, state="readonly")
        ttk.Label(ba, text="Instructor").grid(row=0, column=0, sticky="e", padx=6, pady=3)
        self.aiid.grid(row=0, column=1, sticky="w", padx=6, pady=3)
        ttk.Label(ba, text="Course").grid(row=1, column=0, sticky="e", padx=6, pady=3)
        self.acid.grid(row=1, column=1, sticky="w", padx=6, pady=3)
        ttk.Button(ba, text="Assign", command=self.assign)\
           .grid(row=2, column=0, columnspan=2, pady=6)

    # ---------- UI: View ----------
    def _build_view(self) -> None:
        v = ttk.Frame(self.pg_view)
        v.pack(fill="both", expand=True)

        row = ttk.Frame(v)
        row.pack(fill="x", pady=6)
        ttk.Button(row, text="Export CSV", command=self.exportcsv)\
           .pack(side="left", padx=6)
        ttk.Button(row, text="Delete Selected", command=self.deleteselected)\
           .pack(side="left", padx=6)

        self.viewtabs = ttk.Notebook(v)
        self.viewtabs.pack(fill="both", expand=True)

        def tree(cols: tuple[str, ...], heads: list[str]) -> ttk.Treeview:
            t = ttk.Treeview(self.viewtabs, columns=cols, show="headings", selectmode="browse")
            for c, h in zip(cols, heads):
                t.heading(c, text=h)
                t.column(c, anchor="w", width=180)
            ys = ttk.Scrollbar(t, orient="vertical", command=t.yview)
            t.configure(yscroll=ys.set)
            ys.pack(side="right", fill="y")
            return t

        self.t_students = tree(("name", "age", "email", "id", "courses"),
                               ["Name", "Age", "Email", "ID", "Courses"])
        self.t_insts = tree(("name", "age", "email", "id", "courses"),
                            ["Name", "Age", "Email", "ID", "Courses"])
        self.t_courses = tree(("cid", "cname", "inst", "students"),
                              ["Course ID", "Course Name", "Instructor", "Students"])

        self.viewtabs.add(self.t_students, text="Students")
        self.viewtabs.add(self.t_insts, text="Instructors")
        self.viewtabs.add(self.t_courses, text="Courses")

    # ---------- UI: Search ----------
    def _build_find(self) -> None:
        v = ttk.Frame(self.pg_find)
        v.pack(fill="both", expand=True)

        top = ttk.Frame(v)
        top.pack(pady=8)
        ttk.Label(top, text="Search").pack(side="left", padx=6)
        self.q = ttk.Entry(top, width=50)
        self.q.pack(side="left")
        self.q.bind("<KeyRelease>", lambda e: self.dosearch())

        cols = ("typ", "name", "code", "info")
        self.t_search = ttk.Treeview(v, columns=cols, show="headings", selectmode="browse")
        for c, h in zip(cols, ["Type", "Name", "ID", "Details"]):
            self.t_search.heading(c, text=h)
            self.t_search.column(c, anchor="w", width=200)
        ys = ttk.Scrollbar(self.t_search, orient="vertical", command=self.t_search.yview)
        self.t_search.configure(yscroll=ys.set)
        ys.pack(side="right", fill="y")
        self.t_search.pack(fill="both", expand=True, padx=6, pady=6)

    # ---------- actions ----------
    def addstudent(self) -> None:
        """Create a student from the form and persist."""
        try:
            s = Student(self.sname.get(), int(self.sage.get()), self.semail.get(), self.sid.get())
            if not self.store.addstudent(s):
                messagebox.showwarning("Note", "Student ID already exists")
                return
            for w in (self.sname, self.sage, self.semail, self.sid):
                w.delete(0, "end")
            self.refresh()
            messagebox.showinfo("OK", "Student added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def addinstructor(self) -> None:
        """Create an instructor from the form and persist."""
        try:
            i = Instructor(self.iname.get(), int(self.iage.get()), self.iemail.get(), self.iid.get())
            if not self.store.addinstructor(i):
                messagebox.showwarning("Note", "Instructor ID already exists")
                return
            for w in (self.iname, self.iage, self.iemail, self.iid):
                w.delete(0, "end")
            self.refresh()
            messagebox.showinfo("OK", "Instructor added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def addcourse(self) -> None:
        """Create a course; optionally link the selected instructor."""
        try:
            instid = self.cinst.get().split(" - ")[0] if self.cinst.get() else ""
            inst = self.sys.findinstructor(instid) if instid else None
            c = Course(self.cid.get(), self.cname.get(), inst)
            if not self.store.addcourse(c):
                messagebox.showwarning("Note", "Course ID already exists")
                return
            if inst:
                inst.take(c)
                self.store.save()  # keep both sides in JSON
            self.cid.delete(0, "end")
            self.cname.delete(0, "end")
            self.cinst.set("")
            self.refresh()
            messagebox.showinfo("OK", "Course added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def register(self) -> None:
        """Enroll the selected student in the selected course."""
        if not self.rsid.get() or not self.rcid.get():
            messagebox.showwarning("Note", "Pick student and course")
            return
        ok = self.store.joincourse(self.rsid.get().split(" - ")[0],
                                   self.rcid.get().split(" - ")[0])
        if not ok:
            messagebox.showinfo("Note", "Already registered or not found")
        self.refresh()

    def assign(self) -> None:
        """Assign the selected instructor to the selected course."""
        if not self.aiid.get() or not self.acid.get():
            messagebox.showwarning("Note", "Pick instructor and course")
            return
        ok = self.store.assigncourse(self.aiid.get().split(" - ")[0],
                                     self.acid.get().split(" - ")[0])
        if not ok:
            messagebox.showinfo("Note", "Already assigned or not found")
        self.refresh()

    def exportcsv(self) -> None:
        """Open a save dialog and write the CSV via the store."""
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return
        self.store.exportcsv(path)
        messagebox.showinfo("OK", "Exported")

    def deleteselected(self) -> None:
        """Delete the selected row from the active table."""
        tab = self.viewtabs.index(self.viewtabs.select())
        if tab == 0:
            sel = self.t_students.selection()
            if sel:
                sid = self.t_students.item(sel[0])["values"][3]
                if self.store.removestudent(sid):
                    self.refresh()
        elif tab == 1:
            sel = self.t_insts.selection()
            if sel:
                iid = self.t_insts.item(sel[0])["values"][3]
                if self.store.removeinstructor(iid):
                    self.refresh()
        else:
            sel = self.t_courses.selection()
            if sel:
                cid = self.t_courses.item(sel[0])["values"][0]
                if self.store.removecourse(cid):
                    self.refresh()

    def refresh(self) -> None:
        """Refill form combos and tables then run a search refresh."""
        # combos
        self.cinst["values"] = [""] + [f"{i.instructorid} - {i.name}" for i in self.sys.instructors]
        self.rsid["values"] = [f"{s.studentid} - {s.name}" for s in self.sys.students]
        self.rcid["values"] = [f"{c.courseid} - {c.coursename}" for c in self.sys.courses]
        self.aiid["values"] = [f"{i.instructorid} - {i.name}" for i in self.sys.instructors]
        self.acid["values"] = [f"{c.courseid} - {c.coursename}" for c in self.sys.courses]

        # tables
        def fill(tree: ttk.Treeview, rows: list[list[str]]) -> None:
            for iid in tree.get_children():
                tree.delete(iid)
            for r in rows:
                tree.insert("", "end", values=r)

        fill(self.t_students, [
            [s.name, s.age, s.email, s.studentid,
             ", ".join(c.coursename for c in s.courses)]
            for s in self.sys.students
        ])
        fill(self.t_insts, [
            [i.name, i.age, i.email, i.instructorid,
             ", ".join(c.coursename for c in i.courses)]
            for i in self.sys.instructors
        ])
        fill(self.t_courses, [
            [c.courseid, c.coursename,
             (c.instructor.name if c.instructor else "None"),
             ", ".join(s.name for s in c.students)]
            for c in self.sys.courses
        ])

        # search page refresh
        self.dosearch()

    def dosearch(self) -> None:
        """Re-run search with the current query and fill the results grid."""
        q = self.q.get()
        rows = self.store.search(q)
        for iid in self.t_search.get_children():
            self.t_search.delete(iid)
        for typ, name, code, info in rows:
            self.t_search.insert("", "end", values=(typ, name, code, info))

def main() -> None:
    """Create the Tk root and mount the app."""
    root = tk.Tk()
    TkApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()

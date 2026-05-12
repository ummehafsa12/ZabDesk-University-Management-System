import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
import hashlib
from datetime import datetime

# ===== DATA FILE =====
DATA_FILE = "zabdesk_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "students": [],
        "courses": [],
        "schedules": [],
        "fees": [],
        "admin_password": hashlib.sha256("admin123".encode()).hexdigest()
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ===== COLORS =====
BG       = "#0f0f1a"
BG2      = "#16162a"
CARD     = "#1e1e35"
GOLD     = "#c9a96e"
GOLD2    = "#e8c98a"
WHITE    = "#f0ede6"
MUTED    = "#8a8a9a"
ACCENT   = "#e64e4e"
GREEN    = "#4caf7d"
BORDER   = "#2a2a45"

# ===== MAIN APP =====
class ZabDesk:
    def __init__(self, root):
        self.root = root
        self.root.title("ZabDesk — University Management System")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)
        self.data = load_data()
        self.current_frame = None
        self.show_login()

    # ==================== LOGIN ====================
    def show_login(self):
        self.clear_root()
        frame = tk.Frame(self.root, bg=BG)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="ZABDESK", font=("Georgia", 36, "bold"),
                 bg=BG, fg=GOLD).pack(pady=(0, 4))
        tk.Label(frame, text="University Management System", font=("Helvetica", 11),
                 bg=BG, fg=MUTED).pack(pady=(0, 40))

        card = tk.Frame(frame, bg=CARD, padx=40, pady=40,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack()

        tk.Label(card, text="Admin Login", font=("Georgia", 16, "bold"),
                 bg=CARD, fg=WHITE).pack(pady=(0, 24))

        tk.Label(card, text="Username", font=("Helvetica", 10),
                 bg=CARD, fg=MUTED).pack(anchor="w")
        self.login_user = tk.Entry(card, font=("Helvetica", 12), bg=BG2,
                                   fg=WHITE, insertbackground=WHITE,
                                   relief="flat", width=28)
        self.login_user.pack(pady=(4, 14), ipady=8, padx=4)
        self.login_user.insert(0, "admin")

        tk.Label(card, text="Password", font=("Helvetica", 10),
                 bg=CARD, fg=MUTED).pack(anchor="w")
        self.login_pass = tk.Entry(card, font=("Helvetica", 12), bg=BG2,
                                   fg=WHITE, insertbackground=WHITE,
                                   relief="flat", width=28, show="•")
        self.login_pass.pack(pady=(4, 24), ipady=8, padx=4)
        self.login_pass.bind("<Return>", lambda e: self.do_login())

        btn = tk.Button(card, text="Login →", font=("Helvetica", 12, "bold"),
                        bg=GOLD, fg=BG, relief="flat", cursor="hand2",
                        command=self.do_login, width=24, pady=8)
        btn.pack()

        tk.Label(card, text="Default: admin / admin123", font=("Helvetica", 9),
                 bg=CARD, fg=MUTED).pack(pady=(14, 0))

    def do_login(self):
        user = self.login_user.get().strip()
        pwd  = self.login_pass.get().strip()
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        if user == "admin" and hashed == self.data["admin_password"]:
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # ==================== LAYOUT ====================
    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_dashboard(self):
        self.clear_root()

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=BG2, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Header
        tk.Label(self.sidebar, text="ZABDESK", font=("Georgia", 18, "bold"),
                 bg=BG2, fg=GOLD).pack(pady=(28, 4))
        tk.Label(self.sidebar, text="University System", font=("Helvetica", 9),
                 bg=BG2, fg=MUTED).pack(pady=(0, 28))

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=16, pady=4)

        nav_items = [
            ("🏠  Dashboard",   self.page_home),
            ("👨‍🎓  Students",    self.page_students),
            ("📚  Courses",      self.page_courses),
            ("🗓  Schedules",    self.page_schedules),
            ("💰  Fees",         self.page_fees),
        ]

        self.nav_buttons = []
        for label, cmd in nav_items:
            btn = tk.Button(self.sidebar, text=label, font=("Helvetica", 11),
                            bg=BG2, fg=WHITE, relief="flat", anchor="w",
                            padx=24, pady=12, cursor="hand2",
                            activebackground=CARD, activeforeground=GOLD,
                            command=lambda c=cmd, b=label: self.nav_click(c, b))
            btn.pack(fill="x")
            self.nav_buttons.append(btn)

        tk.Button(self.sidebar, text="🔓  Logout", font=("Helvetica", 10),
                  bg=BG2, fg=MUTED, relief="flat", anchor="w", padx=24, pady=10,
                  cursor="hand2", command=self.show_login).pack(side="bottom", fill="x", pady=8)

        # Main content area
        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

        self.page_home()

    def nav_click(self, cmd, label):
        for b in self.nav_buttons:
            b.configure(bg=BG2, fg=WHITE)
            if b["text"] == label:
                b.configure(bg=CARD, fg=GOLD)
        cmd()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def page_title(self, title, subtitle=""):
        hdr = tk.Frame(self.content, bg=BG, pady=20)
        hdr.pack(fill="x", padx=32)
        tk.Label(hdr, text=title, font=("Georgia", 22, "bold"),
                 bg=BG, fg=WHITE).pack(anchor="w")
        if subtitle:
            tk.Label(hdr, text=subtitle, font=("Helvetica", 10),
                     bg=BG, fg=MUTED).pack(anchor="w")
        ttk.Separator(self.content, orient="horizontal").pack(fill="x", padx=32, pady=(0, 16))

    # ==================== HOME ====================
    def page_home(self):
        self.clear_content()
        self.page_title("Dashboard", "Welcome back, Admin")

        stats_frame = tk.Frame(self.content, bg=BG)
        stats_frame.pack(fill="x", padx=32, pady=8)

        stats = [
            ("👨‍🎓 Students",  len(self.data["students"]), GOLD),
            ("📚 Courses",    len(self.data["courses"]),  "#6c9bd2"),
            ("🗓 Schedules",  len(self.data["schedules"]),GREEN),
            ("💰 Fees Due",   sum(1 for f in self.data["fees"] if f.get("status") == "Pending"), ACCENT),
        ]

        for label, val, color in stats:
            card = tk.Frame(stats_frame, bg=CARD, padx=20, pady=20,
                            highlightbackground=BORDER, highlightthickness=1)
            card.pack(side="left", expand=True, fill="both", padx=8)
            tk.Label(card, text=str(val), font=("Georgia", 32, "bold"),
                     bg=CARD, fg=color).pack()
            tk.Label(card, text=label, font=("Helvetica", 10),
                     bg=CARD, fg=MUTED).pack()

        # Recent students
        tk.Label(self.content, text="Recent Students", font=("Georgia", 14, "bold"),
                 bg=BG, fg=WHITE).pack(anchor="w", padx=32, pady=(24, 8))

        cols = ("ID", "Name", "Department", "Semester")
        tree = self.make_tree(self.content, cols)
        for s in self.data["students"][-5:]:
            tree.insert("", "end", values=(s["id"], s["name"], s["dept"], s["semester"]))
        tree.pack(fill="x", padx=32)

    # ==================== STUDENTS ====================
    def page_students(self):
        self.clear_content()
        self.page_title("Students", "Manage student records")

        # Form
        form = tk.LabelFrame(self.content, text=" Add Student ", font=("Helvetica", 10),
                              bg=BG, fg=GOLD, padx=16, pady=12,
                              highlightbackground=BORDER, highlightthickness=1)
        form.pack(fill="x", padx=32, pady=(0, 16))

        fields = [("Student ID", 10), ("Full Name", 22), ("Department", 14),
                  ("Semester", 6), ("Contact", 14), ("Email", 22)]
        self.s_vars = {}
        row = tk.Frame(form, bg=BG)
        row.pack(fill="x")
        for i, (lbl, w) in enumerate(fields):
            col = tk.Frame(row, bg=BG)
            col.pack(side="left", padx=8)
            tk.Label(col, text=lbl, font=("Helvetica", 9), bg=BG, fg=MUTED).pack(anchor="w")
            var = tk.StringVar()
            e = tk.Entry(col, textvariable=var, font=("Helvetica", 11),
                         bg=CARD, fg=WHITE, insertbackground=WHITE,
                         relief="flat", width=w)
            e.pack(ipady=6)
            self.s_vars[lbl] = var

        btns = tk.Frame(form, bg=BG)
        btns.pack(anchor="e", pady=(10, 0))
        tk.Button(btns, text="Clear", font=("Helvetica", 10), bg=CARD, fg=MUTED,
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  command=lambda: [v.set("") for v in self.s_vars.values()]).pack(side="left", padx=4)
        tk.Button(btns, text="+ Add Student", font=("Helvetica", 10, "bold"),
                  bg=GOLD, fg=BG, relief="flat", padx=14, pady=6,
                  cursor="hand2", command=self.add_student).pack(side="left")

        # Search
        sf = tk.Frame(self.content, bg=BG)
        sf.pack(fill="x", padx=32, pady=(0, 8))
        tk.Label(sf, text="Search:", font=("Helvetica", 10), bg=BG, fg=MUTED).pack(side="left")
        self.s_search = tk.StringVar()
        self.s_search.trace("w", lambda *a: self.refresh_students())
        tk.Entry(sf, textvariable=self.s_search, font=("Helvetica", 11),
                 bg=CARD, fg=WHITE, insertbackground=WHITE,
                 relief="flat", width=30).pack(side="left", padx=8, ipady=5)

        # Table
        cols = ("ID", "Name", "Department", "Semester", "Contact", "Email")
        self.s_tree = self.make_tree(self.content, cols)
        self.s_tree.pack(fill="both", expand=True, padx=32)

        tk.Button(self.content, text="🗑  Delete Selected", font=("Helvetica", 10),
                  bg=ACCENT, fg=WHITE, relief="flat", padx=14, pady=6,
                  cursor="hand2", command=self.delete_student).pack(anchor="e", padx=32, pady=8)

        self.refresh_students()

    def add_student(self):
        vals = {k: v.get().strip() for k, v in self.s_vars.items()}
        if not vals["Student ID"] or not vals["Full Name"]:
            messagebox.showwarning("Missing", "Student ID and Full Name are required.")
            return
        if any(s["id"] == vals["Student ID"] for s in self.data["students"]):
            messagebox.showerror("Duplicate", "Student ID already exists.")
            return
        self.data["students"].append({
            "id": vals["Student ID"], "name": vals["Full Name"],
            "dept": vals["Department"], "semester": vals["Semester"],
            "contact": vals["Contact"], "email": vals["Email"]
        })
        save_data(self.data)
        for v in self.s_vars.values(): v.set("")
        self.refresh_students()
        messagebox.showinfo("Success", "Student added successfully!")

    def delete_student(self):
        sel = self.s_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a student to delete.")
            return
        sid = self.s_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete student {sid}?"):
            self.data["students"] = [s for s in self.data["students"] if s["id"] != str(sid)]
            save_data(self.data)
            self.refresh_students()

    def refresh_students(self):
        q = self.s_search.get().lower() if hasattr(self, "s_search") else ""
        self.s_tree.delete(*self.s_tree.get_children())
        for s in self.data["students"]:
            if q in s["name"].lower() or q in s["id"].lower() or q in s["dept"].lower():
                self.s_tree.insert("", "end", values=(
                    s["id"], s["name"], s["dept"], s["semester"], s["contact"], s["email"]))

    # ==================== COURSES ====================
    def page_courses(self):
        self.clear_content()
        self.page_title("Courses", "Manage course catalog")

        form = tk.LabelFrame(self.content, text=" Add Course ", font=("Helvetica", 10),
                              bg=BG, fg=GOLD, padx=16, pady=12,
                              highlightbackground=BORDER, highlightthickness=1)
        form.pack(fill="x", padx=32, pady=(0, 16))

        row = tk.Frame(form, bg=BG)
        row.pack(fill="x")
        fields = [("Course Code", 12), ("Course Name", 28), ("Credits", 6), ("Instructor", 20)]
        self.c_vars = {}
        for lbl, w in fields:
            col = tk.Frame(row, bg=BG)
            col.pack(side="left", padx=8)
            tk.Label(col, text=lbl, font=("Helvetica", 9), bg=BG, fg=MUTED).pack(anchor="w")
            var = tk.StringVar()
            tk.Entry(col, textvariable=var, font=("Helvetica", 11),
                     bg=CARD, fg=WHITE, insertbackground=WHITE,
                     relief="flat", width=w).pack(ipady=6)
            self.c_vars[lbl] = var

        tk.Button(form, text="+ Add Course", font=("Helvetica", 10, "bold"),
                  bg=GOLD, fg=BG, relief="flat", padx=14, pady=6,
                  cursor="hand2", command=self.add_course).pack(anchor="e", pady=(10, 0))

        cols = ("Code", "Name", "Credits", "Instructor")
        self.c_tree = self.make_tree(self.content, cols)
        self.c_tree.pack(fill="both", expand=True, padx=32)

        tk.Button(self.content, text="🗑  Delete Selected", font=("Helvetica", 10),
                  bg=ACCENT, fg=WHITE, relief="flat", padx=14, pady=6,
                  cursor="hand2", command=self.delete_course).pack(anchor="e", padx=32, pady=8)

        self.refresh_courses()

    def add_course(self):
        vals = {k: v.get().strip() for k, v in self.c_vars.items()}
        if not vals["Course Code"] or not vals["Course Name"]:
            messagebox.showwarning("Missing", "Course Code and Name are required.")
            return
        self.data["courses"].append({
            "code": vals["Course Code"], "name": vals["Course Name"],
            "credits": vals["Credits"], "instructor": vals["Instructor"]
        })
        save_data(self.data)
        for v in self.c_vars.values(): v.set("")
        self.refresh_courses()

    def delete_course(self):
        sel = self.c_tree.selection()
        if not sel: return
        code = self.c_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete course {code}?"):
            self.data["courses"] = [c for c in self.data["courses"] if c["code"] != str(code)]
            save_data(self.data)
            self.refresh_courses()

    def refresh_courses(self):
        self.c_tree.delete(*self.c_tree.get_children())
        for c in self.data["courses"]:
            self.c_tree.insert("", "end", values=(c["code"], c["name"], c["credits"], c["instructor"]))

    # ==================== SCHEDULES ====================
    def page_schedules(self):
        self.clear_content()
        self.page_title("Schedules", "Manage class timetable")

        form = tk.LabelFrame(self.content, text=" Add Schedule ", font=("Helvetica", 10),
                              bg=BG, fg=GOLD, padx=16, pady=12,
                              highlightbackground=BORDER, highlightthickness=1)
        form.pack(fill="x", padx=32, pady=(0, 16))

        row = tk.Frame(form, bg=BG)
        row.pack(fill="x")

        self.sch_vars = {}
        fields = [("Course Code", 14), ("Day", 10), ("Time", 12), ("Room", 10), ("Semester", 8)]
        for lbl, w in fields:
            col = tk.Frame(row, bg=BG)
            col.pack(side="left", padx=8)
            tk.Label(col, text=lbl, font=("Helvetica", 9), bg=BG, fg=MUTED).pack(anchor="w")
            var = tk.StringVar()
            if lbl == "Day":
                days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
                ttk.Combobox(col, textvariable=var, values=days,
                             width=w, font=("Helvetica", 11), state="readonly").pack(ipady=4)
            else:
                tk.Entry(col, textvariable=var, font=("Helvetica", 11),
                         bg=CARD, fg=WHITE, insertbackground=WHITE,
                         relief="flat", width=w).pack(ipady=6)
            self.sch_vars[lbl] = var

        tk.Button(form, text="+ Add Schedule", font=("Helvetica", 10, "bold"),
                  bg=GOLD, fg=BG, relief="flat", padx=14, pady=6,
                  cursor="hand2", command=self.add_schedule).pack(anchor="e", pady=(10, 0))

        cols = ("Course Code", "Day", "Time", "Room", "Semester")
        self.sch_tree = self.make_tree(self.content, cols)
        self.sch_tree.pack(fill="both", expand=True, padx=32)

        tk.Button(self.content, text="🗑  Delete Selected", font=("Helvetica", 10),
                  bg=ACCENT, fg=WHITE, relief="flat", padx=14, pady=6,
                  cursor="hand2", command=self.delete_schedule).pack(anchor="e", padx=32, pady=8)

        self.refresh_schedules()

    def add_schedule(self):
        vals = {k: v.get().strip() for k, v in self.sch_vars.items()}
        if not vals["Course Code"] or not vals["Day"]:
            messagebox.showwarning("Missing", "Course Code and Day are required.")
            return
        self.data["schedules"].append({
            "code": vals["Course Code"], "day": vals["Day"],
            "time": vals["Time"], "room": vals["Room"],
            "semester": vals["Semester"]
        })
        save_data(self.data)
        for v in self.sch_vars.values(): v.set("")
        self.refresh_schedules()

    def delete_schedule(self):
        sel = self.sch_tree.selection()
        if not sel: return
        idx = self.sch_tree.index(sel[0])
        if messagebox.askyesno("Confirm", "Delete this schedule?"):
            self.data["schedules"].pop(idx)
            save_data(self.data)
            self.refresh_schedules()

    def refresh_schedules(self):
        self.sch_tree.delete(*self.sch_tree.get_children())
        for s in self.data["schedules"]:
            self.sch_tree.insert("", "end", values=(s["code"], s["day"], s["time"], s["room"], s["semester"]))

    # ==================== FEES ====================
    def page_fees(self):
        self.clear_content()
        self.page_title("Fee Management", "Track student payments")

        form = tk.LabelFrame(self.content, text=" Add Fee Record ", font=("Helvetica", 10),
                              bg=BG, fg=GOLD, padx=16, pady=12,
                              highlightbackground=BORDER, highlightthickness=1)
        form.pack(fill="x", padx=32, pady=(0, 16))

        row = tk.Frame(form, bg=BG)
        row.pack(fill="x")

        self.f_vars = {}
        fields = [("Student ID", 12), ("Amount ($)", 10), ("Semester", 8)]
        for lbl, w in fields:
            col = tk.Frame(row, bg=BG)
            col.pack(side="left", padx=8)
            tk.Label(col, text=lbl, font=("Helvetica", 9), bg=BG, fg=MUTED).pack(anchor="w")
            var = tk.StringVar()
            tk.Entry(col, textvariable=var, font=("Helvetica", 11),
                     bg=CARD, fg=WHITE, insertbackground=WHITE,
                     relief="flat", width=w).pack(ipady=6)
            self.f_vars[lbl] = var

        col = tk.Frame(row, bg=BG)
        col.pack(side="left", padx=8)
        tk.Label(col, text="Status", font=("Helvetica", 9), bg=BG, fg=MUTED).pack(anchor="w")
        self.f_status = tk.StringVar(value="Pending")
        ttk.Combobox(col, textvariable=self.f_status,
                     values=["Pending", "Paid", "Partial"],
                     width=10, font=("Helvetica", 11), state="readonly").pack(ipady=4)

        col2 = tk.Frame(row, bg=BG)
        col2.pack(side="left", padx=8)
        tk.Label(col2, text="Date", font=("Helvetica", 9), bg=BG, fg=MUTED).pack(anchor="w")
        self.f_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(col2, textvariable=self.f_date, font=("Helvetica", 11),
                 bg=CARD, fg=WHITE, insertbackground=WHITE,
                 relief="flat", width=12).pack(ipady=6)

        tk.Button(form, text="+ Add Record", font=("Helvetica", 10, "bold"),
                  bg=GOLD, fg=BG, relief="flat", padx=14, pady=6,
                  cursor="hand2", command=self.add_fee).pack(anchor="e", pady=(10, 0))

        # Summary
        total_due = sum(float(f.get("amount", 0)) for f in self.data["fees"] if f.get("status") == "Pending")
        total_paid = sum(float(f.get("amount", 0)) for f in self.data["fees"] if f.get("status") == "Paid")
        sf = tk.Frame(self.content, bg=BG)
        sf.pack(fill="x", padx=32, pady=(0, 10))
        for label, val, color in [("Total Pending", f"${total_due:.2f}", ACCENT),
                                   ("Total Paid", f"${total_paid:.2f}", GREEN)]:
            c = tk.Frame(sf, bg=CARD, padx=20, pady=10,
                         highlightbackground=BORDER, highlightthickness=1)
            c.pack(side="left", padx=6)
            tk.Label(c, text=val, font=("Georgia", 16, "bold"), bg=CARD, fg=color).pack()
            tk.Label(c, text=label, font=("Helvetica", 9), bg=CARD, fg=MUTED).pack()

        cols = ("Student ID", "Amount", "Semester", "Status", "Date")
        self.f_tree = self.make_tree(self.content, cols)
        self.f_tree.pack(fill="both", expand=True, padx=32)

        tk.Button(self.content, text="🗑  Delete Selected", font=("Helvetica", 10),
                  bg=ACCENT, fg=WHITE, relief="flat", padx=14, pady=6,
                  cursor="hand2", command=self.delete_fee).pack(anchor="e", padx=32, pady=8)

        self.refresh_fees()

    def add_fee(self):
        vals = {k: v.get().strip() for k, v in self.f_vars.items()}
        if not vals["Student ID"] or not vals["Amount ($)"]:
            messagebox.showwarning("Missing", "Student ID and Amount are required.")
            return
        self.data["fees"].append({
            "student_id": vals["Student ID"],
            "amount": vals["Amount ($)"],
            "semester": vals["Semester"],
            "status": self.f_status.get(),
            "date": self.f_date.get()
        })
        save_data(self.data)
        for v in self.f_vars.values(): v.set("")
        self.page_fees()

    def delete_fee(self):
        sel = self.f_tree.selection()
        if not sel: return
        idx = self.f_tree.index(sel[0])
        if messagebox.askyesno("Confirm", "Delete this fee record?"):
            self.data["fees"].pop(idx)
            save_data(self.data)
            self.page_fees()

    def refresh_fees(self):
        self.f_tree.delete(*self.f_tree.get_children())
        for f in self.data["fees"]:
            color = ""
            self.f_tree.insert("", "end", values=(
                f["student_id"], f"${f['amount']}", f["semester"], f["status"], f["date"]))

    # ==================== HELPERS ====================
    def make_tree(self, parent, columns):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                         background=CARD, foreground=WHITE,
                         fieldbackground=CARD, rowheight=32,
                         borderwidth=0, font=("Helvetica", 10))
        style.configure("Custom.Treeview.Heading",
                         background=BG2, foreground=GOLD,
                         font=("Helvetica", 10, "bold"), borderwidth=0)
        style.map("Custom.Treeview",
                  background=[("selected", BORDER)],
                  foreground=[("selected", GOLD)])

        frame = tk.Frame(parent, bg=BG)
        tree = ttk.Treeview(frame, columns=columns, show="headings",
                             style="Custom.Treeview", height=10)
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="w", minwidth=80)

        return frame


# ===== RUN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = ZabDesk(root)
    root.mainloop()

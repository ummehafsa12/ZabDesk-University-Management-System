# 🎓 ZabDesk — University Management System

A Python-based desktop application for managing university operations, built with **Tkinter GUI**.

## ✨ Features

- 🔐 **Admin Login** — Secure password-protected access
- 👨‍🎓 **Student Records** — Add, view, search, and delete students
- 📚 **Course Management** — Maintain course catalog with instructor info
- 🗓️ **Schedule Management** — Timetable with day, time, room assignment
- 💰 **Fee Tracking** — Record payments, track pending/paid status
- 💾 **Persistent Storage** — All data saved locally in JSON format
- 🌙 **Dark Theme UI** — Clean, modern dark interface

## 🛠️ Tech Stack

| Tech | Usage |
|------|-------|
| Python 3 | Core language |
| Tkinter | GUI framework (built-in) |
| JSON | Local data persistence |
| hashlib | Password hashing |

## 📂 Project Structure

```
ZabDesk/
├── zabdesk.py          # Main application
├── zabdesk_data.json   # Auto-generated data file
└── README.md           # Documentation
```

## 🚀 Getting Started

### Requirements
- Python 3.x (Tkinter is included by default)

### Run the app
```bash
python zabdesk.py
```

### Default Login
```
Username: admin
Password: admin123
```

## 📸 Modules

| Module | Features |
|--------|----------|
| Dashboard | Stats overview, recent students |
| Students | Add/search/delete student records |
| Courses | Course catalog management |
| Schedules | Weekly timetable management |
| Fees | Payment tracking with status |

## 🔮 Future Improvements

- Role-based access (staff, student portals)
- MySQL database integration
- PDF report generation
- Email notifications for fee dues

## 📄 License

MIT License

---
Built with ❤️ using Python & Tkinter

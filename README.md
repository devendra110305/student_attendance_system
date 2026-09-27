# 🎓 Student Attendance Management System

A colorful, modern, full-stack **Student Attendance Management System** built with **Flask** + **SQLite** + **HTML/CSS/JS**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 👨‍🎓 **Student Records** — Add, view, delete students
- 📚 **Subjects** — Manage subjects with faculty info
- ✅ **Attendance Entry** — Mark Present/Absent with one click
- 📅 **Date-wise Records** — Filter attendance by date & subject
- 📊 **Reports** — Percentage calculation per student per subject
- 🏆 **Top Performers** — Ranked by attendance percentage
- 🕒 **Live Dashboard** — Real-time stats, clock, recent activity
- 🎨 **Modern UI** — Gradients, animations, particles, glassmorphism

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Templating | Jinja2 |

---

## 📁 Project Structure

```
student_attendance_system/
│
├── app.py                  # Flask application (routes & logic)
├── database.py             # SQLite setup & connection
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore rules
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── students.html
│   ├── subjects.html
│   ├── attendance.html
│   ├── datewise.html
│   └── report.html
│
└── static/                 # Static assets
    ├── style.css
    └── script.js
```

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/student_attendance_system.git
cd student_attendance_system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```

### 4. Open in your browser
```
http://127.0.0.1:5000/
```

> 💡 The `attendance.db` file is auto-created on first run.

---

## 📖 How to Use

1. **Add Students** → go to *Students* page → enter Roll No, Name, Class, Email
2. **Add Subjects** → go to *Subjects* page → enter Code, Name, Faculty
3. **Mark Attendance** → go to *Mark Attendance* → pick date + subject → save
4. **View Records** → *Date-wise* page to filter by date
5. **Check Reports** → *Reports* page shows percentage per student per subject

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo, open issues, or submit pull requests.

---

## 👨‍💻 Author

**Devendra**

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

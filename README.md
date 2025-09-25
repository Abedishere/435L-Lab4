# EECE435L Software Tools Lab Project

## Lab 4: Version Control, Git and GitHub
**Student:** Abdel Rahman El Kouche

### Project Description
This repository contains the School Management System project developed in Lab 2, now organized for collaborative development using Git version control. The project demonstrates the integration of different GUI frameworks (Tkinter and PyQt) with a comprehensive database management system.

### Project Structure
```
├── database_manager.py    # Database operations and management
├── integrated_gui.py      # Combined GUI interface
├── pyqt_gui.py           # PyQt interface implementation
├── tkinter_gui.py        # Tkinter interface implementation
├── school_management.py   # Core business logic
├── docs/                 # Documentation files
└── __pycache__/          # Python bytecode cache
```

### Features
- **Database Management**: SQLite database for storing student, instructor, and course information
- **Dual GUI Implementation**:
  - Tkinter interface for traditional desktop application feel
  - PyQt interface for modern, feature-rich user experience
- **Integrated Interface**: Combined functionality from both GUI frameworks
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Data Validation**: Input validation and error handling

### How to Run
1. **Tkinter Interface**: `python tkinter_gui.py`
2. **PyQt Interface**: `python pyqt_gui.py`
3. **Integrated Interface**: `python integrated_gui.py`

### Requirements
- Python 3.x
- tkinter (usually included with Python)
- PyQt5 or PyQt6
- sqlite3 (included with Python)

### Lab 4 Collaboration Setup
This project is set up for collaborative development between two students:
- **Student 1**: Focus on Tkinter UI enhancements and testing
- **Student 2**: Focus on PyQt UI enhancements and backend integration

### Git Workflow
1. Clone the repository
2. Create feature branches for specific implementations
3. Commit changes with descriptive messages
4. Use pull requests for code review and integration
5. Merge completed features into main branch

### Version Control Best Practices
- Regular commits with meaningful messages
- Branch-based development workflow
- Code review through pull requests
- Proper handling of merge conflicts
- Documentation of changes and features

---
*Developed for EECE435L Software Tools Lab - Fall 2025*
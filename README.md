# EECE435L Software Tools Lab Project

## Lab 4: Version Control, Git and GitHub
**Student:** Abdel Rahman El Kouche
**Student:** Karim Abou Daher

### Project Description
This repository contains the School Management System project developed in Lab 2, now organized for collaborative development using Git version control. The project demonstrates the integration of different GUI frameworks (Tkinter and PyQt) with a comprehensive database management system.

### Project Structure
```
├── .gitignore             # Python project ignore patterns
├── README.md              # Project documentation
├── database_manager.py    # Documented database operations (from documented proj)
├── school_management.py   # Documented core business logic (from documented proj)
├── integrated_gui.py      # Documented combined interface (from documented proj)
├── pyqt_gui.py           # Documented PyQt interface (from documented proj)
├── tkinter_gui.py        # Tkinter interface (ready for enhancement)
└── docs/                 # Sphinx documentation for documented modules
```

### Features
- **Documented Core System**: Well-documented database and business logic modules
- **Dual GUI Implementation**:
  - **PyQt Interface**: Fully documented, feature-rich modern interface
  - **Tkinter Interface**: Basic implementation ready for collaborative enhancement
  - **Integrated Interface**: Documented combined functionality demonstration
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Data Persistence**: SQLite database with comprehensive management
- **Documentation**: Sphinx-generated documentation for core modules

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
- **Student 1**: Enhance and document the Tkinter interface (`tkinter_gui.py`)
- **Student 2**: Work with the documented PyQt interface and backend integration

### File Organization for Collaboration
- **Core documented modules** (database_manager.py, school_management.py): Shared foundation
- **PyQt implementation**: Fully documented and ready for advanced features
- **Tkinter implementation**: Basic version ready for enhancement and documentation
- **Integration example**: Shows how both frameworks can work together

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
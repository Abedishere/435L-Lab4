# EECE435L Software Tools Lab Project

## Lab 4: Version Control, Git and GitHub
**Student:** Abdel Rahman El Kouche
**Student:** Karim Abou Daher

### Project Description
This repository contains the School Management System project developed in Lab 2, now organized for collaborative development using Git version control. The project demonstrates the integration of different GUI frameworks (Tkinter and PyQt) with a comprehensive database management system.

### Project Structure
```
├── .gitignore                    # Python project ignore patterns
├── README.md                     # Project documentation
├── database_manager.py           # Documented database operations
├── school_management.py          # Documented core business logic
├── pyqt_implementation/          # PyQt GUI implementations
│   ├── pyqt_gui.py              # Basic PyQt interface
│   └── integrated_gui.py        # PyQt interface with database support
├── tkinter_implementation/       # Tkinter GUI implementations
│   └── apptk.py                 # Tkinter interface by Karim
├── school.py                     # School management logic by Karim
├── start.py                      # Main entry point by Karim
├── store.py                      # Data storage by Karim
└── docs/                         # Sphinx documentation for documented modules
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

#### PyQt Implementations
1. **Basic PyQt Interface**:
   ```bash
   python pyqt_implementation/pyqt_gui.py
   ```

2. **PyQt Interface with Database Support**:
   ```bash
   python pyqt_implementation/integrated_gui.py
   ```

#### Tkinter Implementation
1. **Karim's Tkinter Interface**:
   ```bash
   python tkinter_implementation/apptk.py
   ```

#### Alternative Entry Points
1. **Karim's Main Application**:
   ```bash
   python start.py
   ```

### Requirements
- Python 3.x
- tkinter (usually included with Python)
- PyQt5 or PyQt6
- sqlite3 (included with Python)

### Lab 4 Collaboration Setup
This project is set up for collaborative development between two students:
- **AbdelRahman El Kouche**: PyQt interface implementations with database integration
- **Karim Abou Daher**: Tkinter interface and alternative backend implementation

### File Organization for Collaboration
- **Core modules** (database_manager.py, school_management.py): Shared foundation by AbdelRahman
- **PyQt implementation**: Complete PyQt interfaces with basic and database-integrated versions
- **Tkinter implementation**: Karim's Tkinter interface implementation
- **Alternative backend**: Karim's school.py, store.py, and start.py provide alternative implementation

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
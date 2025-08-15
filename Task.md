# Flask Project Refactor Task & Summary

## Objective
Refactor the existing Flask project to follow a clean **Model–View–Template (MVT) style architecture**, migrate the database from **PostgreSQL** to **MySQL**, implement relevant **design patterns**, and rename files/functions for clarity — all without breaking functionality.

---

## Target Folder Structure
CODE_GUIDE/
│
├── project/ # Core application logic
│ ├── models/ # Database models & ORM logic
│ ├── views/ # Route handlers & business logic
│ ├── templates/ # HTML templates
│ ├── static/ # CSS / JS / Images
│ ├── utils/ # Helper functions
│ ├── init.py # Flask app factory
│ ├── routes.py # URL routing definitions
│
├── config/ # Environment-specific configs
│ ├── init.py


---

## Key Refactoring Changes

### 1. Folder Structure Transformation
- **Before:** Flat structure with templates, static files, and logic in the same directory.
- **After:** Separated code into models, views, templates, static, and utils, following MVT principles.

### 2. Database Migration
- Migrated from **PostgreSQL** to **MySQL**.
- Updated SQLAlchemy URI in configuration.
- Adjusted migration scripts and `.env` to use MySQL.

### 3. Design Pattern Adoption
- Implemented **MVT-style architecture**.
- Centralized reusable logic in `utils/`.
- Organized route logic inside `views/`.
- Improved naming for clarity (e.g., `db_ops.py` → `models/user.py`).

### 4. Codebase Cleanup
- Removed unused imports, redundant code, and deprecated functions.
- Added `.gitignore` to exclude `venv/` and other environment-specific files.
- Unified database connection logic via a single Flask app factory pattern.

---

## Benefits Achieved
- **Maintainability:** Clear separation of concerns and structured layout.
- **Scalability:** Easy to add more features without clutter.
- **Portability:** MySQL compatibility across multiple hosting providers.
- **Readability:** Consistent naming conventions and better organized logic.

---

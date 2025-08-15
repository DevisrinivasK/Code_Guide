# Flask Project Refactor Task

## Objective
Refactor the existing Flask project to follow a clean **MVT-style architecture**, migrate the database from **PostgreSQL** to **MySQL**, implement relevant **design patterns**, and rename files/functions for clarity — all without breaking functionality.

---

## Target Folder Structure
CODE_GUIDE/
│
├── project/
│ ├── models/ # Database models & ORM
│ ├── views/ # Route handlers & business logic
│ ├── templates/ # HTML templates
│ ├── static/ # CSS/JS/images
│ ├── utils/ # Helper functions
│ ├── init.py # Flask app factory
│ └── routes.py # URL routing
│
├── config/
│ ├── init.py
│ └── settings.py # MySQL config
│
├── venv/
├── requirements.txt
├── manage.py # App entry point
└── REFACTOR_SUMMARY.md

---

## Step-by-Step Refactor Plan---

## Refactor Instructions for Copilot
1. **Convert `app.py` into App Factory**  
   - Move app creation into `project/__init__.py` as `create_app()`.  
   - Configure the app to load database settings from `config/settings.py`.  
   - Remove direct route definitions from `app.py` and move them to `routes.py`.

2. **Create `routes.py`**  
   - Move all `@app.route` definitions here.  
   - Each route should only call a function from `views/` and not contain core business logic.

3. **Move Business Logic into `views/`**  
   - For each route, create a corresponding function in `views/`.  
   - Keep route functions thin; business logic goes inside these view functions.  
   - Import and use models for DB interactions, utils for helper logic.

4. **Move DB Code into `models/`**  
   - All schema definitions and database queries go into `models/`.  
   - Replace PostgreSQL queries/configuration with MySQL equivalents.  
   - Apply the **Singleton pattern** to manage DB connections.

5. **Move Reusable Functions into `utils/`**  
   - Identify helper functions and move them here.  
   - Give them meaningful, descriptive names.  
   - Keep them generic for reuse across the project.

6. **Organize `templates/`**  
   - Ensure all HTML files are in `templates/` and loaded with `render_template()`.  
   - Rename files for clarity (e.g., `dashboard.html` instead of `page1.html`).

7. **Create `settings.py` in `config/`**  
   - Store MySQL configuration here.  
   - Use `python-dotenv` to load credentials from `.env`.  
   - Keep sensitive data out of source code.

8. **Update `requirements.txt`**  
   - Remove PostgreSQL dependencies.  
   - Add MySQL drivers (`mysqlclient` or `PyMySQL`).

9. **Create `manage.py`**  
   - Serve as the application entry point.  
   - Import `create_app()` from `project/__init__.py` and run it.

10. **Document All Changes in `REFACTOR_SUMMARY.md`**  
    - List old vs new file names.  
    - Summarize the folder structure.  
    - Detail database migration steps.  
    - Note design patterns added.

---

## Rules for Copilot
- Never delete working functionality unless absolutely necessary for migration.
- Always use descriptive names for files, functions, and variables.
- Maintain clear separation between models, views, and templates.
- Ensure the project runs correctly after all changes.
- Apply design patterns thoughtfully, not just for the sake of using them.


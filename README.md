# Student Study Tracker

Student Study Tracker is a web application that helps college students organize their assignments, manage their time, and keep track of their academic progress. It gives students one central place to see upcoming deadlines, estimate how long work will take, and keep notes for each class.

## Planned Features
- Assignment tracker with due dates, estimated time, and completion status
- Notes for classes and comments on assignments
- Dashboard of upcoming and completed work with a progress tracker
- Deadline reminders

## Technology Stack
- **Frontend**: React
- **Backend**: Python, Flask
- **Database**: SQLite
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Hosting**: Google Cloud Run
- **Project Management**: Jira, Confluence

## AI Integration
I am using GitHub Copilot, Claude, and ChatGPT for boilerplate code, debugging, writing tests, and drafting Docker and GitHub Actions files. See the AI Usage section below for specific examples.

## Current Status (Sprint 1: MVP)
- Assignment tracker: add, list, complete, and delete assignments (Flask + SQLite)
- Dockerized with a Dockerfile; runs locally and on Google Cloud Run
- Deployed manually to Cloud Run: https://student-study-tracker-753670552196.us-central1.run.app
- Not yet built (planned for Sprint 2): login, notes/comments, dashboard, reminders, automated tests, CI/CD
- Simplified from the original plan: the MVP uses plain Flask with an HTML page instead of React to get an end-to-end version working quickly.
- Styled with a Copilot-generated stylesheet (`static/style.css`), merged through a pull request

## Getting Started
Run locally with Docker:
   
```bash
docker build -t student-study-tracker .
docker run -p 8080:8080 student-study-tracker
```

Then open http://localhost:8080.

## Deployment
Deployed from Google Cloud Shell:

```bash
gcloud run deploy student-study-tracker --source . --region us-central1 --allow-unauthenticated
```

Known limitation: SQLite lives inside the container, so data resets when Cloud Run restarts. Cloud SQL is a planned upgrade.

## AI Usage

### Claude
Generated the initial `app.py`, `templates/index.html`, and `Dockerfile`, and walked me through git branches, Docker, and Cloud Run.

Example of AI-generated code (the main page route in `app.py`):

```python
@app.route("/")
def index():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM assignments ORDER BY completed, due_date"
    ).fetchall()
    conn.close()
    return render_template("index.html", assignments=rows)
```

Example of AI-generated code (database setup in `app.py`):

```python
def init_db():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS assignments (...)")
```

### GitHub Copilot
Generated the stylesheet (`static/style.css`) from a Copilot Chat prompt. I reviewed the output, tested it in Docker, and kept the layout it produced.

Prompt I used:

> Write a clean, modern stylesheet for my Flask assignment tracker page. It has a heading, an add-assignment form, and a table with Complete and Delete buttons. Completed rows have a "done" class. Use a card-style layout, readable fonts, a blue accent color, and make it look good on mobile.

Example of Copilot-generated code (from `static/style.css`):

```css
form.add button[type="submit"] {
  background: var(--blue);
  color: #fff;
  white-space: nowrap;
}

form.add button[type="submit"]:hover {
  background: var(--blue-dark);
}
```

### What I did myself
Reviewed and tested the code in Docker, fixed an empty-file commit and a misnamed `.dockerignore`, then deployed to Cloud Run.

### Lessons
AI-generated code still needs verification. An empty commit and a paste error showed that, along with indent issues.

## Development Workflow
- Each change was built on a feature branch (`feature/assignment-tracker`, `feature/css-styling`, `docs/copilot-usage`) and merged to `main` through a pull request.
- Commits are small and descriptive. The history also shows two mistakes I caught and fixed: an empty `app.py` commit and a misnamed `.dockerignore`.
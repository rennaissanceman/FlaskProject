# Getting Started with Flask Movie Database

This project was bootstrapped as a simple **Flask + SQLite** application.

It provides a minimal web interface for managing a list of movies:
adding new entries, displaying them, and removing selected ones.

---

## Available Scripts

In the project directory, you can run:

---

### `python app.py`

Runs the application in **development mode** using the built-in Flask server.

Open  
http://127.0.0.1:5000  
to view it in your browser.

The page will reload automatically when you make changes to the code.

Any runtime errors or logs will be visible in the terminal.

---

### `flask run --debug`

Runs the app using **Flask CLI** with debug mode enabled.

Before running this command, make sure the Flask app is set:

```powershell
$env:FLASK_APP="app.py"

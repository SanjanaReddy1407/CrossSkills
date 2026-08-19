"""
extensions.py
The SQLAlchemy `db` object lives here (not in app.py) so that models.py,
services, and app.py can all import it without circular-import problems.

    app.py       -> creates Flask app, calls db.init_app(app)
    models.py    -> imports db, defines db.Model subclasses
    services/*   -> imports db for db.session queries
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
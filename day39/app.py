from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
import re


app = Flask(__name__)
app.config["SECRET_KEY"] = "day39-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)


def validate_registration(name, email, password):
    errors = []

    if not name or len(name) < 2:
        errors.append("El nombre debe tener al menos 2 caracteres.")

    if not email:
        errors.append("El correo es obligatorio.")
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors.append("El correo no tiene un formato valido.")

    if not password:
        errors.append("La contrasena es obligatoria.")
    elif len(password) < 6:
        errors.append("La contrasena debe tener al menos 6 caracteres.")

    return errors


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        errors = validate_registration(name, email, password)
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("register"))

        existing_user = User.query.filter(func.lower(User.email) == email).first()
        if existing_user:
            flash("Este correo ya esta registrado.", "error")
            return redirect(url_for("register"))

        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
        )

        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Usuario registrado correctamente.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("No se pudo completar el registro. Intenta de nuevo.", "error")

        return redirect(url_for("register"))

    users = User.query.order_by(User.id.desc()).all()
    return render_template("register.html", users=users)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

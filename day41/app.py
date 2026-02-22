from flask import Flask, render_template
# from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
app.config["ENV"] = os.getenv("FLASK_ENV", "production")
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "0") == "1"


@app.route("/")
def index():
    return render_template(
        "index.html",
        app_name=os.getenv("APP_NAME", "Flask Deploy Practice"),
        env_name=app.config["ENV"],
    )


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port, debug=app.config["DEBUG"])

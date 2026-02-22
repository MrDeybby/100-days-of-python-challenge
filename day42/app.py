from flask import Flask, render_template, abort

app = Flask(__name__)

projects_data = [
    {
        "slug": "dashboard-ventas",
        "title": "Dashboard de Ventas",
        "summary": "Analisis interactivo de ventas mensuales con KPIs y tendencias.",
        "stack": ["Python", "Pandas", "Plotly", "Flask"],
        "impact": "Reducíon de 35% del tiempo de analisis para reportes semanales.",
    },
    {
        "slug": "prediccion-churn",
        "title": "Prediccion de Churn",
        "summary": "Modelo de machine learning para detectar clientes en riesgo.",
        "stack": ["Python", "Scikit-learn", "SQL", "Matplotlib"],
        "impact": "Permitio priorizar retencion con segmentacion automatica.",
    },
    {
        "slug": "etl-automatizado",
        "title": "Pipeline ETL Automatizado",
        "summary": "Extraccion y transformacion diaria de datos desde APIs y CSV.",
        "stack": ["Python", "SQLite", "APIs", "Airflow"],
        "impact": "Mejoro la calidad de datos y redujo errores manuales.",
    },
]


@app.route("/")
def home():
    featured = projects_data[:2]
    return render_template("home.html", featured_projects=featured)


@app.route("/proyectos")
def projects():
    return render_template("projects.html", projects=projects_data, active_tag=None)


@app.route("/etiquetas/<tag>")
def projects_by_tag(tag):
    normalized_tag = tag.strip().lower()
    filtered_projects = [
        project
        for project in projects_data
        if any(stack_item.lower() == normalized_tag for stack_item in project["stack"])
    ]
    display_tag = next(
        (
            stack_item
            for project in projects_data
            for stack_item in project["stack"]
            if stack_item.lower() == normalized_tag
        ),
        tag,
    )
    return render_template(
        "projects.html",
        projects=filtered_projects,
        active_tag=display_tag,
    )


@app.route("/proyectos/<slug>")
def project_detail(slug):
    project = next((p for p in projects_data if p["slug"] == slug), None)
    if not project:
        abort(404)
    return render_template("project_detail.html", project=project)


@app.route("/acerca")
def about():
    return render_template("about.html")


@app.route("/contactos")
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)

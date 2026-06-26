from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os

from parser import extract_resume_data
from matcher import calculate_match_score
from database import create_table, add_candidate, get_candidates, delete_candidate

app = Flask(__name__)
app.secret_key = "resumeproject"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

create_table()


@app.route("/")
def dashboard():
    candidates = get_candidates()

    total = len(candidates)
    average = 0
    top = "-"

    if total > 0:
        average = round(sum(c["score"] for c in candidates) / total, 2)
        top = max(candidates, key=lambda x: x["score"])["name"]

    return render_template(
        "dashboard.html",
        candidates=candidates,
        total=total,
        average=average,
        top=top
    )


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        if "resume" not in request.files:
            flash("Please select a resume.")
            return redirect("/upload")

        file = request.files["resume"]

        if file.filename == "":
            flash("Please select a PDF resume.")
            return redirect("/upload")

        if not file.filename.lower().endswith(".pdf"):
            flash("Only PDF files are allowed.")
            return redirect("/upload")

        job_title = request.form.get("job_title")
        education = request.form.get("education")
        experience = request.form.get("experience")
        selected_skills = request.form.getlist("skills")

        if not selected_skills:
            flash("Please select at least one required skill.")
            return redirect("/upload")

        job_description = " ".join(selected_skills)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        try:
            candidate = extract_resume_data(filepath)
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            flash("Invalid or corrupted PDF.")
            return redirect("/upload")

        candidate["score"] = calculate_match_score(
            candidate["skills"],
            job_description
        )

        candidate["resume"] = filename
        candidate["job_title"] = job_title
        candidate["required_education"] = education
        candidate["required_experience"] = experience
        candidate["required_skills"] = selected_skills

        try:
            add_candidate(candidate)
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            flash("Candidate already exists.")
            return redirect("/upload")

        flash("Resume analyzed successfully!")
        return redirect("/results")

    return render_template("upload.html")


@app.route("/results")
def results():
    candidates = get_candidates()
    return render_template("results.html", candidates=candidates)


@app.route("/ranking")
def ranking():
    candidates = get_candidates()
    return render_template("ranking.html", candidates=candidates)


@app.route("/delete/<int:id>")
def delete(id):
    delete_candidate(id)
    flash("Candidate deleted successfully.")
    return redirect("/results")


if __name__ == "__main__":
    app.run(debug=True)

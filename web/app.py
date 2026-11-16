"""
Interactive Web Application for PathMatch Recommendation Engine.
Powered by Flask, O*NET Content Model, and Agentic AI Architecture.
"""

import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src import (
    StudentProfile,
    ONetDataLoader,
    PathMatcher,
    ResumeParserAgent,
    CareerCoachAgent,
    CompanyInternshipCatalog
)

app = Flask(__name__, template_folder="templates", static_folder="static")

# Initialize shared components
loader = ONetDataLoader()
default_matcher = PathMatcher(data_loader=loader)
resume_parser = ResumeParserAgent()
career_coach = CareerCoachAgent()
company_catalog = CompanyInternshipCatalog()


@app.route("/")
def index():
    domains = loader.get_unique_domains()
    return render_template("index.html", domains=domains)


@app.route("/api/profiles", methods=["GET"])
def get_sample_profiles():
    profile_dir = PROJECT_ROOT / "sample_profiles"
    profile_files = sorted(list(profile_dir.glob("student_*.json")))
    profiles = []
    for pfile in profile_files:
        p = StudentProfile.from_file(pfile)
        profiles.append({
            "id": p.id,
            "filename": pfile.name,
            "name": p.name,
            "major": p.major,
            "degree_level": p.degree_level,
            "profile_data": p.to_dict()
        })
    return jsonify(profiles)


@app.route("/api/domains", methods=["GET"])
def get_domains():
    return jsonify(loader.get_unique_domains())


@app.route("/api/parse_resume", methods=["POST"])
def parse_resume():
    """
    Agentic Endpoint: Parses raw text or an uploaded PDF CV into a structured StudentProfile.
    """
    resume_text = ""
    candidate_name = None

    if "file" in request.files:
        file = request.files["file"]
        candidate_name = request.form.get("name")
        if file.filename.endswith(".pdf"):
            temp_path = PROJECT_ROOT / "data" / "temp_resume.pdf"
            file.save(temp_path)
            try:
                resume_text = resume_parser.extract_text_from_pdf(temp_path)
            finally:
                if temp_path.exists():
                    temp_path.unlink()
        else:
            resume_text = file.read().decode("utf-8", errors="ignore")
    else:
        data = request.json or {}
        resume_text = data.get("text", "")
        candidate_name = data.get("name")

    if not resume_text.strip():
        return jsonify({"error": "No resume text or file provided"}), 400

    profile = resume_parser.parse_resume_text(resume_text, student_name=candidate_name)
    return jsonify({
        "success": True,
        "profile": profile.to_dict(),
        "extracted_skills_count": len(profile.technical_skills)
    })


@app.route("/api/match", methods=["POST"])
def match_profile():
    data = request.json or {}
    
    # Extract weights if provided
    w_tech = float(data.get("weight_tech", 0.40))
    w_core = float(data.get("weight_core", 0.25))
    w_know = float(data.get("weight_knowledge", 0.15))
    w_sem = float(data.get("weight_semantic", 0.20))
    domain_filter = data.get("domain_filter", None)
    top_k = int(data.get("top_k", 5))

    matcher = PathMatcher(
        data_loader=loader,
        weight_tech=w_tech,
        weight_core=w_core,
        weight_knowledge=w_know,
        weight_semantic=w_sem
    )

    profile_data = data.get("profile")
    if not profile_data:
        return jsonify({"error": "No profile data provided"}), 400

    profile = StudentProfile.from_dict(profile_data)
    onet_recommendations = matcher.match(profile, top_k=top_k, domain_filter=domain_filter)

    # 1. Match active real-world company postings
    company_postings = company_catalog.match_company_postings(
        student=profile,
        top_onet_roles=onet_recommendations,
        limit=6
    )

    # 2. Generate personalized career coaching roadmap for top fit role
    career_coaching_plan = None
    if onet_recommendations:
        career_coaching_plan = career_coach.generate_career_plan(
            student_name=profile.name,
            role=onet_recommendations[0]
        )

    return jsonify({
        "student": profile.to_dict(),
        "recommendations": onet_recommendations,
        "company_postings": company_postings,
        "career_plan": career_coaching_plan
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

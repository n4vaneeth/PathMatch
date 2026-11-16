"""
Unit and integration tests for PathMatch Agentic AI modules:
ResumeParserAgent, CareerCoachAgent, and CompanyInternshipCatalog.
"""

import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agents import ResumeParserAgent, CareerCoachAgent, CompanyInternshipCatalog
from src import StudentProfile, PathMatcher, ONetDataLoader


def test_resume_parser_agent_text_extraction():
    parser = ResumeParserAgent()
    sample_cv = """
    Liam Vance
    Email: liam.vance@university.edu | Phone: (555) 123-4567
    
    Education:
    B.S. in Computer Science & Statistics, Senior
    Relevant Coursework: Machine Learning, Data Structures, Algorithms, Linear Algebra
    
    Skills:
    Languages & Tools: Python, PyTorch, SQL, Pandas, Scikit-Learn, Docker, Git, Linux
    
    Experience & Projects:
    - Trained a deep convolutional neural network using PyTorch on medical images.
    - Extracted 5M transaction records with complex SQL and built predictive pipelines in Scikit-Learn.
    """

    profile = parser.parse_resume_text(sample_cv)
    assert profile.name == "Liam Vance"
    assert "Computer Science" in profile.major
    assert "Undergraduate" in profile.degree_level
    assert "Python" in profile.technical_skills
    assert "PyTorch" in profile.technical_skills
    assert "SQL" in profile.technical_skills
    assert profile.technical_skills["Python"] >= 3.0
    assert "Machine Learning" in profile.coursework


def test_career_coach_agent_roadmap():
    coach = CareerCoachAgent()
    mock_role = {
        "internship_title": "Machine Learning & Data Science Intern",
        "domain": "Artificial Intelligence & Data",
        "match_percentage": 86.4,
        "gap_analysis": {
            "missing_mandatory": [],
            "missing_important": ["TensorFlow"],
            "matched_mandatory": [{"skill": "Python", "proficiency": 5.0}],
            "matched_important": [{"skill": "PyTorch", "proficiency": 4.0}]
        }
    }

    plan = coach.generate_career_plan("Maya Lin", mock_role)
    assert plan["target_role"] == "Machine Learning & Data Science Intern"
    assert plan["primary_gap"] == "TensorFlow"
    assert len(plan["weekly_plan"]) == 4
    assert "Week 1" in plan["weekly_plan"][0]["week"]
    assert len(plan["interview_prep_questions"]) == 3
    assert "TensorFlow" in plan["recommended_project"]["tech_stack"]


def test_company_internship_catalog_matching():
    catalog = CompanyInternshipCatalog()
    assert len(catalog.postings) >= 20

    student = StudentProfile(
        id="test_student",
        name="Alex Rivera",
        major="Software Engineering",
        technical_skills={"JavaScript": 5, "React": 5, "HTML/CSS": 5, "TypeScript": 4, "Git": 4}
    )

    top_onet_roles = [
        {"onet_soc": "15-1254.00", "similarity_score": 0.85},
        {"onet_soc": "15-1252.00", "similarity_score": 0.70}
    ]

    company_matches = catalog.match_company_postings(student, top_onet_roles, limit=5)
    assert len(company_matches) == 5
    top_company = company_matches[0]
    # Meta or Airbnb should be among the top frontend web matches
    companies = [c["company"] for c in company_matches]
    assert any(c in ["Meta", "Airbnb", "Microsoft", "Stripe"] for c in companies)
    assert top_company["match_score"] > 0.60

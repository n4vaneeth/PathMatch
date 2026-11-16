"""
Unit tests for the Flask Web API endpoints of PathMatch.
"""

import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from web.app import app


def test_index_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"PathMatch" in response.data


def test_api_profiles_route():
    client = app.test_client()
    response = client.get("/api/profiles")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 5
    names = [p["name"] for p in data]
    assert "Maya Lin" in names
    assert "Alex Rivera" in names
    assert "Sarah Chen" in names
    assert "David Kim" in names
    assert "Priya Patel" in names


def test_api_domains_route():
    client = app.test_client()
    response = client.get("/api/domains")
    assert response.status_code == 200
    domains = json.loads(response.data)
    assert len(domains) > 0
    assert "Artificial Intelligence & Data" in domains
    assert "Software Engineering" in domains


def test_api_match_route():
    client = app.test_client()
    sample_profile = {
        "id": "test_student",
        "name": "Jordan Smith",
        "major": "Data Science",
        "technical_skills": {
            "Python": 5,
            "Machine Learning": 4,
            "SQL": 4,
            "Pandas": 5
        },
        "core_competencies": {
            "Mathematics": 4.5,
            "Programming": 4.2
        },
        "knowledge_domains": {
            "Mathematics": 4.5,
            "Computers and Electronics": 4.0
        },
        "domain_interests": ["Machine Learning"],
        "coursework": ["Linear Algebra", "Data Mining"],
        "project_experience": "Built an ML pipeline with scikit-learn."
    }

    payload = {
        "profile": sample_profile,
        "weight_tech": 0.40,
        "weight_core": 0.25,
        "weight_knowledge": 0.15,
        "weight_semantic": 0.20,
        "top_k": 3
    }

    response = client.post("/api/match", json=payload)
    assert response.status_code == 200
    res_data = json.loads(response.data)
    assert "recommendations" in res_data
    assert len(res_data["recommendations"]) == 3
    top_role = res_data["recommendations"][0]
    assert top_role["similarity_score"] > 0.60
    assert "Machine Learning" in top_role["internship_title"] or "Data Science" in top_role["internship_title"]
    assert "gap_analysis" in top_role

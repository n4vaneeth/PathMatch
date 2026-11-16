"""
Comprehensive unit and integration test suite for PathMatch Recommendation Engine.
"""

import pytest
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src import (
    StudentProfile,
    ONetDataLoader,
    PathMatcher,
    generate_skill_gap_analysis,
    determine_fit_level
)
from src.data_loader import normalize_skill_name


@pytest.fixture(scope="module")
def data_loader():
    return ONetDataLoader()


@pytest.fixture(scope="module")
def matcher(data_loader):
    return PathMatcher(data_loader=data_loader)


def test_onet_data_loader_integrity(data_loader):
    occupations = data_loader.get_all_occupations()
    assert len(occupations) >= 15, "Expected at least 15 O*NET occupations loaded"
    
    # Check required fields in each occupation
    for occ in occupations:
        assert "onet_soc" in occ
        assert "onet_title" in occ
        assert "internship_title" in occ
        assert "domain" in occ
        assert "technical_skills" in occ
        assert "mandatory" in occ["technical_skills"]
        assert "important" in occ["technical_skills"]
        assert "bonus" in occ["technical_skills"]
        assert "core_competencies" in occ
        assert "knowledge_domains" in occ


def test_skill_name_normalization():
    assert normalize_skill_name("React.js") == "react"
    assert normalize_skill_name("REACTJS") == "react"
    assert normalize_skill_name("K8s") == "kubernetes"
    assert normalize_skill_name("Scikit-Learn") == "scikit-learn"
    assert normalize_skill_name("sklearn") == "scikit-learn"
    assert normalize_skill_name("Python") == "python"
    assert normalize_skill_name("AWS") == "cloud platforms (aws/gcp)"


def test_student_profile_model():
    data = {
        "id": "test_1",
        "name": "Jordan Lee",
        "major": "Computer Engineering",
        "technical_skills": {"Python": 5, "C++": 4},
        "core_competencies": {"Programming": 4.5},
        "knowledge_domains": {"Computers and Electronics": 4.8},
        "domain_interests": ["Embedded Systems"],
        "coursework": ["Digital Logic"],
        "project_experience": "Built microcontroller firmware."
    }
    profile = StudentProfile.from_dict(data)
    assert profile.name == "Jordan Lee"
    assert profile.technical_skills["Python"] == 5.0
    assert "Digital Logic" in profile.coursework
    semantic_text = profile.get_semantic_text()
    assert "Computer Engineering" in semantic_text
    assert "microcontroller" in semantic_text.lower()


def test_fit_tier_classification():
    assert determine_fit_level(0.92) == "Exceptional Fit"
    assert determine_fit_level(0.75) == "Strong Candidate"
    assert determine_fit_level(0.60) == "Competitive with Growth Areas"
    assert determine_fit_level(0.45) == "Stretch Opportunity"
    assert determine_fit_level(0.30) == "Low Alignment"


def test_maya_lin_recommendation(matcher):
    profile_path = PROJECT_ROOT / "sample_profiles" / "student_01_maya_lin.json"
    profile = StudentProfile.from_file(profile_path)
    ranked = matcher.match(profile, top_k=3)
    
    assert len(ranked) == 3
    top_role = ranked[0]
    # Data Science / Machine Learning should be top recommendation
    assert "Machine Learning" in top_role["internship_title"] or "Data Science" in top_role["internship_title"]
    assert top_role["similarity_score"] >= 0.80
    assert top_role["fit_tier"] == "Exceptional Fit"


def test_alex_rivera_recommendation(matcher):
    profile_path = PROJECT_ROOT / "sample_profiles" / "student_02_alex_rivera.json"
    profile = StudentProfile.from_file(profile_path)
    ranked = matcher.match(profile, top_k=3)
    
    top_role = ranked[0]
    assert "Web Development" in top_role["internship_title"] or "Software Engineering" in top_role["internship_title"]
    assert top_role["similarity_score"] >= 0.75


def test_sarah_chen_recommendation(matcher):
    profile_path = PROJECT_ROOT / "sample_profiles" / "student_03_sarah_chen.json"
    profile = StudentProfile.from_file(profile_path)
    ranked = matcher.match(profile, top_k=3)
    
    top_role = ranked[0]
    assert "UI/UX" in top_role["internship_title"] or "Design" in top_role["internship_title"]
    assert top_role["similarity_score"] >= 0.80


def test_david_kim_recommendation(matcher):
    profile_path = PROJECT_ROOT / "sample_profiles" / "student_04_david_kim.json"
    profile = StudentProfile.from_file(profile_path)
    ranked = matcher.match(profile, top_k=3)
    
    top_role = ranked[0]
    assert "Financial" in top_role["internship_title"] or "Investment" in top_role["internship_title"]
    assert top_role["similarity_score"] >= 0.80


def test_priya_patel_recommendation(matcher):
    profile_path = PROJECT_ROOT / "sample_profiles" / "student_05_priya_patel.json"
    profile = StudentProfile.from_file(profile_path)
    ranked = matcher.match(profile, top_k=3)
    
    top_role = ranked[0]
    assert "Cybersecurity" in top_role["internship_title"] or "Security" in top_role["internship_title"]
    assert top_role["similarity_score"] >= 0.85


def test_gap_analysis_generation():
    student_skills = {"Python": 5, "SQL": 4}
    normalized_skills = {"python": 5.0, "sql": 4.0}
    role_skills = {
        "mandatory": ["Python", "Machine Learning", "SQL"],
        "important": ["PyTorch", "Pandas"],
        "bonus": ["Docker"]
    }
    gap = generate_skill_gap_analysis(student_skills, role_skills, normalized_skills, 0.72)
    
    # Missing mandatory skill should be Machine Learning
    assert "Machine Learning" in gap["missing_mandatory"]
    # Matched mandatory skills should be Python and SQL
    matched_mand_names = [m["skill"] for m in gap["matched_mandatory"]]
    assert "Python" in matched_mand_names
    assert "SQL" in matched_mand_names
    assert "Prioritize" in gap["guidance"]


def test_domain_filtering(matcher):
    profile_path = PROJECT_ROOT / "sample_profiles" / "student_01_maya_lin.json"
    profile = StudentProfile.from_file(profile_path)
    
    # Filter by domain
    ranked = matcher.match(profile, top_k=5, domain_filter="Software Engineering")
    for r in ranked:
        assert r["domain"] == "Software Engineering"


def test_custom_weights(data_loader):
    # Matcher with heavy emphasis on technical stack
    matcher_tech_heavy = PathMatcher(
        data_loader=data_loader,
        weight_tech=0.80,
        weight_core=0.10,
        weight_knowledge=0.05,
        weight_semantic=0.05
    )
    profile_path = PROJECT_ROOT / "sample_profiles" / "student_01_maya_lin.json"
    profile = StudentProfile.from_file(profile_path)
    ranked = matcher_tech_heavy.match(profile, top_k=1)
    assert len(ranked) == 1
    assert ranked[0]["similarity_score"] > 0

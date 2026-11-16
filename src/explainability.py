"""
Explainability and skill gap analysis module for PathMatch.
Breaks down match factors, pinpoints missing critical competencies,
and generates actionable learning recommendations.
"""

from typing import Dict, List, Any


def determine_fit_level(score: float) -> str:
    """Classifies percentage similarity score into human-readable readiness tiers."""
    if score >= 0.82:
        return "Exceptional Fit"
    elif score >= 0.70:
        return "Strong Candidate"
    elif score >= 0.55:
        return "Competitive with Growth Areas"
    elif score >= 0.40:
        return "Stretch Opportunity"
    else:
        return "Low Alignment"


def generate_skill_gap_analysis(
    student_skills: Dict[str, float],
    role_skills: Dict[str, List[str]],
    normalized_student_skills: Dict[str, float],
    score: float
) -> Dict[str, Any]:
    """
    Analyzes technical skill overlaps and deficits between a student profile
    and an O*NET role.
    """
    mandatory = role_skills.get("mandatory", [])
    important = role_skills.get("important", [])
    bonus = role_skills.get("bonus", [])

    matched_mandatory = []
    missing_mandatory = []
    for skill in mandatory:
        norm = skill.strip().lower()
        if norm in normalized_student_skills:
            matched_mandatory.append({
                "skill": skill,
                "proficiency": normalized_student_skills[norm]
            })
        else:
            missing_mandatory.append(skill)

    matched_important = []
    missing_important = []
    for skill in important:
        norm = skill.strip().lower()
        if norm in normalized_student_skills:
            matched_important.append({
                "skill": skill,
                "proficiency": normalized_student_skills[norm]
            })
        else:
            missing_important.append(skill)

    matched_bonus = []
    for skill in bonus:
        norm = skill.strip().lower()
        if norm in normalized_student_skills:
            matched_bonus.append({
                "skill": skill,
                "proficiency": normalized_student_skills[norm]
            })

    # Actionable guidance
    recommendations = []
    if missing_mandatory:
        top_missing = missing_mandatory[:2]
        recommendations.append(
            f"Prioritize building foundational competency in {', '.join(top_missing)}."
        )
    if missing_important and len(missing_mandatory) < 2:
        top_imp = missing_important[:2]
        recommendations.append(
            f"Level up complementary tools like {', '.join(top_imp)} to strengthen interview readiness."
        )
    if not missing_mandatory and not missing_important:
        recommendations.append(
            "Excellent technical alignment! Highlight concrete portfolio metrics in your resume."
        )

    return {
        "matched_mandatory": matched_mandatory,
        "missing_mandatory": missing_mandatory,
        "matched_important": matched_important,
        "missing_important": missing_important,
        "matched_bonus": matched_bonus,
        "total_skills_matched": len(matched_mandatory) + len(matched_important) + len(matched_bonus),
        "total_role_skills": len(mandatory) + len(important) + len(bonus),
        "fit_tier": determine_fit_level(score),
        "guidance": " ".join(recommendations)
    }

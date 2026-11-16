"""
Company Internship Matcher for PathMatch.
Maps student competencies to real-world style active internship postings from top tech,
finance, healthcare, and engineering companies aligned with O*NET SOC codes.
"""

from typing import List, Dict, Any, Optional
import json
from pathlib import Path
from ..student_profile import StudentProfile
from ..data_loader import normalize_skill_name


class CompanyInternshipCatalog:
    def __init__(self, data_path: Optional[str | Path] = None):
        if data_path is None:
            data_path = Path(__file__).resolve().parent.parent.parent / "data" / "onet" / "company_internships.json"
        self.data_path = Path(data_path)
        self.postings: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if self.data_path.exists():
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.postings = json.load(f)

    def match_company_postings(
        self,
        student: StudentProfile,
        top_onet_roles: List[Dict[str, Any]],
        limit: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Ranks real-world company postings based on the student's top O*NET career pathways
        and specific company skill requirement overlap.
        """
        if not self.postings:
            return []

        student_skills_norm = {
            normalize_skill_name(k): v for k, v in student.technical_skills.items()
        }

        # Map top SOC codes and their scores
        soc_score_map = {r["onet_soc"]: r["similarity_score"] for r in top_onet_roles}

        scored_postings = []
        for post in self.postings:
            soc = post["onet_soc"]
            base_onet_score = soc_score_map.get(soc, 0.30)

            # Calculate specific company requirement overlap
            req_skills = [normalize_skill_name(s) for s in post.get("required_skills", [])]
            matched_req = [s for s in req_skills if s in student_skills_norm]
            req_ratio = len(matched_req) / len(req_skills) if req_skills else 0.5

            pref_skills = [normalize_skill_name(s) for s in post.get("preferred_skills", [])]
            matched_pref = [s for s in pref_skills if s in student_skills_norm]
            pref_ratio = len(matched_pref) / len(pref_skills) if pref_skills else 0.0

            # Combined company match score
            company_score = (0.50 * base_onet_score) + (0.35 * req_ratio) + (0.15 * pref_ratio)
            company_score = min(0.99, max(0.10, company_score))

            scored_postings.append({
                "id": post["id"],
                "company": post["company"],
                "company_domain": post["company_domain"],
                "role_title": post["role_title"],
                "onet_soc": post["onet_soc"],
                "location": post["location"],
                "stipend": post["stipend"],
                "deadline": post["deadline"],
                "match_score": round(company_score, 4),
                "match_percentage": round(company_score * 100, 1),
                "matched_requirements": [post["required_skills"][i] for i, s in enumerate(req_skills) if s in student_skills_norm],
                "missing_requirements": [post["required_skills"][i] for i, s in enumerate(req_skills) if s not in student_skills_norm],
                "matched_preferred": [post["preferred_skills"][i] for i, s in enumerate(pref_skills) if s in student_skills_norm],
                "description": post["description"]
            })

        # Sort descending by match score
        scored_postings.sort(key=lambda x: x["match_score"], reverse=True)
        return scored_postings[:limit]

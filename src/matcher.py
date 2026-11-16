"""
Core Recommendation Engine for PathMatch.
Computes multi-dimensional similarity between student profiles and O*NET occupational roles.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .student_profile import StudentProfile
from .data_loader import ONetDataLoader, normalize_skill_name
from .explainability import generate_skill_gap_analysis, determine_fit_level


class PathMatcher:
    def __init__(
        self,
        data_loader: Optional[ONetDataLoader] = None,
        weight_tech: float = 0.40,
        weight_core: float = 0.25,
        weight_knowledge: float = 0.15,
        weight_semantic: float = 0.20
    ):
        self.data_loader = data_loader or ONetDataLoader()
        
        # Normalize weights so they sum to 1.0
        total_weight = weight_tech + weight_core + weight_knowledge + weight_semantic
        self.w_tech = weight_tech / total_weight
        self.w_core = weight_core / total_weight
        self.w_know = weight_knowledge / total_weight
        self.w_sem = weight_semantic / total_weight

    def _compute_tech_score(
        self,
        student_skills_norm: Dict[str, float],
        role_skills: Dict[str, List[str]]
    ) -> float:
        """
        Calculates technical competency match considering mandatory,
        important, and bonus skills weighted by student proficiency.
        """
        w_mandatory = 1.5
        w_important = 1.0
        w_bonus = 0.5

        mandatory = [normalize_skill_name(s) for s in role_skills.get("mandatory", [])]
        important = [normalize_skill_name(s) for s in role_skills.get("important", [])]
        bonus = [normalize_skill_name(s) for s in role_skills.get("bonus", [])]

        req_sum = len(mandatory) * w_mandatory + len(important) * w_important
        if req_sum == 0:
            return 0.5

        earned = 0.0
        mandatory_matched = 0

        for skill in mandatory:
            if skill in student_skills_norm:
                prof = student_skills_norm[skill]
                # Proficiency on 1-5 scale normalized
                earned += w_mandatory * (prof / 5.0)
                mandatory_matched += 1

        for skill in important:
            if skill in student_skills_norm:
                prof = student_skills_norm[skill]
                earned += w_important * (prof / 5.0)

        for skill in bonus:
            if skill in student_skills_norm:
                prof = student_skills_norm[skill]
                earned += w_bonus * (prof / 5.0)

        raw_score = min(1.0, earned / req_sum)

        # Apply mandatory coverage multiplier
        if mandatory:
            coverage = mandatory_matched / len(mandatory)
            # Penalizes if zero mandatory skills matched, smoothly ramps up
            score = raw_score * (0.35 + 0.65 * coverage)
        else:
            score = raw_score

        return float(np.clip(score, 0.0, 1.0))

    def _compute_vector_cosine(
        self,
        student_vec: Dict[str, float],
        role_vec: Dict[str, float]
    ) -> float:
        """
        Calculates cosine similarity between two dimensional rating vectors.
        """
        keys = list(set(student_vec.keys()).union(set(role_vec.keys())))
        if not keys:
            return 0.5

        v1 = np.array([student_vec.get(k, 2.5) for k in keys], dtype=float)
        v2 = np.array([role_vec.get(k, 2.5) for k in keys], dtype=float)

        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.5

        cos = np.dot(v1, v2) / (norm1 * norm2)
        # Cosine of non-negative ratings usually ranges in [0.7, 1.0];
        # rescales to [0.0, 1.0] for high contrast discrimination
        scaled = (cos - 0.70) / 0.30
        return float(np.clip(scaled, 0.0, 1.0))

    def _compute_semantic_scores(self, student_text: str) -> np.ndarray:
        """
        Computes cosine similarity of student textual profile
        against all O*NET role documents via pre-fitted TF-IDF.
        """
        student_tfidf = self.data_loader.tfidf_vectorizer.transform([student_text])
        sims = cosine_similarity(student_tfidf, self.data_loader.role_tfidf_matrix)[0]
        # Soft scale to reward strong semantic overlaps
        return np.clip(sims * 1.8, 0.0, 1.0)

    def match(
        self,
        student: StudentProfile,
        top_k: int = 5,
        domain_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Evaluates student profile against all O*NET occupational roles,
        returns top-K ranked recommendations with full sub-score breakdowns.
        """
        # Normalize student skills for fast lookup
        student_skills_norm = {
            normalize_skill_name(k): v for k, v in student.technical_skills.items()
        }

        # Compute semantic similarities in batch
        student_text = student.get_semantic_text()
        semantic_sims = self._compute_semantic_scores(student_text)

        ranked_results = []
        occupations = self.data_loader.get_all_occupations()

        for idx, occ in enumerate(occupations):
            if domain_filter and domain_filter.lower() != "all":
                if occ["domain"].lower() != domain_filter.lower():
                    continue

            # 1. Tech Compatibility Score
            tech_score = self._compute_tech_score(
                student_skills_norm,
                occ["technical_skills"]
            )

            # 2. O*NET Core Competencies Alignment Score
            core_score = self._compute_vector_cosine(
                student.core_competencies,
                occ.get("core_competencies", {})
            )

            # 3. Knowledge Domains Alignment Score
            knowledge_score = self._compute_vector_cosine(
                student.knowledge_domains,
                occ.get("knowledge_domains", {})
            )

            # 4. Semantic Experience Score
            sem_score = float(semantic_sims[idx])

            # Composite Weighted Score
            composite = (
                self.w_tech * tech_score +
                self.w_core * core_score +
                self.w_know * knowledge_score +
                self.w_sem * sem_score
            )
            composite = float(np.clip(composite, 0.0, 1.0))

            # Explainability and Skill Gap Analysis
            gap_analysis = generate_skill_gap_analysis(
                student.technical_skills,
                occ["technical_skills"],
                student_skills_norm,
                composite
            )

            ranked_results.append({
                "rank": 0,
                "onet_soc": occ["onet_soc"],
                "onet_title": occ["onet_title"],
                "internship_title": occ["internship_title"],
                "domain": occ["domain"],
                "similarity_score": round(composite, 4),
                "match_percentage": round(composite * 100, 1),
                "fit_tier": determine_fit_level(composite),
                "sub_scores": {
                    "technical_stack": round(tech_score, 4),
                    "core_competencies": round(core_score, 4),
                    "knowledge_domains": round(knowledge_score, 4),
                    "semantic_experience": round(sem_score, 4)
                },
                "summary": occ["summary"],
                "tasks": occ.get("tasks", []),
                "gap_analysis": gap_analysis
            })

        # Sort descending by composite score
        ranked_results.sort(key=lambda x: x["similarity_score"], reverse=True)

        # Assign rank numbers
        for rank_num, item in enumerate(ranked_results, 1):
            item["rank"] = rank_num

        return ranked_results[:top_k]

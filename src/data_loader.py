"""
Data loader and preprocessor for O*NET occupational database.
Handles taxonomy ingestion, synonym normalization, and TF-IDF semantic indexing.
"""

from typing import List, Dict, Any, Optional
import json
from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer


# Common skill aliases and synonyms for flexible matching
SKILL_SYNONYMS: Dict[str, str] = {
    "react.js": "react",
    "reactjs": "react",
    "node": "node.js",
    "nodejs": "node.js",
    "vue.js": "vue",
    "vuejs": "vue",
    "nextjs": "next.js",
    "ts": "typescript",
    "js": "javascript",
    "py": "python",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "k8s": "kubernetes",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "aws": "cloud platforms (aws/gcp)",
    "gcp": "cloud platforms (aws/gcp)",
    "azure": "cloud platforms (aws/gcp)",
    "cloud": "cloud platforms (aws/gcp)",
    "html": "html/css",
    "css": "html/css",
    "ui": "ui/ux design",
    "ux": "ui/ux design",
    "ui/ux": "ui/ux design",
    "user experience": "ui/ux design",
    "product design": "ui/ux design",
    "financial modeling": "financial modeling",
    "dcf": "valuation",
    "excel": "excel (advanced)",
    "advanced excel": "excel (advanced)",
    "bash": "bash scripting",
    "shell": "bash scripting",
    "shell scripting": "bash scripting",
    "ros": "ros/ros2",
    "ros2": "ros/ros2",
    "transformers": "transformers (huggingface)",
    "huggingface": "transformers (huggingface)",
    "rest api": "rest apis",
    "restful api": "rest apis",
    "restful apis": "rest apis",
    "ci cd": "ci/cd",
    "cicd": "ci/cd"
}


def normalize_skill_name(skill: str) -> str:
    """Standardizes skill name by lowercasing, stripping punctuation, and mapping aliases."""
    cleaned = skill.strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return SKILL_SYNONYMS.get(cleaned, cleaned)


class ONetDataLoader:
    def __init__(self, data_path: Optional[str | Path] = None):
        if data_path is None:
            data_path = Path(__file__).resolve().parent.parent / "data" / "onet" / "occupations.json"
        self.data_path = Path(data_path)
        self.occupations: List[Dict[str, Any]] = []
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.role_corpus: List[str] = []
        self.role_tfidf_matrix = None
        self._load_data()

    def _load_data(self) -> None:
        if not self.data_path.exists():
            raise FileNotFoundError(f"O*NET dataset not found at {self.data_path}")
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.occupations = json.load(f)
        
        # Build semantic corpus for each role:
        # includes title, summary, tasks, technical skills, and domain
        self.role_corpus = []
        for occ in self.occupations:
            tech_mandatory = " ".join(occ["technical_skills"].get("mandatory", []))
            tech_important = " ".join(occ["technical_skills"].get("important", []))
            tech_bonus = " ".join(occ["technical_skills"].get("bonus", []))
            tasks_str = " ".join(occ.get("tasks", []))
            
            doc = (
                f"{occ['onet_title']} {occ['internship_title']} {occ['domain']} "
                f"{occ['summary']} {tasks_str} {tech_mandatory} {tech_important} {tech_bonus}"
            )
            self.role_corpus.append(doc)

        self.role_tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.role_corpus)

    def get_all_occupations(self) -> List[Dict[str, Any]]:
        return self.occupations

    def get_occupation_by_soc(self, soc_code: str) -> Optional[Dict[str, Any]]:
        for occ in self.occupations:
            if occ["onet_soc"] == soc_code:
                return occ
        return None

    def get_unique_domains(self) -> List[str]:
        return sorted(list(set(occ["domain"] for occ in self.occupations)))

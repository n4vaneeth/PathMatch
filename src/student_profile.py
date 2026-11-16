"""
Student Profile data model for PathMatch Internship Recommendation Engine.
Provides structured representation, validation, and feature vector extraction.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass
class StudentProfile:
    id: str
    name: str
    major: str
    degree_level: str = "Undergraduate"
    gpa: Optional[float] = None
    technical_skills: Dict[str, float] = field(default_factory=dict)
    core_competencies: Dict[str, float] = field(default_factory=dict)
    knowledge_domains: Dict[str, float] = field(default_factory=dict)
    domain_interests: List[str] = field(default_factory=list)
    coursework: List[str] = field(default_factory=list)
    project_experience: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StudentProfile":
        return cls(
            id=data.get("id", "student_unknown"),
            name=data.get("name", "Anonymous Student"),
            major=data.get("major", "Undeclared"),
            degree_level=data.get("degree_level", "Undergraduate"),
            gpa=data.get("gpa"),
            technical_skills={k: float(v) for k, v in data.get("technical_skills", {}).items()},
            core_competencies={k: float(v) for k, v in data.get("core_competencies", {}).items()},
            knowledge_domains={k: float(v) for k, v in data.get("knowledge_domains", {}).items()},
            domain_interests=data.get("domain_interests", []),
            coursework=data.get("coursework", []),
            project_experience=data.get("project_experience", "")
        )

    @classmethod
    def from_file(cls, filepath: str | Path) -> "StudentProfile":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "major": self.major,
            "degree_level": self.degree_level,
            "gpa": self.gpa,
            "technical_skills": self.technical_skills,
            "core_competencies": self.core_competencies,
            "knowledge_domains": self.knowledge_domains,
            "domain_interests": self.domain_interests,
            "coursework": self.coursework,
            "project_experience": self.project_experience
        }

    def get_semantic_text(self) -> str:
        """
        Combines major, coursework, domain interests, and project experience
        into a coherent textual representation for semantic/NLP indexing.
        """
        parts = [
            f"Major: {self.major}",
            f"Interests: {', '.join(self.domain_interests)}",
            f"Coursework: {', '.join(self.coursework)}",
            f"Experience: {self.project_experience}"
        ]
        return " | ".join(parts)

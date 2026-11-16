"""
PathMatch — Internship Recommendation Engine.
Built using the O*NET Occupational Database taxonomy with Agentic AI capabilities.
"""

from .student_profile import StudentProfile
from .data_loader import ONetDataLoader
from .matcher import PathMatcher
from .explainability import generate_skill_gap_analysis, determine_fit_level
from .report_generator import format_terminal_report, generate_markdown_summary
from .agents import ResumeParserAgent, CareerCoachAgent, CompanyInternshipCatalog

__all__ = [
    "StudentProfile",
    "ONetDataLoader",
    "PathMatcher",
    "generate_skill_gap_analysis",
    "determine_fit_level",
    "format_terminal_report",
    "generate_markdown_summary",
    "ResumeParserAgent",
    "CareerCoachAgent",
    "CompanyInternshipCatalog"
]

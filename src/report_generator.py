"""
Report generator for PathMatch recommendation engine.
Formats ranked internship outputs into terminal summaries, Markdown, and JSON.
"""

from typing import List, Dict, Any
from pathlib import Path


def format_terminal_report(student_name: str, major: str, ranked_roles: List[Dict[str, Any]]) -> str:
    lines = []
    lines.append("=" * 80)
    lines.append(f"  PATHMATCH INTERNSHIP RECOMMENDATIONS: {student_name.upper()}")
    lines.append(f"  Academic Background: {major}")
    lines.append("=" * 80)

    for role in ranked_roles:
        score_pct = role["match_percentage"]
        tier = role["fit_tier"]
        lines.append(f"\n[#{role['rank']}] {role['internship_title']} ({role['domain']})")
        lines.append(f"     O*NET-SOC Code: {role['onet_soc']} | Official Title: {role['onet_title']}")
        lines.append(f"     Match Score:    {score_pct:.1f}% [{tier}]")
        
        subs = role["sub_scores"]
        lines.append(
            f"     Score Breakdown: Tech: {subs['technical_stack']*100:.1f}% | "
            f"Core: {subs['core_competencies']*100:.1f}% | "
            f"Knowledge: {subs['knowledge_domains']*100:.1f}% | "
            f"Semantic: {subs['semantic_experience']*100:.1f}%"
        )
        
        gap = role["gap_analysis"]
        matched_str = ", ".join([f"{m['skill']} (lvl {int(m['proficiency'])})" for m in gap["matched_mandatory"] + gap["matched_important"]]) or "None"
        missing_m = ", ".join(gap["missing_mandatory"]) or "None"
        missing_i = ", ".join(gap["missing_important"]) or "None"

        lines.append(f"     Matched Skills:   {matched_str}")
        if missing_m != "None":
            lines.append(f"     Critical Gaps:    {missing_m}")
        if missing_i != "None":
            lines.append(f"     Secondary Gaps:   {missing_i}")
        lines.append(f"     Guidance:         {gap['guidance']}")
        lines.append("-" * 80)

    return "\n".join(lines)


def generate_markdown_summary(student_name: str, major: str, ranked_roles: List[Dict[str, Any]]) -> str:
    md = []
    md.append(f"### Internship Matches for **{student_name}** (*{major}*)")
    md.append("")
    md.append("| Rank | Recommended Internship Role | O*NET SOC | Domain | Match Score | Fit Tier | Key Matched Skills | Critical Skill Gaps |")
    md.append("| :---: | :--- | :---: | :--- | :---: | :---: | :--- | :--- |")

    for r in ranked_roles:
        gap = r["gap_analysis"]
        matched = ", ".join([m["skill"] for m in gap["matched_mandatory"][:3]])
        gaps = ", ".join(gap["missing_mandatory"][:2]) or "No critical gaps"
        md.append(
            f"| **#{r['rank']}** | **{r['internship_title']}** | `{r['onet_soc']}` | {r['domain']} | **{r['match_percentage']}%** | `{r['fit_tier']}` | {matched} | *{gaps}* |"
        )
    md.append("")
    return "\n".join(md)

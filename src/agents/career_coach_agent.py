"""
AI Career Coach Agent for PathMatch.
Synthesizes personalized 30-day upskilling roadmaps, portfolio project proposals,
and technical interview prep tailored to bridge identified skill gaps.
"""

from typing import Dict, List, Any


class CareerCoachAgent:
    def __init__(self):
        pass

    def generate_career_plan(
        self,
        student_name: str,
        role: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a structured 4-week upskilling roadmap and project plan
        specifically tailored to the top recommended internship role.
        """
        role_title = role["internship_title"]
        domain = role["domain"]
        score_pct = role["match_percentage"]
        gap = role["gap_analysis"]
        missing_mandatory = gap.get("missing_mandatory", [])
        missing_important = gap.get("missing_important", [])
        matched_skills = [m["skill"] for m in gap.get("matched_mandatory", []) + gap.get("matched_important", [])]

        primary_gap = missing_mandatory[0] if missing_mandatory else (missing_important[0] if missing_important else "Advanced Optimization")
        secondary_gap = missing_mandatory[1] if len(missing_mandatory) > 1 else (missing_important[0] if missing_important and missing_mandatory else "System Architecture")

        # 4-Week Roadmap
        weekly_plan = [
            {
                "week": "Week 1",
                "phase": "Foundational Tooling & Core Prerequisite Setup",
                "goal": f"Set up working development environments and master baseline concepts for {primary_gap}.",
                "milestones": [
                    f"Read official documentation and architectural patterns for {primary_gap}.",
                    f"Implement 2 basic 'Hello World' and CRUD starter workflows incorporating {primary_gap}.",
                    "Analyze 3 top open-source repositories using this tool in production."
                ]
            },
            {
                "week": "Week 2",
                "phase": f"Deep Dive: Mastering {primary_gap}",
                "goal": f"Bridge the critical skill gap by building a non-trivial functional module.",
                "milestones": [
                    f"Build a feature using {primary_gap} connected with your existing skill in {matched_skills[0] if matched_skills else 'core stack'}.",
                    f"Integrate error logging, automated testing, and CI/CD validation.",
                    f"Begin exploring complementary tooling ({secondary_gap})."
                ]
            },
            {
                "week": "Week 3",
                "phase": "High-Impact Portfolio Capstone Project",
                "goal": f"Construct an end-to-end demonstrable project targeting the {role_title} requirements.",
                "milestones": [
                    f"Build an end-to-end repository featuring {primary_gap} and {matched_skills[0] if matched_skills else 'data APIs'}.",
                    "Write a professional README with architectural diagrams, latency benchmarks, and installation instructions.",
                    "Record a 2-minute Loom/demo GIF showcasing real-time functionality."
                ]
            },
            {
                "week": "Week 4",
                "phase": "Interview Prep & Resume Storytelling",
                "goal": f"Perfect technical storytelling and solve mock interview problems for {role_title}.",
                "milestones": [
                    "Draft STAR-format resume bullet points highlighting business impact and metrics.",
                    "Practice live whiteboarding questions on data flows and system design.",
                    "Reach out to 2 alumni or engineers currently working in this role for informational interviews."
                ]
            }
        ]

        # Recommended Project Idea
        project_idea = {
            "title": f"Production-Ready {role_title} Showcase Application",
            "tech_stack": [primary_gap] + matched_skills[:3],
            "description": f"Build a full-stack, tested application combining your mastery of {matched_skills[0] if matched_skills else 'programming'} with new capability in {primary_gap} to solve a real user problem with measurable performance.",
            "metrics_to_highlight": "Target sub-100ms response times, 90%+ test coverage, and automated deployment."
        }

        # Interview Questions to Expect
        interview_questions = [
            f"Can you explain how {primary_gap} works under the hood and why you would choose it over alternatives?",
            f"Walk me through a challenging bug you encountered in {matched_skills[0] if matched_skills else 'your previous project'} and how you debugged it.",
            f"How would you architect a scalable system to perform the core tasks of a {role_title}?"
        ]

        return {
            "target_role": role_title,
            "domain": domain,
            "current_fit_score": f"{score_pct}%",
            "primary_gap": primary_gap,
            "weekly_plan": weekly_plan,
            "recommended_project": project_idea,
            "interview_prep_questions": interview_questions
        }

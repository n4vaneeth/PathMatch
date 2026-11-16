"""
Sample student profiles generator for PathMatch.
Generates 5 realistic, diverse student profiles across different disciplines:
1. Maya Lin (Machine Learning & Data Science)
2. Alex Rivera (Full-Stack & Web Engineering)
3. Sarah Chen (UI/UX & Product Design)
4. David Kim (Finance & Quantitative Analytics)
5. Priya Patel (Cybersecurity & Systems)
"""

import json
from pathlib import Path

SAMPLE_PROFILES = [
    {
        "id": "student_01",
        "name": "Maya Lin",
        "major": "Computer Science & Statistics",
        "degree_level": "Undergraduate (Junior)",
        "gpa": 3.85,
        "technical_skills": {
            "Python": 5,
            "Machine Learning": 4,
            "PyTorch": 4,
            "SQL": 4,
            "Pandas": 5,
            "Scikit-Learn": 4,
            "NumPy": 5,
            "Data Visualization": 4,
            "Linear Algebra": 4,
            "Statistics": 4,
            "Git": 4,
            "Docker": 2,
            "NLP": 3
        },
        "core_competencies": {
            "Mathematics": 4.8,
            "Programming": 4.4,
            "Complex Problem Solving": 4.5,
            "Critical Thinking": 4.5,
            "Active Learning": 4.6,
            "Systems Analysis": 3.9
        },
        "knowledge_domains": {
            "Mathematics": 4.8,
            "Computers and Electronics": 4.4,
            "Engineering and Technology": 3.6,
            "Administration and Management": 2.2
        },
        "domain_interests": [
            "Artificial Intelligence",
            "Machine Learning Research",
            "Predictive Analytics",
            "Data Science"
        ],
        "coursework": [
            "Data Structures & Algorithms",
            "Deep Learning",
            "Applied Statistical Models",
            "Multivariable Calculus & Linear Algebra",
            "Database Systems"
        ],
        "project_experience": "Trained an end-to-end convolutional neural network for medical image classification using PyTorch. Built exploratory data pipelines in Pandas and Scikit-Learn predicting customer lifetime value with 92% ROC-AUC. Deployed model inference endpoint using FastAPI and Docker."
    },
    {
        "id": "student_02",
        "name": "Alex Rivera",
        "major": "Software Engineering",
        "degree_level": "Undergraduate (Sophomore)",
        "gpa": 3.72,
        "technical_skills": {
            "JavaScript": 5,
            "TypeScript": 4,
            "React": 5,
            "Node.js": 4,
            "HTML/CSS": 5,
            "Tailwind CSS": 4,
            "REST APIs": 4,
            "PostgreSQL": 3,
            "Git": 4,
            "Docker": 2,
            "Python": 3,
            "Agile/Scrum": 3,
            "Responsive Design": 4
        },
        "core_competencies": {
            "Programming": 4.5,
            "Complex Problem Solving": 4.0,
            "Operations Analysis": 4.1,
            "Critical Thinking": 3.9,
            "Active Learning": 4.0,
            "Systems Analysis": 3.7
        },
        "knowledge_domains": {
            "Computers and Electronics": 4.6,
            "Design": 4.0,
            "Engineering and Technology": 3.8,
            "Communications and Media": 3.5
        },
        "domain_interests": [
            "Full Stack Web Development",
            "Frontend Engineering",
            "Cloud Web Applications",
            "Developer Tools"
        ],
        "coursework": [
            "Software Architecture & Design",
            "Web Application Development",
            "Database Management",
            "Object-Oriented Programming"
        ],
        "project_experience": "Engineered a collaborative real-time kanban board web application with React, TypeScript, and Node.js Express REST API. Built responsive client UI with Tailwind CSS and integrated PostgreSQL storage with automated GitHub Actions CI/CD workflows."
    },
    {
        "id": "student_03",
        "name": "Sarah Chen",
        "major": "Cognitive Science & Human-Computer Interaction",
        "degree_level": "Undergraduate (Junior)",
        "gpa": 3.91,
        "technical_skills": {
            "Figma": 5,
            "UI/UX Design": 5,
            "Wireframing": 5,
            "Prototyping": 5,
            "User Research": 4,
            "Usability Testing": 4,
            "Design Systems": 4,
            "Information Architecture": 4,
            "Adobe XD": 3,
            "HTML/CSS": 3,
            "Storyboarding": 4,
            "Notion": 4,
            "Interaction Design": 4
        },
        "core_competencies": {
            "Social Perceptiveness": 4.8,
            "Active Listening": 4.7,
            "Complex Problem Solving": 4.0,
            "Critical Thinking": 4.2,
            "Operations Analysis": 4.1,
            "Speaking": 4.4,
            "Programming": 2.0
        },
        "knowledge_domains": {
            "Design": 5.0,
            "Communications and Media": 4.6,
            "Psychology": 4.5,
            "Computers and Electronics": 3.5,
            "Customer and Personal Service": 4.4
        },
        "domain_interests": [
            "Product Design",
            "User Experience Research",
            "Design Systems",
            "Digital Accessibility",
            "Interaction Design"
        ],
        "coursework": [
            "User-Centered Design Methods",
            "Cognitive Psychology & Perception",
            "Interactive Media Systems",
            "Qualitative Research Methods",
            "Visual Communication Design"
        ],
        "project_experience": "Redesigned a campus dining navigation mobile app through 12 in-depth user interviews, heuristic evaluations, interactive Figma prototyping, and usability testing with 30 students, reducing task completion time by 35%."
    },
    {
        "id": "student_04",
        "name": "David Kim",
        "major": "Finance & Computational Economics",
        "degree_level": "Undergraduate (Senior)",
        "gpa": 3.88,
        "technical_skills": {
            "Financial Modeling": 5,
            "Excel (Advanced)": 5,
            "Valuation": 4,
            "Financial Statement Analysis": 4,
            "Accounting": 4,
            "SQL": 4,
            "Python": 3,
            "Power BI": 4,
            "Tableau": 3,
            "Statistics": 4,
            "Risk Analysis": 3,
            "Corporate Finance": 4,
            "VBA": 3
        },
        "core_competencies": {
            "Mathematics": 4.5,
            "Critical Thinking": 4.6,
            "Complex Problem Solving": 4.3,
            "Judgment and Decision Making": 4.4,
            "Writing": 4.1,
            "Speaking": 4.0
        },
        "knowledge_domains": {
            "Economics and Accounting": 5.0,
            "Mathematics": 4.5,
            "Administration and Management": 4.2,
            "Computers and Electronics": 3.3
        },
        "domain_interests": [
            "Investment Banking",
            "Financial Analytics",
            "Portfolio Valuation",
            "Corporate Finance",
            "Capital Markets"
        ],
        "coursework": [
            "Corporate Finance & Valuation",
            "Financial Econometrics",
            "Intermediate Accounting I & II",
            "Derivatives & Risk Management",
            "Statistical Data Analysis"
        ],
        "project_experience": "Constructed dynamic 3-statement financial forecast models and discounted cash flow (DCF) valuation models in Excel for M&A tech transactions. Extracted corporate revenue metrics with complex SQL queries and visualized performance KPIs in Power BI."
    },
    {
        "id": "student_05",
        "name": "Priya Patel",
        "major": "Cybersecurity & Information Assurance",
        "degree_level": "Undergraduate (Junior)",
        "gpa": 3.79,
        "technical_skills": {
            "Network Security": 5,
            "Linux": 4,
            "Python": 4,
            "Wireshark": 4,
            "Vulnerability Assessment": 4,
            "SIEM": 3,
            "Cryptography": 4,
            "Firewall Configuration": 4,
            "Bash Scripting": 4,
            "Git": 4,
            "Docker": 3,
            "Cloud Platforms (AWS/GCP)": 3,
            "OWASP Top 10": 3
        },
        "core_competencies": {
            "Systems Analysis": 4.7,
            "Complex Problem Solving": 4.6,
            "Critical Thinking": 4.5,
            "Judgment and Decision Making": 4.3,
            "Operations Monitoring": 4.3,
            "Programming": 3.8
        },
        "knowledge_domains": {
            "Computers and Electronics": 4.9,
            "Telecommunications": 4.5,
            "Engineering and Technology": 4.1,
            "Law and Government": 3.6
        },
        "domain_interests": [
            "Cybersecurity Operations",
            "Network Defense",
            "Threat Intelligence & Incident Response",
            "Cloud Security",
            "Vulnerability Research"
        ],
        "coursework": [
            "Computer Network Security",
            "Applied Cryptography",
            "Operating Systems & Linux Administration",
            "Defensive Cyber Operations",
            "Ethical Hacking & Penetration Testing"
        ],
        "project_experience": "Configured a home virtual SOC lab analyzing Suricata IDS intrusion alerts and Wireshark PCAPs. Built an automated vulnerability scanning script in Python that audits open firewall ports, misconfigurations, and weak SSL/TLS certificates."
    }
]

def generate_profiles():
    target_dir = Path("sample_profiles")
    target_dir.mkdir(parents=True, exist_ok=True)
    
    for profile in SAMPLE_PROFILES:
        filename = f"{profile['id']}_{profile['name'].lower().replace(' ', '_')}.json"
        filepath = target_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)
        print(f"Saved profile: {filepath}")

if __name__ == "__main__":
    generate_profiles()

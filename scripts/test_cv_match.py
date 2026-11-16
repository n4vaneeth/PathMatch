import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agents import ResumeParserAgent, CompanyInternshipCatalog
from src import PathMatcher, ONetDataLoader

parser = ResumeParserAgent()
pdf_path = Path("D:/12317238_NavaneethS.pdf")
if pdf_path.exists():
    text = parser.extract_text_from_pdf(pdf_path)
    profile = parser.parse_resume_text(text)
    print("Candidate Name:", profile.name)
    print("Major:", profile.major)
    print("Degree:", profile.degree_level)
    print(f"Skills Found ({len(profile.technical_skills)}):", sorted(list(profile.technical_skills.keys())))

    loader = ONetDataLoader()
    matcher = PathMatcher(data_loader=loader)
    results = matcher.match(profile, top_k=3)

    print("\n--- O*NET TOP MATCHES ---")
    for r in results:
        print(f"#{r['rank']} {r['internship_title']} -> {r['match_percentage']}% [{r['fit_tier']}]")
        matched = [m['skill'] for m in r['gap_analysis']['matched_mandatory'] + r['gap_analysis']['matched_important']]
        print("   Matched:", matched)
        print("   Gaps:", r['gap_analysis']['missing_mandatory'])

    catalog = CompanyInternshipCatalog()
    company_matches = catalog.match_company_postings(profile, results, limit=3)
    print("\n--- COMPANY MATCHES ---")
    for c in company_matches:
        print(f"[{c['company']}] {c['role_title']} -> {c['match_percentage']}% Match")
else:
    print("CV not found at D:/12317238_NavaneethS.pdf")

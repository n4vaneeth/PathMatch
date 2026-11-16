"""
Script to execute the PathMatch Internship Recommendation Engine
across all 5 sample student profiles.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import json
from src import StudentProfile, ONetDataLoader, PathMatcher, format_terminal_report, generate_markdown_summary


def main():
    print("=" * 80)
    print("  INITIALIZING PATHMATCH INTERNSHIP RECOMMENDATION ENGINE")
    print("  Dataset: O*NET Occupational Database (Content Model Taxonomy)")
    print("=" * 80)

    # Initialize data loader and matcher
    loader = ONetDataLoader()
    matcher = PathMatcher(data_loader=loader)
    print(f"Loaded {len(loader.get_all_occupations())} O*NET occupational internship profiles.\n")

    profile_dir = Path("sample_profiles")
    profile_files = sorted(list(profile_dir.glob("student_*.json")))

    all_recommendations = {}

    for pfile in profile_files:
        profile = StudentProfile.from_file(pfile)
        ranked = matcher.match(profile, top_k=5)
        all_recommendations[profile.id] = {
            "profile": profile.to_dict(),
            "recommendations": ranked
        }

        # Print formatted report to terminal
        print(format_terminal_report(profile.name, profile.major, ranked))
        print("\n")

    # Save output summary
    output_path = Path("sample_profiles") / "ranked_outputs_summary.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_recommendations, f, indent=2)
    print(f"Saved full recommendation JSON outputs to {output_path}")


if __name__ == "__main__":
    main()

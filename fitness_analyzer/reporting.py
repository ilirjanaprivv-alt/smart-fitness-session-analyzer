import csv
from pathlib import Path


def write_analysis_summary(reports, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    summary_file = output_path / "analysis_summary.csv"

    fieldnames = [
        "session_id",
        "participant_id",
        "usable_observations",
        "classification",
        "average_heart_rate",
        "average_activity_level",
        "average_signal_quality"
    ]

    with open(summary_file, "w", encoding="utf-8", newline="") as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for report in reports:
            heart_rate_summary = report.get("heart_rate_summary", {})

            activity_summary = report.get("activity_level_summary", {})

            signal_quality_summary = report.get("signal_quality_summary", {})

            writer.writerow({
                "session_id": report["session_id"],
                "participant_id": report["participant_id"],
                "usable_observations": report["usable_observations"],
                "classification": report["classification"],
                "average_heart_rate": heart_rate_summary.get("average", ""),
                "average_activity_level": activity_summary.get("average", ""),
                "average_signal_quality": signal_quality_summary.get("average", "")
            })

    return summary_file
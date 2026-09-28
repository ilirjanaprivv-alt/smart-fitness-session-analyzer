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

def write_analysis_report(reports, output_dir): 
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    report_file = output_path / "analysis_report.txt"

    with open(report_file, "w", encoding="utf-8") as file:

        for report in reports:
            file.write("--- FITNESS SESSION REPORT ---\n")

            file.write("\nSession:\n")
            file.write(
                f"Session ID: {report['session_id']}\n"
            )

            file.write("\nParticipant:\n")
            file.write(
                f"Participant ID: {report['participant_id']}\n"
            )
            file.write(
                f"Baseline Heart Rate: "
                f"{report['baseline_heart_rate']}\n"
            )
            file.write(
                f"Baseline Skin Response: "
                f"{report['baseline_skin_response']}\n"
            )
            file.write(
                f"Baseline Temperature: "
                f"{report['baseline_temperature']}\n"
            )

            file.write("\nObservations:\n")
            file.write(
                f"Total Observations: "
                f"{report['total_observations']}\n"
            )
            file.write(
                f"Usable Observations: "
                f"{report['usable_observations']}\n"
            )

            file.write("\nClassification:\n")
            file.write(
                f"{report['classification']}\n"
            )
            file.write(
                f"Explanation: "
                f"{report['classification_reason']}\n"
            )

            if report["usable_observations"] == 0:
                file.write(
                    "\nNot enough valid data to calculate summaries.\n"
                )
                file.write("\n" + "=" * 40 + "\n\n")
                continue

            heart_rate = report.get(
                "heart_rate_summary",
                {}
            )

            skin_response = report.get(
                "skin_response_summary",
                {}
            )

            temperature = report.get(
                "temperature_summary",
                {}
            )

            activity = report.get(
                "activity_level_summary",
                {}
            )

            signal_quality = report.get(
                "signal_quality_summary",
                {}
            )

            file.write("\nHeart Rate:\n")
            file.write(
                f"Average: {round(heart_rate['average'], 2)}\n"
            )
            file.write(
                f"Minimum: {heart_rate['minimum']}\n"
            )
            file.write(
                f"Maximum: {heart_rate['maximum']}\n"
            )

            file.write("\nSkin Response:\n")
            file.write(
                f"Average: {round(skin_response['average'], 2)}\n"
            )
            file.write(
                f"Minimum: {skin_response['minimum']}\n"
            )
            file.write(
                f"Maximum: {skin_response['maximum']}\n"
            )

            file.write("\nTemperature:\n")
            file.write(
                f"Average: {round(temperature['average'], 2)}\n"
            )
            file.write(
                f"Minimum: {temperature['minimum']}\n"
            )
            file.write(
                f"Maximum: {temperature['maximum']}\n"
            )

            file.write("\nActivity Level:\n")
            file.write(
                f"Average: {round(activity['average'], 2)}\n"
            )
            file.write(
                f"Minimum: {activity['minimum']}\n"
            )
            file.write(
                f"Maximum: {activity['maximum']}\n"
            )

            file.write("\nSignal Quality:\n")
            file.write(
                f"Average: {round(signal_quality['average'], 2)}\n"
            )
            file.write(
                f"Minimum: {signal_quality['minimum']}\n"
            )
            file.write(
                f"Maximum: {signal_quality['maximum']}\n"
            )

            file.write("\n" + "=" * 40 + "\n\n")

    return report_file
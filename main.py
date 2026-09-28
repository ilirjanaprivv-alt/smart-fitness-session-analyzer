import argparse
from pathlib import Path

from fitness_analyzer.csv_reader import (load_participants, load_sessions)
from fitness_analyzer.analysis import analyze_session
from fitness_analyzer.reporting import (write_analysis_summary, write_analysis_report, write_rejected_records)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Smart Fitness Session Analyzer")

    parser.add_argument(
        "--profiles",
        type=Path,
        default=Path("data/participants.csv"),
        help="Path to participant CSV file"
    )

    parser.add_argument(
        "--sessions",
        type=Path,
        nargs="+",
        default=[
            Path("data/fitness_sessions.csv"),
            Path("data/fitness_sessions_invalid.csv")
        ],
        help="Path to one or more fitness session CSV files"
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Path to output directory"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    participants_file = args.profiles
    session_files = args.sessions
    output_dir = args.output

    participants = load_participants(participants_file)

    all_sessions = {}
    all_rejected_records = []

    for session_file in session_files:
        sessions, rejected_records = load_sessions(session_file, participants)

        all_rejected_records.extend(rejected_records)

        for session_id, session in sessions.items():
            if session_id not in all_sessions:
                all_sessions[session_id] = session

            else:
                all_sessions[session_id].observations.extend(
                    session.observations
                )

    reports = []

    for session in all_sessions.values():
        report = analyze_session(session, len(session.observations))

        reports.append(report)

    summary_file = write_analysis_summary(reports, output_dir)

    report_file = write_analysis_report(reports, output_dir)

    rejected_file = write_rejected_records(all_rejected_records, output_dir)

    accepted_rows = 0

    for session in all_sessions.values():
        accepted_rows += len(session.observations)

    print("Analysis completed.")
    print("Accepted rows:", accepted_rows)
    print("Rejected rows:", len(all_rejected_records))

    print("\nCreated files:")
    print(summary_file)
    print(report_file)
    print(rejected_file)


if __name__ == "__main__":
    main()
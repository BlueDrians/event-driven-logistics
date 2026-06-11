import csv
import json
from pathlib import Path

INPUT = Path("data/sample/logistics_events_sample.csv")
OUTPUT = Path("data/sample/logistics_events_replay.jsonl")


def main():
    with INPUT.open(newline="", encoding="utf-8") as f, OUTPUT.open("w", encoding="utf-8") as out:
        for row in csv.DictReader(f):
            row["sla_minutes"] = int(row["sla_minutes"])
            row["actual_minutes"] = int(row["actual_minutes"])
            row["is_sla_breached"] = str(row["is_sla_breached"]).lower() == "true"
            out.write(json.dumps(row) + "\n")
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()

import csv
from pathlib import Path

INPUT = Path("data/sample/logistics_events_sample.csv")
OUTPUT = Path("docs/generated-executive-summary.md")


def main():
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    total = len(rows)
    delivered = sum(1 for r in rows if r["status"] == "DELIVERED")
    delayed = sum(1 for r in rows if r["status"] == "DELAYED")
    breach = sum(1 for r in rows if str(r["is_sla_breached"]).lower() == "true")
    sla_rate = (total - breach) / total if total else 0
    summary = f"""# Generated Executive Summary

Based on the sample dataset, the logistics platform processed **{total} status events**.

## Key Findings

- Delivered events: **{delivered}**
- Delayed events: **{delayed}**
- SLA breach count: **{breach}**
- SLA achievement rate: **{sla_rate:.1%}**

## Recommendation

Prioritize route-level monitoring, delay reason classification, and proactive alerting for routes with repeated SLA breaches.
"""
    OUTPUT.write_text(summary, encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()

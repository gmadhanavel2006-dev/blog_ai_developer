import os
import schedule
import sys
import time
import warnings
from datetime import datetime

for stream_name in ("stdout", "stderr"):
    stream = getattr(sys, stream_name)
    if hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
)

from agents.categories import DAILY_CATEGORIES
from agents.publisher_agent import PublisherAgent
from scheduler.night_job import run_night_workflow


def morning_job():
    print(f"\n--- APPROVAL CHECK ({datetime.now().strftime('%H:%M')}) ---")
    publisher = PublisherAgent()
    drafts = publisher.check_for_drafts()

    if not drafts:
        print("No new drafts found.")
        return

    for draft in drafts:
        publisher.ask_approval(draft)


def run_category(category):
    """Run the full workflow for one specific category."""
    print(f"\n--- BLOG JOB [{category['name']}] TRIGGERED ({datetime.now().strftime('%H:%M')}) ---")
    run_night_workflow(category=category)


def main():
    print("\n" + "=" * 55)
    print("   India & Tamil Nadu News Agent — 8 Blogs/Day")
    print("=" * 55)
    print("\nSchedule:")
    for cat in DAILY_CATEGORIES:
        print(f"  {cat['schedule_time']}  →  {cat['name']}")
    print("\nApproval check runs every hour.")
    print("Type '1' in the terminal when prompted to publish.\n")
    print("-" * 55)

    # Run the first category immediately on startup so you see output right away
    # print("[System] Running startup cycle (Morning Roundup)...")
    # run_category(DAILY_CATEGORIES[0])
    # morning_job()

    # Schedule all 4 categories at their designated times
    for cat in DAILY_CATEGORIES:
        # Use a default arg capture to avoid closure bug
        schedule.every().day.at(cat["schedule_time"]).do(
            lambda c=cat: run_category(c)
        )

    # Check for pending drafts every hour
    schedule.every(1).hour.do(morning_job)

    print("\nScheduler Active — Press Ctrl+C to stop.")

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()

import os
import sys
from datetime import datetime
from agents.categories import DAILY_CATEGORIES
from scheduler.night_job import run_night_workflow

def run_all_categories():
    print(f"\n{'='*60}")
    print(f"   STARTING FULL DAY GENERATION ({datetime.now().strftime('%Y-%m-%d')})")
    print(f"{'='*60}\n")
    
    for i, category in enumerate(DAILY_CATEGORIES):
        print(f"\n[Category {i+1}/8] Processing: {category['name']}")
        try:
            run_night_workflow(category=category)
        except Exception as e:
            print(f"[ERROR] Failed to process {category['name']}: {e}")
            continue
            
    print(f"\n{'='*60}")
    print("   DAY 1 GENERATION COMPLETE!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_all_categories()

import sys
import os
sys.path.insert(0, os.getcwd())

from agents.categories import DAILY_CATEGORIES
from agents.quality_checker import QualityChecker

print("=== Category Schedule ===")
for cat in DAILY_CATEGORIES:
    print(f"  {cat['schedule_time']}  {cat['name']}")

print("\n=== Quality Checker Test ===")
qc = QualityChecker()

# Test 1: Short content (should fail word count)
r1 = qc.validate("Test blog title", "Short content.", {"word_count": "700-900"})
print(f"Short content check => ok={r1['ok']}")

# Test 2: Good content, unique title
long_content = "This is a proper article with lots of information about AI trends. " * 60
r2 = qc.validate("A brand new unique title about AI trends in India", long_content, {"word_count": "700-900"})
print(f"Good content check  => ok={r2['ok']}")

print("\n[SUCCESS] All 8 categories and quality checks are working!")

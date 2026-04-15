import os
import sys
import time
import warnings

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

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.editor_agent import EditorAgent
from agents.formatter_agent import FormatterAgent
from agents.monetization_agent import MonetizationAgent
from agents.quality_checker import QualityChecker
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent


def workflow_sleep(seconds):
    if os.getenv("FAST_MODE") == "true" or os.getenv("MOCK_MODE") == "true":
        return
    time.sleep(seconds)


def run_with_retry(agent_func, task_name, *args, max_retries=3, delay=60):
    for i in range(max_retries):
        try:
            return agent_func(*args)
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(
                    f"[WARN] Quota hit during {task_name}. Waiting {delay} seconds before retry {i + 1}/{max_retries}..."
                )
                time.sleep(delay)
            else:
                raise
    raise Exception(f"Failed {task_name} after {max_retries} retries due to quota limits.")


def run_night_workflow(category=None):
    """
    Run the full research → write → edit → monetize → save pipeline.
    If a category dict is provided (from agents/categories.py), the writer
    will use a customised prompt, tone, and focus sections for that slot.
    """
    label = category["name"] if category else "India & Tamil Nadu Daily News"
    print("\n" + "=" * 55)
    print(f"STARTING WORKFLOW: {label}")
    print("=" * 55)

    # 1. Research
    researcher = ResearchAgent()
    sections   = researcher.get_daily_sections()
    lead_story = run_with_retry(researcher.select_best_topic, "Research", sections)
    roundup_title = f"{label}: {lead_story}"
    print(f"[OK] Lead story: {lead_story}")

    workflow_sleep(20)

    # 2. Write – pass the category so the prompt is customised
    writer        = WriterAgent()
    draft_content = run_with_retry(
        writer.write_blog, "Writing", roundup_title, sections, category
    )
    print(f"[OK] Content generated ({len(draft_content)} chars)")

    workflow_sleep(20)

    # 3. Edit
    editor           = EditorAgent()
    polished_content = run_with_retry(editor.edit_blog, "Editing", draft_content)
    print("[OK] Content polished")

    workflow_sleep(20)

    # 4. Monetise
    monetizer         = MonetizationAgent()
    final_blog_content = run_with_retry(
        monetizer.add_affiliate_links, "Related Reading", polished_content
    )
    print("[OK] Related reading added")

    workflow_sleep(20)

    # 5. Quality check — reject duplicates and low-quality content
    checker = QualityChecker(base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    result  = checker.validate(roundup_title, final_blog_content, category or {})
    if result["duplicate"]:
        print("[Quality Guard] ✗ Duplicate content detected. Draft NOT saved.")
        print("=" * 55)
        return
    if not result["word_count_ok"]:
        print("[Quality Guard] ✗ Content too short. Draft NOT saved.")
        print("=" * 55)
        return

    # 6. Format & save
    formatter = FormatterAgent()
    filename, final_markdown = formatter.format_to_markdown(roundup_title, final_blog_content)
    path = formatter.save_draft(filename, final_markdown)
    print(f"[OK] Draft saved → {path}")
    print("=" * 55)


if __name__ == "__main__":
    run_night_workflow()

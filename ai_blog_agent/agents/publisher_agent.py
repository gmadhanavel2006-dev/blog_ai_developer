import os
import shutil
import sys

from agents.wordpress_publisher import WordPressPublisher

class PublisherAgent:
    def __init__(self):
        self.wordpress_publisher = WordPressPublisher()

    def check_for_drafts(self):
        draft_dir = os.path.join("blog", "drafts")
        if not os.path.exists(draft_dir):
            return []
        return [f for f in os.listdir(draft_dir) if f.endswith(".md")]

    def publish_blog(self, filename):
        draft_path = os.path.join("blog", "drafts", filename)
        publish_dir = os.path.join("blog", "published")
        os.makedirs(publish_dir, exist_ok=True)

        wordpress_result = None
        if self.wordpress_publisher.is_configured():
            try:
                with open(draft_path, "r", encoding="utf-8") as f:
                    draft_content = f.read()
                wordpress_result = self.wordpress_publisher.publish_markdown_content(draft_content)
                if wordpress_result and wordpress_result.get("link"):
                    print(
                        f"[Publisher Agent] WordPress published: {wordpress_result['link']}"
                    )
            except Exception as exc:
                print(f"[Publisher Agent] WordPress publish skipped: {exc}")
        else:
            print("[Publisher Agent] WordPress is not configured; publishing locally only.")

        publish_path = os.path.join(publish_dir, filename)

        shutil.move(draft_path, publish_path)
        print(f"[Publisher Agent] Successfully published! Moved to: {publish_path}")
        if wordpress_result and wordpress_result.get("link"):
            print(f"[Publisher Agent] Remote post URL: {wordpress_result['link']}")
        return publish_path

    def ask_approval(self, filename):
        if os.getenv("AUTO_PUBLISH") == "true":
            print(f"[Publisher Agent] AUTO_PUBLISH is enabled. Automatically publishing: {filename}")
            self.publish_blog(filename)
            return

        print(f"\n--- MORNING UPDATE ---")
        print(f"Your blog is ready: {filename}")
        
        draft_path = os.path.join("blog", "drafts", filename)
        try:
            with open(draft_path, "r", encoding="utf-8") as f:
                content = f.read()
                preview = content[:500] + "..." if len(content) > 500 else content
                print("\n=== PREVIEW ===")
                print(preview)
                print("================\n")
        except Exception as e:
            print(f"Could not read draft for preview: {e}")

        print("Do you want to publish it?")
        if self.wordpress_publisher.is_configured():
            print("Type 1 to publish in the site and WordPress.")
        else:
            print("Type 1 to publish in the local site.")
        print("Type 2 to keep it as a draft.")

        if not sys.stdin.isatty():
            print("[Publisher Agent] Non-interactive terminal detected. Blog kept in drafts.")
            return

        try:
            choice = input("Select an option (1/2): ").strip().lower()
        except EOFError:
            print("[Publisher Agent] No input available. Blog kept in drafts.")
            return

        if choice in {"1", "y", "yes"}:
            self.publish_blog(filename)
        else:
            print("[Publisher Agent] Blog kept in drafts.")

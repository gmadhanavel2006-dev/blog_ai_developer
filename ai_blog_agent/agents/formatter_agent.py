import os
from datetime import datetime

class FormatterAgent:
    SECTION_IMAGES = {
        "National": "/assets/national.svg",
        "International": "/assets/international.svg",
        "Sports": "/assets/sports.svg",
        "Headlines": "/assets/headlines.svg",
    }

    def _inject_section_images(self, content):
        updated = content
        for section_name, image_path in self.SECTION_IMAGES.items():
            marker = f"## {section_name}\n"
            image_markdown = f"![{section_name} illustration]({image_path})\n\n"
            if marker in updated and image_markdown not in updated:
                updated = updated.replace(marker, f"{marker}{image_markdown}", 1)
        return updated

    def format_to_markdown(self, title, content):
        print("[Formatter Agent] Converting to Markdown...")
        # Ensure title is file-system friendly and keep it short for Windows limits
        safe_title = "".join([c for c in title if c.isalnum() or c==' ']).rstrip()
        safe_title = safe_title.replace(" ", "_")
        if len(safe_title) > 50:
            safe_title = safe_title[:50]
        
        filename = f"{safe_title}_{datetime.now().strftime('%Y%m%d')}.md"
        
        # Add metadata frontmatter
        metadata = f"---\ntitle: {title}\ndate: {datetime.now().strftime('%Y-%m-%d')}\nagent: NightWriter\n---\n\n"
        markdown_content = metadata + self._inject_section_images(content)
        return filename, markdown_content

    def save_draft(self, filename, content):
        path = os.path.join("blog", "drafts", filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[Formatter Agent] Saved draft to: {path}")
        return path

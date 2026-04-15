import base64
import mimetypes
import os
from dataclasses import dataclass

import markdown
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class WordPressConfig:
    site_url: str
    username: str
    app_password: str
    status: str = "publish"


class WordPressPublisher:
    def __init__(self):
        self.config = self._load_config()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(self.base_dir, "blog", "assets")

    def _load_config(self):
        site_url = os.getenv("WORDPRESS_URL", "").strip()
        username = os.getenv("WORDPRESS_USERNAME", "").strip()
        app_password = os.getenv("WORDPRESS_APP_PASSWORD", "").strip()
        status = os.getenv("WORDPRESS_STATUS", "publish").strip() or "publish"

        if not (site_url and username and app_password):
            return None

        return WordPressConfig(
            site_url=site_url.rstrip("/"),
            username=username,
            app_password=app_password,
            status=status,
        )

    def is_configured(self):
        return self.config is not None

    def _split_frontmatter(self, content):
        title = None
        body = content

        if content.startswith("---"):
            try:
                parts = content.split("---", 2)
                meta = parts[1]
                body = parts[2]
                for line in meta.splitlines():
                    if line.lower().startswith("title:"):
                        title = line.split(":", 1)[1].strip()
                        break
            except Exception:
                body = content

        return title, body

    def _strip_duplicate_heading(self, body, title):
        stripped_body = body.lstrip("\n")
        lines = stripped_body.splitlines()
        if not lines:
            return body

        first_line = lines[0].lstrip()
        if first_line.startswith("#"):
            heading_text = first_line.lstrip("#").strip()
            if title and heading_text == title.strip():
                return "\n".join(lines[1:]).lstrip("\n")
        return body

    def _asset_to_data_uri(self, asset_path):
        mime_type, _ = mimetypes.guess_type(asset_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        with open(asset_path, "rb") as asset_file:
            encoded = base64.b64encode(asset_file.read()).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"

    def _inline_local_images(self, html_content):
        if not self.assets_dir or not os.path.isdir(self.assets_dir):
            return html_content

        soup = BeautifulSoup(html_content, "html.parser")
        changed = False

        for img in soup.find_all("img"):
            src = img.get("src", "")
            if src.startswith("/assets/"):
                asset_name = src.split("/assets/", 1)[1]
                asset_path = os.path.join(self.assets_dir, asset_name)
                if os.path.exists(asset_path):
                    img["src"] = self._asset_to_data_uri(asset_path)
                    changed = True

        return str(soup) if changed else html_content

    def render_markdown_for_wordpress(self, content):
        title, body = self._split_frontmatter(content)
        body = self._strip_duplicate_heading(body, title)
        html = markdown.markdown(body, extensions=["extra"])
        html = self._inline_local_images(html)
        return title, html

    def publish_markdown_content(self, content):
        if not self.is_configured():
            raise RuntimeError(
                "WordPress is not configured. Set WORDPRESS_URL, WORDPRESS_USERNAME, and WORDPRESS_APP_PASSWORD."
            )

        title, html_content = self.render_markdown_for_wordpress(content)
        if not title:
            title = "Daily News Roundup"

        endpoint = f"{self.config.site_url}/wp-json/wp/v2/posts"
        payload = {
            "title": title,
            "content": html_content,
            "status": self.config.status,
        }

        response = requests.post(
            endpoint,
            json=payload,
            auth=(self.config.username, self.config.app_password),
            timeout=30,
        )

        if response.status_code >= 400:
            raise RuntimeError(
                f"WordPress publish failed ({response.status_code}): {response.text}"
            )

        data = response.json()
        return {
            "id": data.get("id"),
            "link": data.get("link"),
            "title": data.get("title", {}).get("rendered", title),
        }

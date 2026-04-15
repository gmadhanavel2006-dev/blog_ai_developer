from datetime import datetime
from html import escape
import os

import markdown
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="India & Tamil Nadu Daily News Dashboard")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLISHED_DIR = os.path.join(BASE_DIR, "blog", "published")
ASSETS_DIR = os.path.join(BASE_DIR, "blog", "assets")

if os.path.isdir(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


def parse_blog_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    title = os.path.basename(path).replace(".md", "").replace("_", " ")
    body = content

    if content.startswith("---"):
        try:
            parts = content.split("---", 2)
            meta = parts[1]
            body = parts[2]
            for line in meta.splitlines():
                if line.lower().startswith("title:"):
                    title = line.split(":", 1)[1].strip()
        except Exception:
            body = content

    stripped_body = body.lstrip("\n")
    body_lines = stripped_body.splitlines()
    if body_lines:
        first_line = body_lines[0].lstrip()
        if first_line.startswith("#"):
            heading_text = first_line.lstrip("#").strip()
            if heading_text == title.strip():
                body = "\n".join(body_lines[1:]).lstrip("\n")

    html_content = markdown.markdown(body, extensions=["extra"])
    modified = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%b %d, %Y")
    return title, html_content, modified


def get_published_blogs():
    if not os.path.exists(PUBLISHED_DIR):
        return []

    blogs = []
    for filename in os.listdir(PUBLISHED_DIR):
        if not filename.endswith(".md"):
            continue

        path = os.path.join(PUBLISHED_DIR, filename)
        title, _, modified = parse_blog_file(path)
        blogs.append(
            {
                "filename": filename,
                "title": title,
                "date": modified,
                "_sort_ts": os.path.getmtime(path),
            }
        )

    return sorted(blogs, key=lambda item: item["_sort_ts"], reverse=True)


def render_page(page_title: str, body_html: str, footer_text: str = "India & Tamil Nadu News Desk"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(page_title)}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --accent: #38bdf8;
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
            --glass: rgba(255, 255, 255, 0.05);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            background-color: var(--bg);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            background-image:
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.1) 0px, transparent 50%);
            min-height: 100vh;
            line-height: 1.7;
        }}

        a {{ color: inherit; }}

        .wrap {{
            width: min(1100px, calc(100% - 2rem));
            margin: 0 auto;
        }}

        header {{
            padding: 4rem 0 2rem;
            text-align: center;
        }}

        h1.page-title {{
            font-family: 'Playfair Display', serif;
            font-size: clamp(2.4rem, 5vw, 4rem);
            margin-bottom: 1rem;
            background: linear-gradient(to right, #38bdf8, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .subtitle {{
            font-size: 1.05rem;
            color: var(--text-dim);
            max-width: 720px;
            margin: 0 auto;
        }}

        .container {{
            padding: 1rem 0 3rem;
        }}

        .blog-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }}

        .blog-card {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass);
            border-radius: 20px;
            padding: 1.75rem;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
            text-decoration: none;
            color: inherit;
            min-height: 180px;
            display: flex;
            flex-direction: column;
        }}

        .blog-card:hover {{
            transform: translateY(-6px);
            border-color: var(--accent);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        }}

        .date {{
            font-size: 0.78rem;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.9rem;
        }}

        .blog-title {{
            font-size: 1.35rem;
            font-weight: 600;
            line-height: 1.3;
            text-wrap: balance;
        }}

        .read-more {{
            margin-top: auto;
            color: var(--accent);
            font-weight: 600;
            padding-top: 1.2rem;
        }}

        .empty-state {{
            text-align: center;
            padding: 4rem 2rem;
            background: var(--card-bg);
            border-radius: 20px;
            border: 1px dashed var(--text-dim);
        }}

        .empty-state h2 {{
            margin-bottom: 0.75rem;
        }}

        .article {{
            max-width: 820px;
            margin: 0 auto;
            padding: 0 0 4rem;
        }}

        .back-nav {{
            padding: 2rem 0 1rem;
        }}

        .back-btn {{
            color: var(--accent);
            text-decoration: none;
            font-weight: 600;
        }}

        .post-card {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 28px;
            border: 1px solid var(--glass);
            padding: clamp(1.5rem, 3vw, 2.5rem);
        }}

        .meta {{
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }}

        .post-title {{
            font-family: 'Playfair Display', serif;
            font-size: clamp(2rem, 5vw, 3rem);
            line-height: 1.1;
            margin-bottom: 1.5rem;
            color: #fff;
        }}

        .content h2 {{
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            color: var(--accent);
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
        }}

        .content h3 {{
            margin-top: 2rem;
            margin-bottom: 0.6rem;
            color: white;
        }}

        .content p {{
            margin-bottom: 1.2rem;
            color: var(--text-main);
            font-size: 1.05rem;
        }}

        .content img {{
            display: block;
            width: 100%;
            height: auto;
            margin: 1rem 0 1.5rem;
            border-radius: 18px;
            border: 1px solid var(--glass);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
        }}

        .content ul,
        .content ol {{
            margin-left: 1.4rem;
            margin-bottom: 1.2rem;
        }}

        .content li {{
            margin-bottom: 0.5rem;
        }}

        .content hr {{
            border: 0;
            border-top: 1px solid var(--glass);
            margin: 2.5rem 0;
        }}

        .content blockquote {{
            border-left: 4px solid var(--accent);
            padding-left: 1.2rem;
            font-style: italic;
            color: var(--text-dim);
            margin-bottom: 1.8rem;
        }}

        footer {{
            text-align: center;
            padding: 2rem 0 3rem;
            color: var(--text-dim);
            font-size: 0.9rem;
        }}

        @media (max-width: 768px) {{
            header {{ padding-top: 2.5rem; }}
            .container {{ padding-top: 0.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="wrap">
        {body_html}
        <footer>&copy; 2024 {escape(footer_text)}</footer>
    </div>
</body>
</html>"""


def render_index(blogs):
    if blogs:
        cards = []
        for blog in blogs:
            cards.append(
                f"""<a href="/blog/{escape(blog['filename'])}" class="blog-card">
                        <div class="date">{escape(blog['date'])}</div>
                        <div class="blog-title">{escape(blog['title'])}</div>
                        <div class="read-more">Read Full Article &rarr;</div>
                    </a>"""
            )

        content = f"""
        <header>
            <h1 class="page-title">India & Tamil Nadu Daily News</h1>
            <p class="subtitle">Nightly roundups covering national, international, sports, and Tamil Nadu headlines.</p>
        </header>
        <div class="container">
            <div class="blog-grid">
                {''.join(cards)}
            </div>
        </div>
        """
    else:
        content = """
        <header>
            <h1 class="page-title">India & Tamil Nadu Daily News</h1>
            <p class="subtitle">Nightly roundups covering national, international, sports, and Tamil Nadu headlines.</p>
        </header>
        <div class="container">
            <div class="empty-state">
                <h2>No blogs published yet.</h2>
                <p>Approve your first draft in the terminal to see it here.</p>
            </div>
        </div>
        """

    return render_page("India & Tamil Nadu Daily News | Dashboard", content, footer_text="India & Tamil Nadu News Desk. Powered by Groq.")


def render_post(title: str, date: str, content_html: str):
    body = f"""
    <div class="article">
        <div class="back-nav">
            <a href="/" class="back-btn">&larr; Back to Dashboard</a>
        </div>
        <article class="post-card">
            <div class="meta">{escape(date)}</div>
            <h1 class="post-title">{escape(title)}</h1>
            <div class="content">
                {content_html}
            </div>
        </article>
    </div>
    """
    return render_page(f"{title} | India & Tamil Nadu Daily News", body)


@app.get("/", response_class=HTMLResponse)
async def home():
    blogs = get_published_blogs()
    return HTMLResponse(render_index(blogs))


@app.get("/blog/{filename}", response_class=HTMLResponse)
async def read_blog(filename: str):
    if os.path.basename(filename) != filename or not filename.endswith(".md"):
        return HTMLResponse("Blog post not found", status_code=404)

    path = os.path.join(PUBLISHED_DIR, filename)
    if not os.path.exists(path):
        return HTMLResponse("Blog post not found", status_code=404)

    title, html_content, modified = parse_blog_file(path)
    return HTMLResponse(render_post(title, modified, html_content))


@app.get("/health", response_class=HTMLResponse)
async def health():
    return HTMLResponse("OK")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

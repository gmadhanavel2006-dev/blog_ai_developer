"""
Defines all 8 daily blog categories, their schedule times, and writing prompts.
Each category produces completely unique content — no duplicates, no low quality.
"""

DAILY_CATEGORIES = [
    {
        "id": "morning_news",
        "name": "India & Tamil Nadu Morning Roundup",
        "schedule_time": "06:00",
        "tone": "crisp, factual, morning-briefing",
        "sections": ["National", "International", "Sports", "Headlines"],
        "word_count": "700-900",
        "prompt_focus": (
            "You are a morning newsroom editor. Write a structured morning briefing for "
            "readers in India and Tamil Nadu. Cover: National, International, Sports, and "
            "Tamil Nadu Headlines in order. Keep paragraphs short and punchy. "
            "Each section must contain unique information not repeated elsewhere in the article."
        ),
    },
    {
        "id": "tutorial",
        "name": "Tech How-To & Tutorial",
        "schedule_time": "08:00",
        "tone": "educational, step-by-step, beginner-friendly",
        "sections": ["National", "International"],
        "word_count": "900-1100",
        "prompt_focus": (
            "You are an expert tech educator writing for Indian readers. "
            "Based on the most relevant technology headline from the inputs, "
            "write a detailed step-by-step tutorial or how-to guide about that technology topic. "
            "Structure it as: Introduction → Why It Matters → Step-by-Step Guide (numbered steps) "
            "→ Tips & Common Mistakes → Conclusion. "
            "Make every step clear, practical, and actionable for a beginner. "
            "Do NOT write a news article — write a TUTORIAL."
        ),
    },
    {
        "id": "news_update",
        "name": "India Tech & Policy News Update",
        "schedule_time": "10:00",
        "tone": "analytical, in-depth, context-rich",
        "sections": ["National", "International"],
        "word_count": "800-1000",
        "prompt_focus": (
            "You are an investigative journalist. Write a deep news analysis article about "
            "the most significant India technology, startup, or government policy development "
            "from the headline inputs. "
            "Structure: What Happened → Why It Matters → Expert Context → Impact for Indians → Outlook. "
            "Add background context. Do NOT repeat headlines — write original analytical prose."
        ),
    },
    {
        "id": "business",
        "name": "India Business & Economy Digest",
        "schedule_time": "12:00",
        "tone": "analytical, authoritative, business-reader audience",
        "sections": ["National", "International"],
        "word_count": "800-1000",
        "prompt_focus": (
            "You are a senior business journalist. Write an afternoon digest focused exclusively "
            "on India's economy, markets, startups, policy decisions, and trade developments. "
            "Use H2 headings for each key business theme. Include context and implications. "
            "Make the content unique and do not repeat points already made in other sections."
        ),
    },
    {
        "id": "tool_review",
        "name": "AI Tool Review & Recommendation",
        "schedule_time": "14:00",
        "tone": "honest, practical, review-style",
        "sections": ["National", "International"],
        "word_count": "900-1100",
        "prompt_focus": (
            "You are a trusted tech reviewer writing for Indian professionals and students. "
            "Based on the most interesting AI or software tool mentioned in the headline inputs, "
            "write a comprehensive tool review. "
            "Structure: Tool Overview → Key Features → Pros & Cons (use bullet points) "
            "→ Who Should Use It → Pricing (if known) → Final Verdict (rating out of 5). "
            "Be honest and specific. Do NOT write a news article — write a REVIEW."
        ),
    },
    {
        "id": "ai_trends",
        "name": "AI Trend Analysis",
        "schedule_time": "16:00",
        "tone": "forward-looking, insightful, expert-level",
        "sections": ["National", "International"],
        "word_count": "900-1100",
        "prompt_focus": (
            "You are a leading AI industry analyst writing for a sophisticated Indian tech audience. "
            "Based on the current headlines, identify the most significant AI or emerging technology trend. "
            "Write an in-depth trend analysis: What the trend is → Why it is happening now → "
            "Global vs India-specific impact → Opportunities and risks → What readers should do next. "
            "Use data, examples, and forward-looking insights. "
            "Do NOT repeat the news — ANALYZE the trend behind it."
        ),
    },
    {
        "id": "sports",
        "name": "Sports & Entertainment Bulletin",
        "schedule_time": "17:00",
        "tone": "energetic, fan-friendly, engaging",
        "sections": ["Sports"],
        "word_count": "700-900",
        "prompt_focus": (
            "You are a lively sports and entertainment writer. Write an evening bulletin "
            "covering cricket (especially IPL and Indian team), football, Tamil film and "
            "entertainment news, and other major sports. Use H2 headings. Keep the energy high. "
            "Do not repeat any headlines from earlier in the day."
        ),
    },
    {
        "id": "tamilnadu_spotlight",
        "name": "Tamil Nadu Deep Dive",
        "schedule_time": "22:00",
        "tone": "in-depth, investigative, reader-friendly",
        "sections": ["Headlines"],
        "word_count": "900-1100",
        "prompt_focus": (
            "You are a Tamil Nadu political and civic affairs correspondent. Write a deep-dive "
            "evening analysis covering Tamil Nadu governance, politics, social developments, "
            "Chennai city updates, and regional human interest stories. Use H2 headings. "
            "Provide original analysis and background. Do NOT repeat morning headlines — "
            "this is a night analysis piece with new angles and deeper insight."
        ),
    },
]

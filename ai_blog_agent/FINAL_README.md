# NightWriter AI: Complete News Agent Project

This is your fully functional, multi-agent AI system specifically designed for **India and Tamil Nadu Daily News**.

## 🚀 The System Architecture
The system operates in a decoupled "Night/Morning" cycle:
1.  **Night Job**: Researches National, International, Sports, and Tamil Nadu news from live RSS feeds. It uses **Llama 3.3 70B** to write a deep-dive roundup.
2.  **Morning Job**: Displays a preview and asks for your approval.
3.  **Publication**: Moves the blog to the `published` folder and optionally posts to WordPress.
4.  **Dashboard**: A premium responsive dashboard to view your news online.

## 🛠️ Installation & Setup
To get your FIRST real result, follow these 3 steps exactly:

### Step 1: Install Dependencies
Run this in your terminal to fix the "ModuleNotFoundError":
```powershell
pip install langchain-groq fastapi uvicorn markdown jinja2 requests beautifulsoup4 python-dotenv schedule
```

### Step 2: Configure Keys
Ensure your `.env` file in the `ai_blog_agent` folder has your Groq key:
```env
GROQ_API_KEY=gsk_your_key_here
```

### Step 3: Run the Agent
To start the automatic cycle:
```powershell
cd ai_blog_agent
python main.py
```

## 🖥️ View Your Result
Once you approve a blog (by typing `1` in the terminal), start the dashboard to see it:
```powershell
python dashboard.py
```
Then visit: **http://localhost:8000**

## 📂 File Structure
- `main.py`: The control center for the scheduler.
- `dashboard.py`: The local web server for your blog.
- `agents/`: The "brains" (Research, Writer, Editor, Monetizer, Publisher).
- `blog/drafts/`: Where new news roundups are prepared.
- `blog/published/`: Where your final articles live.

---
**Project Status**: COMPLETE
**AI Models**: Llama-3.3-70b (Writer), Llama-3.1-8b (Research)

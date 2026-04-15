# NightWriter AI – Autonomous Blog Writing Agent

NightWriter AI is a multi-agent system that automates the entire blog writing lifecycle for daily India and Tamil Nadu news. It researches the latest headlines at night, writes and edits a full news brief, and waits for your approval in the morning to publish.

## 🚀 How it Works

### 1. Night Workflow (1:00 AM)
- **Research Agent**: Pulls current national, international, sports, and Tamil Nadu headlines from Google News RSS feeds.
- **Writer Agent**: Generates a clean daily news roundup using Groq-hosted Llama 3.3 70B.
- **Editor Agent**: Refines clarity, flow, and newsroom tone.
- **Formatter Agent**: Converts the roundup into Markdown and saves it as a draft in `blog/drafts/`.

### 2. Morning Workflow (7:00 AM)
- **Publisher Agent**: Checks for new drafts and prompts the user in the terminal:
  - "Your news draft is ready. Type 1 to publish in the site, or 2 to keep it as a draft."
- If you type `1`: Moves the blog to `blog/published/`.
- If you type `2`: Keeps it in `blog/drafts/` for manual editing.

### Publishing Choice
- If you want the project to publish to an external platform later, `WordPress.org` is the best choice for this workflow because it gives full control and supports programmatic posting.
- `Medium` is not ideal for new automated integrations anymore.
- `Wix` is good for visual sites, but it is less direct for this kind of automated newsroom-style posting.

### Optional WordPress Publishing
If you want approved drafts to publish to a real WordPress site automatically, set these in `.env`:
```env
WORDPRESS_URL=https://your-site.com
WORDPRESS_USERNAME=your-username
WORDPRESS_APP_PASSWORD=your-application-password
WORDPRESS_STATUS=publish
```
When those values are present, typing `1` publishes to both the local site and WordPress. The article images are embedded inline from the project assets so the post stays self-contained.

---

## 🛠️ Installation

1. **Clone or Download** the project.
2. **Open in VS Code**.
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Setup API Key**:
   - Create a `.env` file in the root directory.
   - Add your Groq API Key:
     ```env
     GROQ_API_KEY=gsk-your-key-here
     ```
   - Optional local testing mode:
     ```env
     MOCK_MODE=true
     ```

---

## 🏃 Running the Agent

### Start the Scheduler
To start the autonomous system, run:
```bash
python main.py
```
*The script must remain running to trigger at 1:00 AM and 7:00 AM.*

### Test Immediately
You don't need to wait until 1 AM to see it work! Use these test commands:

**Run the Night Workflow now:**
```bash
python main.py test-night
```

**Run the Morning Approval now:**
```bash
python main.py test-morning
```

---

## 📂 Project Structure
- `agents/`: Contains the logic for Research, Writing, Editing, Related Reading, Formatting, and Publishing.
- `scheduler/`: The `night_job.py` script orchestrates the nightly tasks.
- `blog/`:
  - `drafts/`: Where new blogs are stored.
  - `published/`: Where approved blogs are moved.
- `main.py`: The entry point with time-based scheduling.

---

## ⚠️ Important Rule
The system will **never** publish without your explicit approval.

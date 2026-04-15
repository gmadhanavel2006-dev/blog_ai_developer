import os
import sys
from dotenv import load_dotenv

# 1. Check folder
current_dir = os.path.basename(os.getcwd())
print(f"[Diag] Current directory: {current_dir}")

# 2. Check .env
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
print(f"[Diag] Groq API Key found: {'Yes (ends in ' + groq_key[-4:] + ')' if groq_key else 'NO'}")

# 3. Test Imports
print("[Diag] Testing imports...")
try:
    import langchain_groq
    import fastapi
    import markdown
    import requests
    import bs4
    import schedule
    import jinja2
    print("[Diag] All core libraries imported successfully!")
except ImportError as e:
    print(f"[ERROR] Missing library: {e}")
    sys.exit(1)

# 4. Test Agent Initialization
try:
    sys.path.append(os.getcwd())
    from agents.models import GROQ_SMALL_MODEL, GROQ_LARGE_MODEL
    from agents.research_agent import ResearchAgent
    print(f"[Diag] Using Gross models: {GROQ_SMALL_MODEL}, {GROQ_LARGE_MODEL}")
    
    # Test a tiny LLM call to verify the key is valid
    from langchain_groq import ChatGroq
    llm = ChatGroq(model=GROQ_SMALL_MODEL, groq_api_key=groq_key)
    res = llm.invoke("Hello, say 'API OK'")
    print(f"[Diag] LLM Test Response: {res.content}")
except Exception as e:
    print(f"[ERROR] Agent or LLM Test failed: {e}")
    sys.exit(1)

print("\n[SUCCESS] Your system is fully ready for REAL generation.")

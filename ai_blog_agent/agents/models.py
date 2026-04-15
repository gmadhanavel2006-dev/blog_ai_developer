import os

# Current Groq replacements for the deprecated Llama 3 model IDs.
GROQ_LARGE_MODEL = os.getenv("GROQ_LARGE_MODEL", "llama-3.3-70b-versatile")
GROQ_SMALL_MODEL = os.getenv("GROQ_SMALL_MODEL", "llama-3.1-8b-instant")

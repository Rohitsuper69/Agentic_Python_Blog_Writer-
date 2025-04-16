import google.generativeai as genai
import os
import sys
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import GEMINI_API_KEY

class WritingAgent:
    def __init__(self, topic, subtopics, tone, context):
        self.topic = topic
        self.subtopics = subtopics
        self.tone = tone
        self.context = context

        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def write_blog(self):
        prompt = self.build_prompt()
        response = self.model.generate_content(prompt)
        return response.text

    def build_prompt(self):
        # Handle news articles (flat list of dicts)
        all_news = self.context.get("news", [])
        news_md = "\n".join(
            [f"- [{n['title']}]({n['link']})" for n in all_news]
        ) if all_news else "No news available."

        # Handle quote (optional or missing)
        quote_data = self.context.get("quote", {})
        if quote_data and isinstance(quote_data, dict) and "content" in quote_data:
            quote_block = f'> _"{quote_data["content"]}"_ — {quote_data.get("author", "Unknown")}'
        else:
            quote_block = "_(No quote provided)_"

        # Build structured Gemini prompt
        prompt = f"""
You are a helpful AI blog-writing assistant.

Generate a full blog post in **Markdown** on the topic: **{self.topic}**.

**Tone:** {self.tone}

### Requirements:

1. Start with a strong introduction (~100–150 words).
2. Write one H2 section for each of the following subtopics:
   - {', '.join(self.subtopics)}
   Each section should be ~200–300 words.
3. End with a **conclusion** and a clear **call-to-action**.
4. Use **these recent news articles** to ground the writing:
{news_md}

5. Include this quote at the end (if available):
{quote_block}

### Format:
- Use `##` for H2s, `###` for optional subsections
- Use bullet points, bold, italics if appropriate
- Keep the structure clean and readable
- Also keep UX looking good
"""
        return prompt

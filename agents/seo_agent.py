import google.generativeai as genai
import re
import json
import sys
import os

# Add parent directory to Python path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import GEMINI_API_KEY

class SEOAgent:
    def __init__(self, blog_content, topic, semantic_context):
        """
        Initialize the SEOAgent with blog content, topic, and semantic keyword context.
        Also configures the Gemini model for use.
        """
        self.blog_content = blog_content
        self.topic = topic
        self.semantic_keywords = semantic_context.get("keywords", [])

        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def analyze_content(self):
        """
        Generates SEO metadata from blog content using Gemini.
        """
        prompt = self.build_prompt()
        response = self.model.generate_content(prompt)
        return self.extract_json(response.text)

    def build_prompt(self):
        """
        Builds the structured prompt that instructs Gemini to return SEO metadata in JSON format.
        """
        enriched_keywords = "\n".join([
            f"- {', '.join(keyword_group)}"
            for keyword_group in self.semantic_keywords
        ])

        return f"""
You are an SEO content expert.

Your task is to generate optimized metadata for a blog post. Please:

1. Create an SEO-friendly **Title** that includes powerful or relevant keywords.
2. Write a catchy **Meta-description** (maximum 160 characters).
3. Generate 5–10 relevant **Tags / Keywords**, utilizing the provided semantic variations.
4. Estimate the **Reading Time** of the blog.
5. Suggest a clean **URL Slug** (lowercase, dash-separated).

📚 Use these semantic keyword groups when appropriate:
{enriched_keywords}

📝 Blog Content:
\"\"\"
{self.blog_content}
\"\"\"

Return the result in **JSON** format with:
`title`, `meta_description`, `tags`, `reading_time`, and `url_slug`.
"""

    def extract_json(self, response_text):
        """
        Extracts JSON from the model's response using regex.
        Returns a structured metadata dictionary or an empty fallback if parsing fails.
        """
        try:
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except Exception as e:
            print("⚠️ Error parsing SEO output:", e)

        # Fallback structure in case parsing fails
        return {
            "title": "",
            "meta_description": "",
            "tags": [],
            "reading_time": "",
            "url_slug": ""
        }

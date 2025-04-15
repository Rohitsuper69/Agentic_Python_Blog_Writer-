import os
import json
from config import OUTPUT_DIR

class ExportAgent:
    def __init__(self, blog_content, metadata):
        self.blog = blog_content
        self.meta = metadata
        self.slug = metadata.get('slug', 'blog-post').strip().lower().replace(' ', '-')

    def export(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        md_path = os.path.join(OUTPUT_DIR, f"{self.slug}.md")
        json_path = os.path.join(OUTPUT_DIR, f"{self.slug}.json")

        try:
            with open(md_path, "w", encoding="utf-8") as md_file:
                md_file.write(self.blog)
            print(f"📄 Blog saved as Markdown: `{md_path}`")

            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(self.meta, json_file, indent=4)
            print(f"📦 Metadata saved as JSON: `{json_path}`")

        except Exception as e:
            print(f"❌ Error exporting files: {e}")
    pass

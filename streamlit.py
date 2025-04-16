import streamlit as st
import asyncio
from main import process_batch
import io
import json

# Streamlit UI
st.title("Junior Blog Writer")
st.write("Generate SEO-optimized blogs with the desired tone and readability scores.")

# User Inputs
topics_input = st.text_area("Enter Blog Topics (comma-separated)", "")
tone_input = st.selectbox("Select Writing Tone", ["educational", "formal", "creative", "informal"])

# Initialize session_state for storing results if not already
if "file_results" not in st.session_state:
    st.session_state["file_results"] = []

# Button to start processing
if st.button("Generate Blogs"):
    if topics_input:
        topics = [topic.strip() for topic in topics_input.split(",")]
        
        # Show progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        async def run_pipeline():
            st.session_state["file_results"] = []  # Clear previous results
            for i, topic in enumerate(topics):
                status_text.text(f"Processing topic {i + 1} of {len(topics)}: {topic}")
                file_results = await process_batch([topic], tone_input)
                st.session_state["file_results"].extend(file_results)
                progress_bar.progress((i + 1) / len(topics))

        asyncio.run(run_pipeline())
        st.success("🎉 Blog generation complete!")
    else:
        st.error("❗ Please enter at least one topic.")

# Display results and download buttons
if st.session_state["file_results"]:
    for file_data in st.session_state["file_results"]:
        # Extract necessary data
        topic = file_data["topic"]
        slug = file_data["slug"]
        markdown_content = file_data["markdown_content"]
        json_content = file_data["json_content"]
        tags = file_data["tags"]
        reading_time = file_data["reading_time"]
        flesch_kincaid_grade = file_data["flesch_kincaid_grade"]
        flesch_reading_ease = file_data["flesch_reading_ease"]

        # Display the results
        st.markdown(f"## ✅ Blog: **{topic}**")
        st.write(f"🔖 **Slug**: {slug}")
        st.write(f"🏷️ **Keywords**: {', '.join(tags)}")
        st.write(f"⏱️ **Read Time**: {reading_time}")
        st.write(f"📊 **Flesch-Kincaid Grade Level**: {flesch_kincaid_grade}")
        st.write(f"📊 **Flesch Reading Ease**: {flesch_reading_ease}")

        # Display markdown preview
        st.markdown("### 📝 Blog Preview (Rendered Markdown)")
        st.markdown(markdown_content, unsafe_allow_html=True)


        # Display JSON preview
        st.markdown("### 📄 SEO Metadata (JSON)")
        st.json(json.loads(json_content))

        # Create in-memory file buffers for download
        markdown_buffer = io.StringIO(markdown_content)
        json_buffer = io.StringIO(json_content)

        # Provide download buttons
        st.download_button(
            label=f"📥 Download {slug}.md",
            data=markdown_buffer.getvalue(),
            file_name=f"{slug}.md",
            mime="text/markdown"
        )

        st.download_button(
            label=f"📥 Download {slug}.json",
            data=json_buffer.getvalue(),
            file_name=f"{slug}.json",
            mime="application/json"
        )

        st.markdown("---")  # Horizontal separator between blogs

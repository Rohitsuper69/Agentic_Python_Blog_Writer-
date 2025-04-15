import os
import json
import hashlib
from config import OUTPUT_DIR
from agents.topic_agent import TopicAgent
from agents.context_agent import ContextAgent
from agents.writing_agent import WritingAgent
from agents.seo_agent import SEOAgent
from agents.export_agent import ExportAgent
import textstat

# Custom cache dictionary for context data
context_cache = {}

def generate_cache_key(*args):
    """Generates a cache key from the arguments."""
    return hashlib.md5(json.dumps(args, default=str).encode()).hexdigest()

async def cached_context_gathering(topic, subtopics):
    """Caches context gathering results."""
    cache_key = generate_cache_key(topic, tuple(subtopics))  # Creating a unique key based on topic and subtopics
    
    if cache_key in context_cache:
        print("\n🔄 Using cached context data.")
        return context_cache[cache_key]
    
    print(f"\n🌍 Gathering context for topic: {topic}")
    context_agent = ContextAgent(topic, subtopics)
    context_data = await context_agent.gather_context()
    
    # Storing the result in the cache
    context_cache[cache_key] = context_data
    return context_data


def cached_topic_analysis(topic, tone):
    print(f"\n🔍 Analyzing topic: {topic} (Tone: {tone})")
    topic_agent = TopicAgent(topic, tone)
    return topic_agent.analyze()


def serialize_dict_to_string(data):
    """Converts a dictionary to a JSON string for caching purposes."""
    return json.dumps(data, sort_keys=True)


def cached_seo_analysis(blog_content, topic, serialized_context_data):
    print(f"\n🔎 Analyzing SEO for topic: {topic}")
    context_data = json.loads(serialized_context_data)  # Deserialize the context data back to a dictionary
    seo_agent = SEOAgent(blog_content, topic, context_data)
    return seo_agent.analyze_content()


def calculate_readability(blog_content):
    """Calculates and returns the readability score of the blog."""
    # Calculate the Flesch-Kincaid Grade Level
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(blog_content)
    # Calculate the Flesch Reading Ease score
    flesch_reading_ease = textstat.flesch_reading_ease(blog_content)
    
    return flesch_kincaid_grade, flesch_reading_ease


async def process_blog(topic, tone):
    print(f"\n🚀 Starting blog generation for: {topic} (Tone: {tone})")

    try:
        # Step 1: Topic Understanding (with caching)
        subtopics, tone_used = cached_topic_analysis(topic, tone)

        # Step 2: Research (with custom caching)
        context_data = await cached_context_gathering(topic, tuple(subtopics))
        print(context_data)

        # Step 3: Content Writing
        writing_agent = WritingAgent(topic, subtopics, tone_used, context_data)
        blog_content = writing_agent.write_blog()
        print(blog_content)

        # Step 4: SEO Optimization (with caching)
        serialized_context_data = serialize_dict_to_string(context_data)  # Serialize context data
        metadata = cached_seo_analysis(blog_content, topic, serialized_context_data)
        print(metadata)

        # Step 5: Calculate Readability Score
        flesch_kincaid_grade, flesch_reading_ease = calculate_readability(blog_content)

        # Step 6: Export (but not saving files to system)
        ExportAgent(blog_content, metadata).export()

        print("✅ Blog generation complete!\n")

        # Return metadata, blog content, readability, etc.
        return topic, metadata, blog_content, flesch_kincaid_grade, flesch_reading_ease

    except Exception as e:
        print(f"Error in process_blog: {e}")
        return None  # Ensure we return None in case of error


import io

async def process_batch(topics, tone):
    file_data = []
    for topic in topics:
        result = await process_blog(topic, tone)
        if result is None:
            print(f"Skipping topic '{topic}' due to error.")
            continue
        
        topic, metadata, blog_text, flesch_kincaid_grade, flesch_reading_ease = result

        # Prepare Markdown and JSON file content as strings
        topic=topic
        tags=metadata['tags']
        read_time=metadata['reading_time']
        slug = metadata['url_slug']
        markdown_content = blog_text
        json_content = json.dumps(metadata, indent=4)

        # Store content for download in the result list
        file_data.append({
            "topic":topic,
            "slug": slug,
            "markdown_content": markdown_content,
            "json_content": json_content,
            "flesch_kincaid_grade":flesch_kincaid_grade,
            "flesch_reading_ease":flesch_reading_ease,
            "tags":tags,
            "reading_time":read_time
        })
        
    return file_data



async def run_pipeline():
    topics = ["Topic 1", "Topic 2", "Topic 3"]  # Example topics
    tone_input = "informative"  # Example tone
    file_results = await process_batch(topics, tone_input)

    # Make sure file_results is not empty or None
    if file_results:
                # In run_pipeline, update the loop to unpack 5 values
        for j, (md_path, json_path, metadata, flesch_kincaid_grade, flesch_reading_ease) in enumerate(file_results):
            print(f"Processed blog {j + 1}:")
            print(f"Markdown Path: {md_path}")
            print(f"JSON Path: {json_path}")
            print(f"Metadata: {metadata}\n")

    else:
        print("No valid file results found.")

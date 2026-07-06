from youtube_transcript_api import YouTubeTranscriptApi
import re
import os
import requests
from datetime import datetime, timezone

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../research/youtube-transcripts/"))
PAUSE_THRESHOLD_SECONDS = 3.0

def extract_video_id(url):
    patterns = [
        r'^https?://(?:www\.)?youtu\.be/([^?&/]+)',
        r'^https?://(?:www\.)?youtube\.com/watch\?v=([^?&/]+)',
    ]
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)

    match = re.search(r'v=([a-zA-Z0-9_-]{11})', url)
    return match.group(1) if match else None


def get_video_metadata(video_id):
    defaults = {
        'title': 'Unknown Title',
        'author_name': 'unknown_expert',
        'author_url': '',
    }
    try:
        oembed_url = (
            f"https://www.youtube.com/oembed"
            f"?url=https://www.youtube.com/watch?v={video_id}&format=json"
        )
        resp = requests.get(oembed_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return {
                'title': data.get('title', defaults['title']),
                'author_name': data.get('author_name', defaults['author_name']),
                'author_url': data.get('author_url', defaults['author_url']),
            }
    except Exception:
        pass
    return defaults


def clean_filename(text):
    filename = text.lower().strip().replace(" ", "_")
    invalid_chars = r'\\/*?:"<>|'
    for ch in invalid_chars:
        filename = filename.replace(ch, '')
    filename = re.sub(r'_+', '_', filename).strip('_')
    return filename or 'untitled'


def build_filename(expert_name, title, video_id):
    parts = [
        clean_filename(expert_name),
        clean_filename(title),
        clean_filename(video_id),
    ]
    return "_".join(parts) + ".md"


def fetch_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    try:
        fetched = ytt_api.fetch(video_id, languages=['en'])
    except Exception:
        fetched = ytt_api.fetch(video_id)

    return {
        'entries': fetched.to_raw_data(),
        'language': fetched.language,
        'language_code': fetched.language_code,
        'is_generated': fetched.is_generated,
    }


def format_transcript_paragraphs(entries):
    if not entries:
        return []

    paragraphs = []
    current_parts = []
    previous_end = entries[0]['start']

    for entry in entries:
        text = entry['text'].strip()
        if not text:
            continue

        gap = entry['start'] - previous_end
        ends_sentence = current_parts and re.search(r'[.!?]["\']?\s*$', current_parts[-1])

        if current_parts and (gap >= PAUSE_THRESHOLD_SECONDS or ends_sentence):
            paragraphs.append(' '.join(current_parts))
            current_parts = []

        current_parts.append(text)
        previous_end = entry['start'] + entry.get('duration', 0)

    if current_parts:
        paragraphs.append(' '.join(current_parts))

    return [re.sub(r'\s+', ' ', p).strip() for p in paragraphs if p.strip()]


def write_transcript_file(filepath, metadata, url, transcript_info, paragraphs):
    fetched_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    language_label = transcript_info['language']
    if transcript_info['language_code']:
        language_label = f"{language_label} ({transcript_info['language_code']})"
    transcript_type = 'auto-generated' if transcript_info['is_generated'] else 'manual'

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"title: \"{metadata['title']}\"\n")
        f.write(f"video_id: {metadata['video_id']}\n")
        f.write(f"url: {url}\n")
        f.write(f"expert: \"{metadata['author_name']}\"\n")
        f.write(f"channel_url: {metadata['author_url']}\n")
        f.write(f"language: \"{language_label}\"\n")
        f.write(f"transcript_type: {transcript_type}\n")
        f.write(f"fetched_at: \"{fetched_at}\"\n")
        f.write("---\n\n")

        f.write(f"# {metadata['title']}\n\n")
        f.write("## Metadata\n\n")
        f.write(f"- **Expert / Channel:** [{metadata['author_name']}]({metadata['author_url']})\n")
        f.write(f"- **Video ID:** `{metadata['video_id']}`\n")
        f.write(f"- **URL:** {url}\n")
        f.write(f"- **Language:** {language_label}\n")
        f.write(f"- **Transcript:** {transcript_type}\n")
        f.write(f"- **Fetched:** {fetched_at}\n\n")

        f.write("## Transcript\n\n")
        for paragraph in paragraphs:
            f.write(f"{paragraph}\n\n")


def save_transcripts(video_urls):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for url in video_urls:
        video_id = extract_video_id(url)

        if not video_id:
            print(f"[ERROR] Invalid URL: {url}")
            continue

        try:
            metadata = get_video_metadata(video_id)
            metadata['video_id'] = video_id

            transcript_info = fetch_transcript(video_id)
            paragraphs = format_transcript_paragraphs(transcript_info['entries'])

            filename = build_filename(
                metadata['author_name'],
                metadata['title'],
                video_id,
            )
            filepath = os.path.join(OUTPUT_DIR, filename)

            write_transcript_file(filepath, metadata, url, transcript_info, paragraphs)
            print(f"[SUCCESS] Saved: {filename}")

        except Exception as e:
             print(f"[SKIPPED] {url} -> no usable transcript")
        continue


if __name__ == "__main__":
    video_urls = [
        "https://www.youtube.com/watch?v=8V6z8J3x0fA",
        "https://www.youtube.com/watch?v=JYk2yHh7x7Y",
        "https://www.youtube.com/watch?v=O0bXq0y3dW4",
        "https://www.youtube.com/watch?v=2pK0x9kJz7E",
        "https://www.youtube.com/watch?v=9j2zXk7wH6Y",
        "https://www.youtube.com/watch?v=Vh7sH7w2k9U",
        "https://www.youtube.com/watch?v=V8eLdbk5N6E",
        "https://www.youtube.com/watch?v=5l8xY3bP5G8",
        "https://www.youtube.com/watch?v=6dKx8dZk6k0",
        "https://www.youtube.com/watch?v=G2p7wY4X0aE",
        "https://www.youtube.com/watch?v=4i3v2uQdY7w",
        "https://www.youtube.com/watch?v=9z3k6F0w0nA",
        "https://www.youtube.com/watch?v=kqtD5dpn9C8",
        "https://www.youtube.com/watch?v=ysz5S6PUM-U",
        "https://www.youtube.com/watch?v=YxS6a1kb7f0",
        "https://www.youtube.com/watch?v=8q2YxW9Zk6E",
        "https://www.youtube.com/watch?v=R4K6c9g0p6E",
        "https://www.youtube.com/watch?v=ZpK6f7r2Y3A"
    ]
    save_transcripts(video_urls)
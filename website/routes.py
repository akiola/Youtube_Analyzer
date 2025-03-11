'''Views for the Flask application.'''
import os
import re
import subprocess
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

main = Blueprint('main', __name__)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
os.makedirs(STATIC_DIR, exist_ok=True)


def extract_video_id(url):
    """Extract the YouTube video ID from a URL."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([A-Za-z0-9_-]{11})',
        r'youtube\.com\/embed\/([A-Za-z0-9_-]{11})',
        r'youtube\.com\/v\/([A-Za-z0-9_-]{11})'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None

def get_video_title(video_id):
    """Fetch the video title using yt-dlp."""
    try:
        command = [
            "yt-dlp",
            "--print", "title",
            f"https://www.youtube.com/watch?v={video_id}"
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e: #pylint: disable=broad-except
        print(f"❌ Error fetching title: {e}")
        return "Unknown Video"


def download_audio(video_id):
    """Download audio from YouTube using yt-dlp and get title.""" ##with the cookies now
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Downloading audio from: {url}")

        audio_file = os.path.join(STATIC_DIR, f"video_audio_{video_id}.mp3")
        cookies_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies.txt")

        command = [
            "yt-dlp",
            "--cookies", cookies_path, 
            "-x",
            "--audio-format", "mp3",
            "-o", audio_file,
            url
        ]

        print(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)#pylint: disable=subprocess-run-check)

        if result.returncode != 0:
            print(f"❌ Error executing yt-dlp: {result.stderr}")
            return None, None

        print(f"✅ Successfully downloaded audio to: {audio_file}")

        video_title = get_video_title(video_id)

        return audio_file, video_title

    except Exception as e: #pylint: disable=broad-except
        print(f"❌ Error downloading audio: {e}")
        return None, None



def transcribe_audio(audio_file):
    """Transcribe audio file using OpenAI Whisper API."""
    try:
        print(f"Transcribing: {audio_file}")

        if not os.path.exists(audio_file):
            print(f"❌ File not found: {audio_file}")
            return None

        file_size = os.path.getsize(audio_file)
        print(f"File size: {file_size} bytes")
        if file_size > 25 * 1024 * 1024:
            print("❌ File too large for OpenAI API (>25MB)")
            return "File too large for transcription. Please try a shorter video."

        with open(audio_file, "rb") as audio:
            print("Sending file to OpenAI Whisper API...")
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio
            )

        print("✅ Transcription successful")

        transcript_path = os.path.join(STATIC_DIR, "transcription.txt")
        with open(transcript_path, "w") as f: #pylint: disable=unspecified-encoding
            f.write(transcript.text)

        return transcript.text

    except Exception as e:#pylint: disable=broad-except
        print(f"❌ Error transcribing audio: {e}")
        return None


def summarize_text(text):
    """Summarize transcribed text using OpenAI GPT-3.5."""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content":"You are assistant that summarizes video transcripts."},
    {"role": "user", "content": f"Please summarize the following transcript concisely:\n\n{text}"}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e: #pylint: disable=broad-except
        print(f"❌ Error summarizing text: {e}")
        return None

@main.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@main.route('/process', methods=['POST'])
def process_video():
    """Process the submitted YouTube URL."""
    url = request.form.get('youtube_url')

    if not url:
        flash('Please enter a YouTube URL')
        return redirect(url_for('main.index'))

    video_id = extract_video_id(url)
    if not video_id:
        flash('Invalid YouTube URL')
        return redirect(url_for('main.index'))

    audio_file, video_title = download_audio(video_id)
    if not audio_file:
        flash('Failed to download audio from the video')
        return redirect(url_for('main.index'))

    transcript = transcribe_audio(audio_file)
    if not transcript:
        flash('Failed to transcribe the audio')
        return redirect(url_for('main.index'))

    summary = summarize_text(transcript)

    return render_template('result.html',
                           video_id=video_id,
                           video_title=video_title,
                           transcript=transcript,
                           summary=summary)


@main.route('/download/<video_id>')
def download_transcript(video_id): #pylint: disable=unused-argument
    """Download the transcript file."""
    transcript_path = os.path.join(STATIC_DIR, "transcription.txt")
    if os.path.exists(transcript_path):
        return send_file(transcript_path, as_attachment=True)

    flash('Transcript file not found')
    return redirect(url_for('main.index'))


@main.route('/api/process', methods=['POST'])
def api_process_video():
    """API endpoint for processing YouTube videos."""
    data = request.json
    url = data.get('youtube_url')

    if not url:
        return jsonify({'error': 'Please provide a YouTube URL'}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    audio_file, video_title = download_audio(video_id)
    if not audio_file:
        return jsonify({'error': 'Failed to download audio from the video'}), 500

    transcript = transcribe_audio(audio_file)
    if not transcript:
        return jsonify({'error': 'Failed to transcribe the audio'}), 500

    summary = summarize_text(transcript)

    return jsonify({
        'video_id': video_id,
        'video_title': video_title,
        'transcript': transcript,
        'summary': summary
    })

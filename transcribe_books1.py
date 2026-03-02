"""
AUDIOBOOK TRANSCRIBER
=====================
This script transcribes all MP3 audiobook files in a folder
and saves the text output, ready for NotebookLM.

Automatically splits files longer than 9 hours into chunks
to stay within AssemblyAI's 10-hour limit.

SETUP (one time):
1. Install Python from https://www.python.org/downloads/
   (Check "Add Python to PATH" during install!)
2. Open Command Prompt and type:
      pip install assemblyai
3. Install ffmpeg (needed for long audiobooks):
      Open Command Prompt and type: winget install ffmpeg
      Then CLOSE and REOPEN Command Prompt.
4. Put your API key below (between the quotes)
5. Put all your MP3 files in one folder and set the path below

THEN JUST RUN THIS FILE!
"""

import assemblyai as aai
import os
import time
import subprocess
import json
import shutil
import tempfile

# ============================================================
#  YOUR SETTINGS - EDIT THESE TWO LINES
# ============================================================

API_KEY = "API for AssemplyAI"           # Paste your AssemblyAI API key between the quotes
AUDIOBOOKS_FOLDER = r"C:\Users\VishalAmin\OneDrive - Wellness House Ltd\Downloads\Books"    # Change this to your folder of MP3 files

# ============================================================
#  DON'T EDIT BELOW THIS LINE
# ============================================================

MAX_DURATION_SECONDS = 9 * 3600  # 9 hours (buffer under 10hr limit)

def format_time(seconds):
    """Turn seconds into a friendly time string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def find_ffmpeg():
    """Find ffmpeg - check script folder first, then system PATH."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_ffmpeg = os.path.join(script_dir, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    return None

def get_audio_duration(filepath, ffmpeg_path):
    """Get the duration of an audio file in seconds."""
    ffprobe_path = ffmpeg_path.replace("ffmpeg", "ffprobe") if "ffmpeg" in ffmpeg_path else "ffprobe"
    try:
        result = subprocess.run(
            [ffprobe_path, "-v", "quiet", "-print_format", "json",
             "-show_format", filepath],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            info = json.loads(result.stdout)
            return float(info["format"]["duration"])
    except Exception:
        pass

    # Fallback: parse ffmpeg output
    try:
        result = subprocess.run(
            [ffmpeg_path, "-i", filepath],
            capture_output=True, text=True, timeout=60
        )
        for line in result.stderr.split("\n"):
            if "Duration:" in line:
                time_str = line.split("Duration:")[1].split(",")[0].strip()
                parts = time_str.split(":")
                return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    except Exception:
        pass
    return None

def split_audio(filepath, ffmpeg_path, chunk_duration, temp_dir):
    """Split an audio file into chunks and return list of chunk paths."""
    basename = os.path.splitext(os.path.basename(filepath))[0]
    output_pattern = os.path.join(temp_dir, f"{basename}_chunk_%03d.mp3")

    try:
        result = subprocess.run(
            [ffmpeg_path, "-i", filepath, "-f", "segment",
             "-segment_time", str(chunk_duration),
             "-c", "copy", "-y", output_pattern],
            capture_output=True, text=True, timeout=3600
        )
        if result.returncode != 0:
            print(f"           ffmpeg error: {result.stderr[:200]}")
            return None

        chunk_paths = []
        for f in sorted(os.listdir(temp_dir)):
            if f.startswith(f"{basename}_chunk_") and f.endswith(".mp3"):
                chunk_paths.append(os.path.join(temp_dir, f))
        return chunk_paths if chunk_paths else None

    except subprocess.TimeoutExpired:
        print("           ffmpeg timed out while splitting.")
        return None

def transcribe_file(filepath, transcriber):
    """Transcribe a single file and return (text, error)."""
    transcript = transcriber.transcribe(filepath)
    if transcript.status == aai.TranscriptStatus.error:
        return None, transcript.error
    return transcript.text, None

def main():
    if API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: You need to paste your AssemblyAI API key into the script.")
        print("Open this file in Notepad and replace YOUR_API_KEY_HERE with your key.")
        input("\nPress Enter to exit...")
        return

    if not os.path.exists(AUDIOBOOKS_FOLDER):
        print(f"ERROR: Folder not found: {AUDIOBOOKS_FOLDER}")
        print("Check the AUDIOBOOKS_FOLDER path in the script.")
        input("\nPress Enter to exit...")
        return

    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        print("WARNING: ffmpeg not found!")
        print("Long audiobooks (10+ hours) will fail without it.")
        print("To install, open Command Prompt and run: winget install ffmpeg")
        print("Then close and reopen Command Prompt before running this script again.")
        print("\nContinuing anyway (shorter files will still work)...\n")

    audio_extensions = ('.mp3', '.m4a', '.m4b', '.wav', '.flac', '.aac', '.ogg', '.wma')
    audio_files = [
        f for f in os.listdir(AUDIOBOOKS_FOLDER)
        if f.lower().endswith(audio_extensions)
    ]

    if not audio_files:
        print(f"No audio files found in: {AUDIOBOOKS_FOLDER}")
        print(f"Supported formats: {', '.join(audio_extensions)}")
        input("\nPress Enter to exit...")
        return

    output_folder = os.path.join(AUDIOBOOKS_FOLDER, "Transcripts")
    os.makedirs(output_folder, exist_ok=True)

    aai.settings.api_key = API_KEY
    config = aai.TranscriptionConfig(speech_models=["universal-2"])
    transcriber = aai.Transcriber(config=config)

    print("=" * 60)
    print("  AUDIOBOOK TRANSCRIBER")
    print("=" * 60)
    print(f"\n  Found {len(audio_files)} audio file(s)")
    print(f"  ffmpeg: {'Found' if ffmpeg_path else 'NOT FOUND (long files may fail)'}")
    print(f"  Transcripts will be saved to: {output_folder}\n")
    print("=" * 60)

    already_done = []
    to_process = []
    for filename in sorted(audio_files):
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{name_without_ext}.txt")
        if os.path.exists(output_path):
            already_done.append(filename)
        else:
            to_process.append(filename)

    if already_done:
        print(f"\n  Skipping {len(already_done)} already-transcribed file(s):")
        for f in already_done:
            print(f"    [DONE] {f}")

    if not to_process:
        print("\n  All files have already been transcribed!")
        input("\nPress Enter to exit...")
        return

    print(f"\n  Transcribing {len(to_process)} file(s)...\n")

    successful = 0
    failed = 0

    for i, filename in enumerate(to_process, 1):
        filepath = os.path.join(AUDIOBOOKS_FOLDER, filename)
        name_without_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(output_folder, f"{name_without_ext}.txt")

        print(f"  [{i}/{len(to_process)}] {filename}")

        needs_splitting = False
        duration = None

        if ffmpeg_path:
            duration = get_audio_duration(filepath, ffmpeg_path)
            if duration:
                print(f"           Duration: {format_time(duration)}")
                if duration > MAX_DURATION_SECONDS:
                    needs_splitting = True
                    print(f"           Longer than 9 hours - splitting into chunks")

        start_time = time.time()

        try:
            if needs_splitting and ffmpeg_path:
                temp_dir = tempfile.mkdtemp()
                try:
                    print(f"           Splitting...")
                    chunks = split_audio(filepath, ffmpeg_path, MAX_DURATION_SECONDS, temp_dir)

                    if not chunks:
                        print(f"           ERROR: Failed to split file")
                        failed += 1
                        continue

                    print(f"           Split into {len(chunks)} chunks")
                    all_text = []

                    for ci, chunk_path in enumerate(chunks, 1):
                        print(f"           Transcribing chunk {ci}/{len(chunks)}...")
                        text, error = transcribe_file(chunk_path, transcriber)
                        if error:
                            print(f"           ERROR on chunk {ci}: {error}")
                        elif text:
                            all_text.append(text)

                    if all_text:
                        with open(output_path, "w", encoding="utf-8") as f:
                            f.write(f"Book: {name_without_ext}\n")
                            f.write(f"{'=' * 50}\n\n")
                            f.write("\n\n".join(all_text))

                        elapsed = time.time() - start_time
                        print(f"           DONE in {format_time(elapsed)} - saved to Transcripts folder")
                        successful += 1
                    else:
                        print(f"           ERROR: No chunks transcribed successfully")
                        failed += 1
                finally:
                    shutil.rmtree(temp_dir, ignore_errors=True)

            else:
                print(f"           Uploading and transcribing... (this may take a while)")
                text, error = transcribe_file(filepath, transcriber)

                if error:
                    print(f"           ERROR: {error}")
                    failed += 1
                    continue

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(f"Book: {name_without_ext}\n")
                    f.write(f"{'=' * 50}\n\n")
                    f.write(text)

                elapsed = time.time() - start_time
                print(f"           DONE in {format_time(elapsed)} - saved to Transcripts folder")
                successful += 1

        except Exception as e:
            print(f"           ERROR: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print("  ALL DONE!")
    print(f"  Successful: {successful}")
    if failed:
        print(f"  Failed: {failed}")
    print(f"\n  Transcripts saved in: {output_folder}")
    print("\n  Next step: Upload the .txt files to NotebookLM!")
    print("=" * 60)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

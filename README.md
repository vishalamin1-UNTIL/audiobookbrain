# 🎧 Audiobook Transcriber

Batch transcribe your audiobook collection into text files, ready to upload to [NotebookLM](https://notebooklm.google.com) as a personal knowledge base.

Uses [AssemblyAI](https://www.assemblyai.com) to convert MP3 audiobooks into searchable text. Just point it at a folder of audiobooks, run the script, and walk away.

## Features

- **Batch processing** — transcribes an entire folder of audiobooks automatically
- **Auto-splitting** — long audiobooks (10+ hours) are split into chunks and stitched back together
- **Resumable** — if you stop the script, it picks up where it left off (skips already-transcribed files)
- **Multiple formats** — supports MP3, M4A, M4B, WAV, FLAC, AAC, OGG, and WMA

## What You'll Need

- **Python 3** — [Download here](https://www.python.org/downloads/) (check "Add Python to PATH" during install)
- **AssemblyAI account** — [Sign up here](https://www.assemblyai.com) (free tier includes $50 in credits, ~135 hours of audio)
- **ffmpeg** (optional but recommended) — needed for audiobooks longer than 10 hours

## Setup

### 1. Install the AssemblyAI Python package

Open a terminal / Command Prompt and run:

```
pip install assemblyai
```

### 2. Install ffmpeg (for long audiobooks)

**Windows:**
```
winget install ffmpeg
```

**Mac:**
```
brew install ffmpeg
```

**Linux:**
```
sudo apt install ffmpeg
```

### 3. Configure the script

Open `transcribe_books.py` in any text editor and update these two lines near the top:

```python
API_KEY = "YOUR_API_KEY_HERE"           # Your AssemblyAI API key
AUDIOBOOKS_FOLDER = r"C:\Audiobooks"    # Path to your folder of audiobook files
```

You can find your API key in your [AssemblyAI dashboard](https://www.assemblyai.com/app).

## Usage

**Windows:** Double-click `transcribe_books.py`

**Or from the terminal:**
```
python transcribe_books.py
```

The script will:
1. Scan your audiobooks folder for audio files
2. Skip any books that have already been transcribed
3. Automatically split files longer than 9 hours into chunks
4. Transcribe each file and save a `.txt` file in a `Transcripts` subfolder

### Example output

```
============================================================
  AUDIOBOOK TRANSCRIBER
============================================================

  Found 116 audio file(s)
  ffmpeg: Found
  Transcripts will be saved to: C:\Audiobooks\Transcripts

============================================================

  [1/116] Atomic Habits.mp3
           Duration: 5h 35m
           Uploading and transcribing... (this may take a while)
           DONE in 3m - saved to Transcripts folder
```

## Cost

AssemblyAI charges approximately **$0.37 per hour** of audio. Some rough estimates:

| Library size | Estimated cost |
|---|---|
| 25 books (~150 hours) | ~$55 |
| 50 books (~300 hours) | ~$111 |
| 100 books (~600 hours) | ~$222 |

New accounts get **$50 in free credits** to start.

## Loading into NotebookLM

Once your transcripts are ready:

1. Go to [notebooklm.google.com](https://notebooklm.google.com)
2. Create a new notebook
3. Click **Add Source** and upload your `.txt` files from the Transcripts folder
4. Start asking questions across all your books!

**Tip:** If you have a lot of books, create multiple notebooks grouped by topic (e.g. "Business Books", "Psychology Books") since NotebookLM has a per-notebook source limit.

## Troubleshooting

| Error | Fix |
|---|---|
| `"speech_models" must be a non-empty list` | Run `pip install --upgrade assemblyai` to update the SDK |
| `Audio duration is too long` | Install ffmpeg (see setup step 2) and use the latest version of this script |
| `Your current account balance is negative` | Top up your balance in the [AssemblyAI dashboard](https://www.assemblyai.com/app) |
| `No audio files found` | Check the `AUDIOBOOKS_FOLDER` path in the script matches your actual folder |

## License

Do whatever you want with this. No restrictions.

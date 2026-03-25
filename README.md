# Audiobook Transcriber

Batch transcribe your audiobook collection into text files, ready to upload to [NotebookLM](https://notebooklm.google.com) as a personal knowledge base ("second brain").

Uses [AssemblyAI](https://www.assemblyai.com) to convert audiobooks into searchable text. Point it at a folder, run the script, and walk away. Includes a second script to automatically organise transcripts into category folders.

## Features

- **Batch processing** — transcribes an entire folder of audiobooks automatically
- **Auto-splitting** — long audiobooks (10+ hours) are split into chunks and stitched back together
- **Resumable** — stop and restart anytime; it skips already-transcribed files
- **Skip and quit** — press **S** to skip a book mid-transcription, or **Q** to quit entirely
- **Auto-organise** — sorts transcripts into category subfolders (Business, Fiction, etc.)
- **Multiple formats** — supports MP3, M4A, M4B, WAV, FLAC, AAC, OGG, and WMA

## What You'll Need

- **Python 3** — [Download here](https://www.python.org/downloads/) (check "Add Python to PATH" during install)
- **AssemblyAI account** — [Sign up here](https://www.assemblyai.com) (free tier includes $50 in credits)
- **ffmpeg** (recommended) — needed for audiobooks longer than 10 hours

## Setup

### 1. Install Python

Download from [python.org/downloads](https://www.python.org/downloads/). During installation, **tick the "Add Python to PATH" checkbox** at the bottom of the installer.

### 2. Install the AssemblyAI package

Open Command Prompt (Windows key, type `cmd`, press Enter) and run:

```
pip install assemblyai
```

### 3. Install ffmpeg (for long audiobooks)

**Windows:**
```
winget install ffmpeg
```
Then **close and reopen** Command Prompt.

**Mac:**
```
brew install ffmpeg
```

**Linux:**
```
sudo apt install ffmpeg
```

### 4. Configure the transcriber script

Open `transcribe_books.py` in any text editor (e.g. right-click, Open with, Notepad) and update these two lines near the top:

```python
API_KEY = "YOUR_API_KEY_HERE"           # Your AssemblyAI API key
AUDIOBOOKS_FOLDER = r"C:\Audiobooks"    # Path to your folder of audiobook files
```

You can find your API key in your [AssemblyAI dashboard](https://www.assemblyai.com/app).

**Important:** Never share your API key publicly. If you upload this script to GitHub, make sure the API key line says `YOUR_API_KEY_HERE`.

## The Pipeline

### Step 1: Get your MP3s

Export DRM-free MP3s from your audiobook library (e.g. using [OpenAudible](https://openaudible.org)) into one folder.

### Step 2: Transcribe

Double-click `transcribe_books.py` (or run `python transcribe_books.py` from Command Prompt).

**Keyboard controls while running:**

| Key | What it does |
|---|---|
| **S** | Skip the current book and move to the next one |
| **Q** | Save progress and stop the script |

The script will:
1. Scan your folder for audio files
2. Show the duration of each file
3. Automatically split anything over 9 hours into chunks
4. Transcribe each file and save a `.txt` file in a `Transcripts` subfolder
5. Skip any books that already have a transcript file

### Step 3: Organise (optional)

Double-click `organize_transcripts.py` to sort transcripts into category subfolders:

```
Transcripts/
    Business & Entrepreneurship/
    Leadership & Management/
    Self-Development & Mindset/
    Psychology & Relationships/
    Communication & Persuasion/
    Biography & Memoir/
    Big Ideas, Science & Society/
    Money & Finance/
    Fiction/
```

Files are **copied** (not moved) — your originals stay in the main Transcripts folder. Any unrecognised books are listed at the end so you can sort them manually.

### Step 4: Upload to NotebookLM

1. Go to [notebooklm.google.com](https://notebooklm.google.com)
2. Create a notebook per category (e.g. "Business Books")
3. Click **Add Source** and upload the `.txt` files from that category subfolder
4. Start asking questions across all your books!

### Adding new books later

Just drop new MP3s into the same audiobooks folder and re-run `transcribe_books.py` — it only processes new files. Then re-run `organize_transcripts.py` to sort them.

## Example Output

```
============================================================
  AUDIOBOOK TRANSCRIBER
============================================================

  Found 116 audio file(s)
  ffmpeg: Found
  Transcripts will be saved to: C:\Audiobooks\Transcripts

  Press S to skip a book | Press Q to quit

============================================================

  [1/116] $100M Offers.mp3
           Duration: 3h 52m
           Uploading and transcribing... (this may take a while)
           DONE in 1m - saved to Transcripts folder
  [2/116] Sapiens - A Brief History of Humankind.mp3
           Duration: 15h 18m
           Longer than 9 hours - splitting into chunks
           Splitting...
           Split into 2 chunks
           Transcribing chunk 1/2...
           Transcribing chunk 2/2...
           DONE in 8m - saved to Transcripts folder
```

## Cost

AssemblyAI charges approximately **$0.37 per hour** of audio.

| Library size | Estimated cost |
|---|---|
| 25 books (~150 hours) | ~$55 |
| 50 books (~300 hours) | ~$111 |
| 100 books (~600 hours) | ~$222 |

New accounts get **$50 in free credits** to start.

## Troubleshooting

| Error | Fix |
|---|---|
| `"speech_models" must be a non-empty list` | Run `pip install --upgrade assemblyai` to update the SDK |
| `Audio duration is too long` | Install ffmpeg (see setup step 3) and use the latest version of this script |
| `Your current account balance is negative` | Top up your balance in the [AssemblyAI dashboard](https://www.assemblyai.com/app) |
| `Folder not found` | Open the script in Notepad and check the `AUDIOBOOKS_FOLDER` path matches your actual folder |
| `UnicodeDecodeError` / encoding crash | Make sure you're using the latest version of this script (encoding fix included) |

## Files

| File | What it does |
|---|---|
| `transcribe_books.py` | Transcribes all audiobooks in a folder to `.txt` files |
| `organize_transcripts.py` | Sorts transcript files into category subfolders |

## License

Do whatever you want with this. No restrictions.

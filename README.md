# AI Rainbolt plays Geoguessr

### I'll take it.

## Setup

Clone this repo, and setup and activate a virtualenv:

```bash
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Then, install the dependencies:
`pip install -r requirements.txt`

Make [OpenAI](https://openai.com/) and [ElevenLabs](https://elevenlabs.io) accounts and set your tokens:

```
export OPENAI_API_KEY=<openai-token>
export ELEVENLABS_API_KEY=<eleven-token>
```

Make a new voice in Eleven and get the voice id of that voice using their [get voices](https://elevenlabs.io/docs/api-reference/voices) API, or by clicking the flask icon next to the voice in the VoiceLab tab.

```
export ELEVENLABS_VOICE_ID=<voice-id>
```

## Run it!

In the terminal, run the narrator:

```bash
python narrator.py
```

When you press the `spacebar` key, the program waits for 3 seconds to let the game or score screen load, takes a screenshot, and asks AI Rainbolt to make his guess.
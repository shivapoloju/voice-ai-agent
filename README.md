# 🎙️ Voice AI Agent - Multilingual Appointment Assistant

Voice AI Agent is a voice-first medical appointment system that supports English, हिंदी (Hindi), and தமிழ் (Tamil). It lets users book, cancel, and manage medical appointments naturally using voice or text while giving staff a dashboard to monitor and adjust bookings.

## Project Overview

Voice AI Agent is designed to simplify appointment scheduling through conversational interaction. The system combines browser-based audio capture, speech recognition, text-to-speech, and a lightweight multi-agent orchestration layer to manage user intent, doctor recommendations, and scheduling.

### What this project does

- Accepts natural language input via chat or voice.
- Converts speech to text using language-aware recognition.
- Processes requests through a multi-agent scheduler.
- Generates spoken responses in the same selected language.
- Sends confirmation emails for booked appointments.
- Displays appointments in a Streamlit dashboard for manual review.

### Why it matters

- Reduces manual phone booking overhead.
- Supports multilingual users in Hindi and Tamil.
- Improves accessibility with voice-first interaction.
- Prevents scheduling conflicts and double bookings.
- Automates reminders and confirmations.

## How it works

The application flow is:

1. User opens the Streamlit app.
2. User selects a voice language: English, Hindi, or Tamil.
3. User records audio or types a request.
4. The app converts speech to text using `SpeechRecognition` and Google Recognizer with the selected language.
5. The request is forwarded to the scheduling logic.
6. The system responds with chat text and generated audio using `gTTS`.
7. Appointment details are saved in session state and can be viewed or cancelled from the dashboard.

## Architecture and components

- `app.py`: Main Streamlit interface, voice controls, chat history, and manual booking UI.
- `config.py`: Loads YAML settings, environment variables, and voice language configuration.
- `voice_agent.py`: Handles speech-to-text and text-to-speech, including locale selection.
- `audio_interface.py`: Provides browser audio recorder and audio player components.
- `utils.py`: Appointment state initialization and helper functions.
- `email_service.py`: Sends booking confirmation emails.
- `multi_agent_system.py`: Orchestrates the AI-based appointment processing.
- `settings.yaml`: Configurable prompts, doctor schedules, voice defaults, and email settings.

## Technology Stack

- Python 3.8+
- Streamlit UI
- SpeechRecognition for ASR
- gTTS for TTS
- streamlit-audiorec for browser audio recording
- Groq LLM integration
- YAML and environment-based configuration

## Supported Languages

- English (`en-US`)
- Hindi (`hi-IN`)
- Tamil (`ta-IN`)

## Local Setup

### Prerequisites

- Python 3.8 or newer
- `pip` package manager
- Browser with microphone support

### Install dependencies

From the project root:

```bash
cd projectdirectory
pip install -r requirements.txt
```

### Optional configuration

Create a `.env` file in the project folder to override defaults:

```env
GROQ_API_KEY=your_groq_api_key
VOICE_LANGUAGE=en-US
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD=your_email_password
SENDER_EMAIL=your_email@example.com
```

If you do not use email features, the app still works for voice and appointment scheduling.

### Run the app locally

Start the Streamlit server:

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

### Use the app

1. Select the desired voice language from the dropdown.
2. Press the microphone button to record voice input.
3. Speak a request such as:
   - "Book an appointment with a cardiologist"
   - "Cancel my appointment"
   - "Show me available doctors"
4. The assistant will reply by text and audio.
5. Manage appointments from the right-side dashboard.

## Configuration details

### `settings.yaml`

- `llm`: Model name, temperature, and max tokens.
- `voice.language`: Default voice language.
- `email.templates_dir`: Location of email templates.
- `doctor_schedules`: Available doctor schedules and specialties.

### `.env` variables

- `GROQ_API_KEY`: API key for Groq LLM access.
- `VOICE_LANGUAGE`: Default voice language code (`en-US`, `hi-IN`, `ta-IN`).
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SENDER_EMAIL`: Email notification settings.

## Troubleshooting

- Confirm browser microphone permissions are allowed.
- Use clear speech and a stable connection.
- If speech recognition returns wrong text, verify the selected language.
- If text-to-speech fails, ensure `gTTS` supports the selected locale.
- Check `app.log` for detailed runtime errors.

## Deploying online

This project is already prepared for Render deployment with `render.yaml`.

### Deploy on Render

1. Push your code to GitHub.
2. Sign in to Render (render.com) and create a new Web Service.
3. Connect your GitHub repository.
4. Render will detect `render.yaml` and use the configured build/start commands.
5. Add environment variables in Render:
   - `GROQ_API_KEY`
   - `VOICE_LANGUAGE` (optional, default `en-US`)
   - `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SENDER_EMAIL` (if email notifications are needed)
6. Deploy the service and open the public URL Render provides.

### What Render does for you

- Installs required system packages for audio support.
- Installs Python dependencies from `requirements.txt`.
- Runs `streamlit run app.py`.
- Exposes the app online on a public URL.

### Alternative hosting options

- Streamlit Community Cloud: good for simple Streamlit apps, but may require custom build tweaks for audio dependencies.
- Railway / Fly.io / PythonAnywhere: suitable if you want another hosting provider.
- Docker-based deployment: build a container with audio dependencies and deploy to any container host.

## Contribution guidelines

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Make your changes and commit them.
4. Push your branch and open a pull request.




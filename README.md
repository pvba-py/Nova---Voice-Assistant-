# 🎙️ Nova - Smart Voice Assistant

> A powerful, real-time voice assistant built with Python that combines speech recognition, AI conversation, and text-to-speech in an elegant web interface.

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [📁 Project Structure](#-project-structure)
- [⚙️ Configuration](#️-configuration)
  - [Voice Settings](#voice-settings)
  - [Performance Optimizations](#performance-optimizations)
- [🎯 Use Cases](#-use-cases)
- [🛠️ Technical Details](#️-technical-details)
  - [Core Technologies](#core-technologies)
  - [Performance Metrics](#performance-metrics)
- [🔒 Security & Privacy](#-security--privacy)
- [🚧 Exit Commands](#-exit-commands)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)
- [🐛 Troubleshooting](#-troubleshooting)

## ✨ Features

- **🎤 Voice Recognition**: Advanced speech-to-text using Deepgram Nova-2 model
- **🧠 AI Conversations**: Powered by Google Gemini 2.0 Flash for fast, intelligent responses
- **🔊 Natural Speech**: High-quality text-to-speech with ElevenLabs voices
- **💬 Real-time Chat**: Beautiful web interface built with Taipy framework
- **⚡ Optimized Performance**: Sub-second response times with smart conversation context
- **🎨 Modern UI**: Purple gradient theme with professional styling
- **🔄 Live Updates**: Real-time conversation display without page refresh

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Microphone access
- API keys for:
  - [Deepgram](https://deepgram.com/) (Speech Recognition)
  - [Google Gemini](https://ai.google.dev/) (AI Responses)
  - [ElevenLabs](https://elevenlabs.io/) (Text-to-Speech)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Nova
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   DEEPGRAM_API_KEY=your_deepgram_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

### Usage

1. **Start Nova (Voice Mode)**
   ```bash
   python main.py
   ```
   - Speak naturally to interact with Nova
   - Say "goodbye Nova" or "stop" to exit

2. **Start Web Interface (Optional)**
   ```bash
   python display.py
   ```
   - View conversation history in real-time
   - Access at `http://localhost:5000`

## 📁 Project Structure

```
Nova/
├── main.py              # Core voice assistant logic
├── display.py           # Taipy web interface
├── record.py            # Audio recording with VAD
├── models.py            # AI model configurations
├── voices.py            # Voice synthesis settings
├── display.css          # Web interface styling
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── audio/              # Audio files directory
│   ├── recording.wav   # Temporary recordings
│   ├── response.wav    # AI responses
│   └── farewell.wav    # Exit messages
└── logs/
    ├── conv.txt        # Conversation history
    ├── status.txt      # Real-time status
    └── meta.log        # Application logs
```

## ⚙️ Configuration

### Voice Settings
- **Speech Model**: Deepgram Nova-2 (optimized for real-time)
- **AI Model**: Google Gemini 2.0 Flash (fastest responses)
- **Voice**: ElevenLabs "B. Hardscrabble Oxley"
- **Silence Detection**: 4-second timeout for natural conversation flow

### Performance Optimizations
- **Context Limit**: Maintains last 4 conversation exchanges
- **Response Limit**: 100 tokens max for quick responses
- **Smart Formatting**: Automatic punctuation and capitalization
- **Background Processing**: Async audio transcription

## 🎯 Use Cases

- **Personal Assistant**: Ask questions, get quick answers
- **Voice Notes**: Speak your thoughts, see them transcribed
- **Learning Companion**: Interactive Q&A sessions
- **Accessibility**: Hands-free computer interaction
- **Development**: Voice-controlled coding assistant

## 🛠️ Technical Details

### Core Technologies
- **Speech Recognition**: Deepgram SDK v2.12.0
- **AI Engine**: Google Generative AI (Gemini)
- **Text-to-Speech**: ElevenLabs v0.2.27
- **Audio Processing**: PyAudio + pygame
- **Web Framework**: Taipy v3.0.0
- **Voice Activity Detection**: Rhasspy Silence

### Performance Metrics
- **Transcription**: ~2-3 seconds
- **AI Response**: <1 second
- **Audio Generation**: ~1.5 seconds
- **Total Response Time**: ~4-5 seconds

## 🔒 Security & Privacy

- **API Keys**: Stored in `.env` file (never commit to version control)
- **Local Processing**: Audio files stored locally, not uploaded
- **Conversation Logs**: Saved locally in `conv.txt`
- **No Data Collection**: Your conversations stay on your machine

## 🚧 Exit Commands

Nova responds to these voice commands to shut down gracefully:
- "stop"
- "exit" 
- "goodbye Nova"
- "sign off"
- "Nova sleep now"
- "Nova shutdown"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Deepgram** for excellent speech recognition API
- **Google** for powerful Gemini AI models
- **ElevenLabs** for natural-sounding voice synthesis
- **Taipy** for the beautiful web framework
- **Rhasspy** for voice activity detection

## 🐛 Troubleshooting

### Common Issues

**Microphone not working**
- Check microphone permissions
- Ensure PyAudio is properly installed
- Try running as administrator

**API Errors**
- Verify API keys in `.env` file
- Check internet connection
- Ensure API quotas aren't exceeded

**Audio playback issues**
- Install latest pygame version
- Check system audio drivers
- Verify audio file permissions

---

**Built with ❤️ by Vasuja** • Nova - Your Smart Voice Companion

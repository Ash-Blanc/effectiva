# Effectiva 🎓

> **Your Shapeshifting Productivity Partner for College Life**

Effectiva is an intelligent AI agent system designed specifically for college students who juggle academics, part-time work, and personal life. Built with [Agno](https://agno.com), [DSPy](https://dspy.ai), and [MemoriSDK](https://memorilabs.ai), it provides personalized, context-aware assistance across all aspects of student life.

## ✨ Key Features

### 🤖 Multi-Agent Intelligence
- **Study Agent**: Academic planning, assignments, exam prep, study schedules
- **Work Agent**: Job management, shift scheduling, career planning
- **Life Agent**: Personal tasks, wellness, habits, self-care
- **Scheduling Agent**: Cross-domain time management and optimization
- **Coordinator Agent**: Intelligent routing and orchestration

### 🧠 Persistent Memory
- Remembers your preferences, courses, work schedule, and habits
- Learns from past interactions to provide personalized guidance
- Maintains context across sessions using MemoriSDK
- Separate memory namespaces for each life domain

### 🔄 Context Switching (Shapeshifting)
- Switch between **Study**, **Work**, **Life**, and **Balanced** modes
- Each mode prioritizes relevant agents and tools
- Seamless transitions as your day flows

### 🛠️ Essential Productivity Tools
- **Task Management**: Create, track, and prioritize tasks
- **Calendar**: Schedule events, find free slots, manage deadlines
- **Time Blocking**: Pomodoro technique, study schedules, break management
- **Context Management**: Switch modes and get context-specific suggestions
- **Quick Capture**: Phone-based task, note, and energy check capture
- **Energy-Aware Scheduling**: Intelligent scheduling based on energy levels
- **WhatsApp Integration**: Essential messaging for student coordination
- **Advanced Study Techniques**: Spaced repetition, active recall, personalized learning

## 🚀 Quick Start

### Prerequisites
- Python 3.14+ (Python 3.10+ should also work)
- uv (recommended)
-   - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- OpenRouter API key ([Get one here](https://openrouter.ai/))
- LangWatch API key ([Get one here](https://app.langwatch.ai/))

### Installation

1. **Clone & navigate to the project**:
```bash
git clone https://github.com/Ash-Blanc/effectiva && cd effectiva
```

2. **Activate virtual environment** (if using venv):
```bash
source .venv/bin/activate  # Linux/Mac
# or
.venv\\Scripts\\activate  # Windows
```

3. **Install dependencies**:
```bash
uv sync  # if using uv
# or
pip install -r requirements.txt  # if using pip
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

5. **Start the Backend**:
```bash
uv run main.py  # if using uv
# or
python main.py
```

6. **Start the AgentUI (Frontend)**:
Open a new terminal window and run:
```bash
cd ui
pnpm install  # Install dependencies
pnpm dev      # Start the UI server
```

The AgentUI will start on `http://localhost:3000` by default.

## 📖 Usage Guide

### Getting Started

When you first open Effectiva, you'll be greeted by the Coordinator Agent. Simply tell it what you need help with:

- "I have three exams next week and need a study plan"
- "Can you help me schedule my work shifts around my classes?"
- "I need to manage my chores and remember to exercise"
- "Show me my upcoming deadlines across everything"

### Context Modes

Switch between modes to focus on different areas:

```
"Switch to study mode"  # Focus on academics
"Switch to work mode"   # Focus on job tasks
"Switch to life mode"   # Focus on personal wellness
"Switch to balanced mode"  # Manage everything together
```

### Example Interactions

**Academic Planning**:
```
You: I need to study for my calculus and history exams
Agent: [Creates study schedule with Pomodoro sessions]
```

**Work-Life Balance**:
```
You: I work 20 hours/week and have 5 classes. Help me find time to exercise.
Agent: [Analyzes schedule, finds free slots, suggests time blocks]
```

**Task Management**:
```
You: Add task: Finish lab report, due Friday, high priority
Agent: [Creates task, checks conflicts, suggests time to work on it]
```

## 🏗️ Architecture

### System Components

```
effectiva/
├── agents/               # Specialized AI agents
│   ├── base.py          # Base agent with memory
│   ├── coordinator.py   # Team orchestrator
│   ├── study_agent.py   # Academic assistant
│   ├── work_agent.py    # Career assistant
│   ├── life_agent.py    # Wellness assistant
│   └── scheduling_agent.py  # Time management
├── tools/               # Agent capabilities
│   ├── task_tools.py    # Task CRUD operations
│   ├── calendar_tools.py # Event management
│   ├── context_tools.py  # Mode switching
│   └── time_management.py # Scheduling optimization
├── tests/               # Test suite
│   └── scenarios/       # End-to-end scenario tests
│       ├── coordinator_test.py    # Coordinator agent tests
│       ├── study_agent_test.py    # Study agent tests
│       ├── work_agent_test.py     # Work agent tests
│       ├── life_agent_test.py     # Life agent tests
│       └── scheduling_agent_test.py # Scheduling agent tests
├── memory/              # Persistent storage
│   └── memory_manager.py # MemoriSDK integration
├── config/              # Configuration
│   └── settings.py      # Environment settings
├── main.py              # Entry point
└── pyproject.toml       # Dependencies
```

### Technology Stack

- **[Agno](https://agno.com)**: Multi-agent framework for building the agent team
- **[DSPy](https://dspy.ai)**: Framework for modular AI software (future optimization)
- **[MemoriSDK](https://memorilabs.ai)**: Persistent memory for AI agents
- **[OpenRouter](https://openrouter.ai/)**: LLM provider for agent intelligence
- **[LangWatch](https://langwatch.ai/)**: Prompt management and agent testing framework
- **Next.js UI**: Custom web interface for chat and agent interaction

### 📱 Social Media & Productivity Integrations

Effectiva integrates with major social platforms and productivity tools:

#### Social Platforms
- **WhatsApp Business API**: Send/receive messages, templates, and media

#### Google Workspace
- **Google Calendar**: Full calendar management, event creation, free/busy times

#### Advanced Learning & Productivity
- **Spaced Repetition**: Evidence-based study scheduling algorithms (Leitner, SM-2, Fibonacci)
- **Active Recall**: AI-generated practice questions and self-testing exercises
- **Study Technique Recommendations**: Personalized learning strategies based on goals and time
- **Quick Capture System**: Phone-based task, note, and energy check capture
- **Energy-Aware Scheduling**: Intelligent scheduling based on energy levels and optimal times

### Memory Architecture

Each agent has its own memory namespace:
- `effectiva:study` - Academic preferences and history
- `effectiva:work` - Job and career information
- `effectiva:life` - Personal habits and routines
- `effectiva:scheduling` - Schedule patterns
- `effectiva:coordinator` - Overall user preferences

Memory is stored in SQLite (`effectiva_memory.db`) by default.

## 🎯 Use Cases

### 1. Exam Week Preparation
- Coordinator analyzes all upcoming exams
- Study Agent creates detailed study schedule
- Scheduling Agent finds optimal time blocks
- Life Agent ensures self-care isn't forgotten

### 2. Work-Study Balance
- Work Agent tracks job schedules
- Study Agent manages class attendance
- Scheduling Agent prevents conflicts
- Coordinator maintains overall balance

### 3. Personal Wellness
- Life Agent tracks habits and routines
- Scheduling Agent finds time for exercise
- Study/Work agents respect personal time
- Coordinator encourages healthy balance

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available options:

- `GOOGLE_API_KEY`: **Required** - Your Google API key for Gemini
- `LANGWATCH_API_KEY`: **Required** - Your LangWatch API key
- `WHATSAPP_ACCESS_TOKEN`: Optional - WhatsApp Business API access token
- `WHATSAPP_PHONE_NUMBER_ID`: Optional - WhatsApp Business API phone number ID
- `DISCORD_BOT_TOKEN`: Optional - Discord bot token
- `DISCORD_DEFAULT_CHANNEL_ID`: Optional - Default Discord channel ID
- `LINKEDIN_ACCESS_TOKEN`: Optional - LinkedIn API access token
- `LINKEDIN_PERSON_URN`: Optional - Your LinkedIn person URN
- `MEMORY_DB_PATH`: Optional - Custom database location
- `PORT`: Optional - Custom UI port (default: 3000)
- `DEBUG_MODE`: Optional - Enable debug logging

### Google API Setup

For Google Calendar and Tasks integration:

1. **Create a Google Cloud Project**: Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **Enable APIs**: Enable Calendar API and Tasks API
3. **Create OAuth 2.0 Credentials**: Download the credentials JSON file
4. **Save credentials**: Place the downloaded file as `google_credentials.json` in the project root
5. **First run**: The system will automatically authenticate and create `google_token.json`

**Note**: The first time you use Google integrations, you'll need to complete OAuth authentication in your browser.

### Model Configuration

Edit `config/settings.py` to change:
- Default LLM model
- Temperature and parameters
- Memory settings
- UI configuration

### Prompt Management with LangWatch

Effectiva uses LangWatch for version-controlled prompt management:

- **Prompts are stored in `prompts/` directory** as YAML files
- **Use LangWatch CLI** to create and manage prompts:
  ```bash
  langwatch prompt create <name>
  langwatch prompt sync
  ```
- **Never hardcode prompts** in application code
- **Fetch prompts dynamically** in your agents using `langwatch.prompts.get()`

### Testing with Scenario

All agent features are tested using Scenario for reliable behavior:

- **Scenario tests** are in `tests/scenarios/` directory
- **Run tests** with pytest: `pytest tests/scenarios/`
- **Write end-to-end tests** for multi-turn conversations
- **Use judge criteria** instead of regex matching
- **Test edge cases** and business value delivery
- **Complete test coverage**: Coordinator, Study, Work, Life, and Scheduling agents all have comprehensive scenario tests

## 🚧 Future Enhancements

- [ ] Social accountability features (study buddies, progress sharing)
- [ ] Habit tracking and analytics (opt-in only, gamified)
- [ ] Voice interface support
- [ ] Mobile-friendly UI improvements
- [ ] Multi-user support
- [ ] Export/import functionality
- [ ] Integration with learning management systems (Canvas, Blackboard)

## ✅ Recent Improvements (v0.2.0)

- [x] **Simplified Architecture**: Removed overkill features (DSPy optimization, complex social integrations)
- [x] **Phone-Based Quick Capture**: Essential mobile productivity tools
- [x] **Energy-Aware Scheduling**: Addresses core afternoon slump productivity barrier
- [x] **Evidence-Based Study Techniques**: Spaced repetition and active recall implementation
- [x] **Streamlined Google Integration**: Focus on Calendar only (Tasks removed for simplicity)

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome! The codebase is designed to be extensible:

- **Add new agents**: Extend `BaseAgent` in `agents/`
- **Add new tools**: Create functions in `tools/`
- **Customize personas**: Edit agent instructions
- **Add integrations**: Create new modules in `integrations/`

## 📚 Resources

- [Agno Documentation](https://docs.agno.com)
- [DSPy Documentation](https://dspy.ai)
- [MemoriSDK Documentation](https://memorilabs.ai)
- [OpenRouter API](https://openrouter.ai/)
- [LangWatch Documentation](https://docs.langwatch.ai/)
- [Scenario Testing](https://scenario.langwatch.ai/)

## 📝 License

This project is for personal use and educational purposes.

## 🙏 Acknowledgments

Built with:
- [Agno](https://agno.com) - Powerful multi-agent framework
- [MemoriSDK](https://memorilabs.ai) - Persistent AI memory
- [DSPy](https://dspy.ai) - Framework for modular AI systems
- [OpenRouter](https://openrouter.ai/) - LLM provider
- [LangWatch](https://langwatch.ai/) - Prompt management and testing

---

**Made with ❤️ for busy college students everywhere**

Need help? Just ask Effectiva! 🎓✨

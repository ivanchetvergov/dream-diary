# DreamWeaver AI Project Context for AI Coding Assistant

## Project Overview
DreamWeaver AI is a SaaS platform for personalized dream analysis and optimization. It uses machine learning to analyze dream texts, classify emotions/symbols, and generate guided meditations. The project includes an AI agent (autonomous assistant) that interacts via Telegram bot, processes user inputs, and adapts based on memory and reasoning.

Key features:
- ML models: RoBERTa for multi-label classification (emotions/symbols), T5 for content generation.
- Data: DreamBank, DEED datasets; support for English and Russian (via translation hack).
- Agent: Autonomous AI with memory (conversation history), reasoning (logical analysis), and tools (analyzer, generator).
- Architecture: Modular OOP in Python, no heavy frameworks, focus on clean code.

## Code Style Guidelines
- **Language:** Python 3.8+.
- **Structure:** Modular (classes in separate files), OOP (SOLID principles).
- **Naming:** Classes (CamelCase), functions/methods (snake_case), variables (snake_case), constants (UPPER_CASE).
- **Formatting:** PEP8, lines <79 chars, functions <50 lines.
- **Imports:** Group (standard, third-party, local).
- **Comments:** Docstrings for classes/functions, inline for complex code.
- **Error Handling:** Try-except, log errors.
- **Testing:** Use pytest, aim for 80% coverage.
- **Performance:** Torch.no_grad() for inference, batch processing.

## Architecture Details
- **Modules:**
  - `data/`: DreamDataset (PyTorch Dataset), preprocess (cleaning).
  - `model/`: RoBERTaModel (classification), ContentGenerator (T5 for meditations).
  - `inference/`: Predictor (analyze dreams).
  - `agent/`: DreamAgent (LangChain-based, with memory and tools).
  - `bot/`: TelegramBotHandler (integrate with agent).
  - `utils/`: Config, Logger, Translator (for Russian support via Google Translate).
- **Agent Flow:** Input (dream text) → Lang detect → Translate if Russian → Analyze (RoBERTa) → Reason (LLM) → Generate/Action → Translate back → Output.
- **ML Specifics:** Fine-tune on Hugging Face, inference in Colab/Yandex Cloud. Multi-label (sigmoid + BCE loss).
- **Russian Support:** Hack: Translate RU→EN, process, EN→RU. Use googletrans library.

## Rules for AI Assistant
- Prioritize clean, maintainable code over speed.
- Suggest OOP solutions, avoid globals.
- For ML: Recommend Hugging Face, not raw PyTorch if possible.
- For agent: Use LangChain for reasoning/tools.
- If suggesting code: Include type hints, docstrings, and examples.
- Context-aware: Reference DreamWeaver modules (e.g., "Use DreamPredictor from inference/").
- Avoid heavy dependencies; prefer lightweight libs.

## Common Pitfalls to Avoid
- Hardcode paths/configs; use Config class.
- Ignore lang support; always check for RU/EN.
- Forget memory in agent; suggest ConversationMemory.
- Overcomplicate; keep simple for MVP.

Use this context to provide accurate, project-specific coding help.

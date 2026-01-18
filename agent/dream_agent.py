"""Dream Agent using Claude."""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import List, Dict, Any
from config import Config
from db.repositories import UserRepository, DreamRepository, ClassificationRepository, ChatHistoryRepository
from db.mappers import EmotionMapper


class DreamDiaryAgent:
    """AI agent for dream analysis and diary management."""

    def __init__(self, anthropic_api_key: str = None):
        """Initialize the agent with Claude."""
        self.api_key = anthropic_api_key or Config.ANTHROPIC_TOKEN
        self.llm = ChatAnthropic(
            temperature=0.8,
            anthropic_api_key=self.api_key,
            model="claude-3-sonnet-20240229"
        )
        self.chat_history: List = []
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the agent."""
        return (
            "You are DreamDiary AI, a thoughtful and empathetic dream analyst "
            "grounded in verified psychological and philosophical models "
            "(e.g., Jungian archetypes, Freudian unconscious, existential philosophy, cognitive behavioral theories). "
            "\n\n"
            "Be moderately strict in interpretations—base all insights on scientific "
            "evidence and established theories, avoiding speculation. Use chain-of-thought reasoning: "
            "first analyze elements, then connect to theories, then provide interpretation. "
            "\n\n"
            "Adapt your tone to the user's style: if they are casual or open, respond "
            "warmly and conversationally; if formal or reserved, be more structured and "
            "precise. If no user info is provided, default to a balanced, professional "
            "tone with clarity and accuracy. "
            "\n\n"
            "Always verify facts against psychological literature, explain concepts "
            "simply yet rigorously, and ensure formulations are precise. Cite key theorists "
            "briefly where relevant (e.g., 'As Jung noted...'). "
            "\n\n"
            "When analyzing dreams: "
            "1. Break down key elements: symbols, emotions, narrative structure. "
            "2. Identify primary emotions and their intensity (e.g., joy: high, fear: moderate). "
            "3. Reference relevant psychological theories (Jung, Freud, CBT, etc.) with evidence. "
            "4. Provide a balanced interpretation: personal meaning, universal insights. "
            "5. Suggest a brief guided meditation (2-3 minutes) tailored to the emotions and symbols. "
            "6. Offer actionable advice for reflection or journaling. "
            "\n\n"
            "Structure responses clearly: Use sections like 'Key Elements', 'Emotional Analysis', "
            "'Psychological Interpretation', 'Guided Meditation', 'Reflection Tips'. "
            "\n\n"
            "Keep responses supportive, evidence-based, and comprehensive but concise (aim for 300-500 words)."
        )

    def process_dream(self, dream_text: str, user_id: int = None) -> str:
        """Process a dream text and return response. Also extract emotions."""

        messages = [SystemMessage(content=self.system_prompt)]
        messages.extend(self.chat_history)
        messages.append(HumanMessage(
            content=(
                f"Analyze this dream in detail following the structured guidelines: {dream_text}. "
                "Ensure the response includes all sections: Key Elements, Emotional Analysis, "
                "Psychological Interpretation, Guided Meditation, and Reflection Tips. "
                "Use chain-of-thought: first list elements, then analyze emotions, then interpret, etc."
            )
        ))

        response = self.llm.invoke(messages)

        # Extract emotions via hidden task with improved prompt
        emotion_prompt = (
            f"Extract emotions from this dream as multi-label binary with intensity: {dream_text}. "
            "Emotions: joy, fear, anger, sadness, calm, anxiety, excitement, confusion, love, disgust. "
            "Format: [joy:1 (high), fear:0 (none), anger:0 (none), sadness:0 (none), calm:1 (moderate), anxiety:1 (low)]. "
            "Only output the list in brackets, with intensity notes."
        )
        emotion_messages = [SystemMessage(content="You are an emotion extractor. Analyze deeply and accurately."), HumanMessage(content=emotion_prompt)]
        emotion_response = self.llm.invoke(emotion_messages)
        emotions = emotion_response.content  # e.g., "[joy:1 (high), fear:0 (none), ...]"

        # Update chat history
        self.chat_history.append(HumanMessage(content=dream_text))
        self.chat_history.append(AIMessage(content=response.content))

        if len(self.chat_history) > 20:
            self.chat_history = self.chat_history[-20:]

        # Save to DB
        try:
            telegram_id = user_id if user_id else 1  # Use provided or dummy
            user = UserRepository.get_or_create(telegram_id=telegram_id, username=f"user_{telegram_id}")
            dream = DreamRepository.create(
                user_id=user.id,
                text=dream_text,
                analysis=response.content,
                emotions=EmotionMapper.parse_emotions(emotions)
            )
            # Parse and save classifications
            emotion_list = EmotionMapper.parse_emotions(emotions)
            for emo in emotion_list:
                ClassificationRepository.create(
                    dream_id=dream.id,
                    emotion=emo["emotion"],
                    intensity=emo["intensity"],
                    symbol=None  # TODO: extract symbols if needed
                )
            # Save chat history
            ChatHistoryRepository.add_message(
                user_id=user.id,
                message=dream_text,
                response=response.content
            )
        except Exception as e:
            print(f"DB save error: {e}")  # Log error, but don't fail

        return response.content

    def clear_history(self):
        """Clear chat history."""
        self.chat_history = []

    def analyze_emotions(self, dream_text: str) -> Dict[str, Any]:
        """Analyze emotions in a dream using Claude."""
        prompt = (
            f"Analyze the emotions in this dream: {dream_text}. "
            "List primary emotions with intensity and context from the dream narrative."
        )
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        response = self.llm.invoke(messages)
        return {"emotions": response.content}

    def explain_symbol(self, symbol: str) -> str:
        """Explain a dream symbol using psychological literature."""
        prompt = (
            f"Explain the dream symbol '{symbol}' using only accurate information "
            "from verified psychological literature (e.g., Jung, Freud). "
            "Communicate in simple, understandable language."
        )
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        response = self.llm.invoke(messages)
        return response.content


if __name__ == "__main__":
    agent = DreamDiaryAgent()
    dream = "I was flying over a vast ocean, feeling both exhilarated and anxious."
    result = agent.process_dream(dream)
    print("Agent Response:", result)

from src.agents.base import BaseAgent
from src.input.models import DesignInput


class KnowledgeValidatorAgent(BaseAgent):
    """Validate knowledge entries. Phase 4."""

    def system_prompt(self) -> str:
        return "Knowledge Validator - not yet implemented."

    def build_user_prompt(self, design_input: DesignInput, context: str = "") -> str:
        return ""

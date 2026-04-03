from src.agents.base import BaseAgent
from src.input.models import DesignInput


class StyleGeneratorAgent(BaseAgent):
    """Generate a complete style guide from a user brief. Phase 2."""

    def system_prompt(self) -> str:
        return "Style Guide Generator - not yet implemented."

    def build_user_prompt(self, design_input: DesignInput, context: str = "") -> str:
        return ""

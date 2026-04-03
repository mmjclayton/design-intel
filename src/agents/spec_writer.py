from src.agents.base import BaseAgent
from src.input.models import DesignInput


class SpecWriterAgent(BaseAgent):
    """Write design specs from feature descriptions. Phase 3."""

    def system_prompt(self) -> str:
        return "Design Spec Writer - not yet implemented."

    def build_user_prompt(self, design_input: DesignInput, context: str = "") -> str:
        return ""

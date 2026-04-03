from src.agents.base import BaseAgent
from src.input.models import DesignInput


class StyleExtractorAgent(BaseAgent):
    """Extract a style guide from an existing site. Phase 2."""

    def system_prompt(self) -> str:
        return "Style Guide Extractor - not yet implemented."

    def build_user_prompt(self, design_input: DesignInput, context: str = "") -> str:
        return ""

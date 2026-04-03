from src.agents.base import BaseAgent
from src.input.models import DesignInput


class KnowledgeCuratorAgent(BaseAgent):
    """Discover and ingest design knowledge. Phase 4."""

    def system_prompt(self) -> str:
        return "Knowledge Curator - not yet implemented."

    def build_user_prompt(self, design_input: DesignInput, context: str = "") -> str:
        return ""

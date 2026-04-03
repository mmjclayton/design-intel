from abc import ABC, abstractmethod

from src.input.models import DesignInput
from src.providers.llm import call_llm


class BaseAgent(ABC):
    """Base class for all design intelligence agents."""

    @abstractmethod
    def system_prompt(self) -> str:
        ...

    @abstractmethod
    def build_user_prompt(self, design_input: DesignInput, context: str = "") -> str:
        ...

    def retrieve_knowledge(self, design_input: DesignInput) -> str:
        """Retrieve relevant knowledge for this agent's task. Override in subclasses."""
        return ""

    def run(self, design_input: DesignInput, context: str = "") -> str:
        knowledge = self.retrieve_knowledge(design_input)
        user_prompt = self.build_user_prompt(design_input, context)

        if knowledge:
            user_prompt = f"## Relevant Design Principles\n\n{knowledge}\n\n---\n\n{user_prompt}"

        return call_llm(
            system_prompt=self.system_prompt(),
            user_prompt=user_prompt,
            image_path=design_input.image_path,
        )

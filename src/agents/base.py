from abc import ABC, abstractmethod
from typing import Any, Dict

class AgentContext:
    def __init__(self, config: Dict[str, Any], data_store: Dict[str, Any], vector_store: Any = None, genai_client: Any = None):
        self.config = config
        self.data_store = data_store
        self.vector_store = vector_store
        self.genai_client = genai_client

class BaseAgent(ABC):
    name: str = "base"
    description: str = ""

    def __init__(self, context: AgentContext):
        self.context = context

    @abstractmethod
    def handle(self, profile: Any) -> Dict[str, Any]:
        """Process the student profile and return structured info."""
        raise NotImplementedError

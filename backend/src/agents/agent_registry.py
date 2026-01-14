"""
Agent Registry for managing agents in the system
"""
from typing import Dict, Type, Optional, List
from .agents import BaseAgent
from .config import AgentConfig
import logging

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Registry for managing agent instances and types"""

    def __init__(self):
        self._agent_types: Dict[str, Type[BaseAgent]] = {}
        self._agent_instances: Dict[str, BaseAgent] = {}
        self._configurations: Dict[str, AgentConfig] = {}

    def register_agent_type(self, name: str, agent_class: Type[BaseAgent]):
        """Register a new agent type"""
        if name in self._agent_types:
            logger.warning(f"Agent type '{name}' already registered, overwriting")
        self._agent_types[name] = agent_class
        logger.info(f"Registered agent type: {name}")

    def register_agent(self, config: AgentConfig) -> BaseAgent:
        """Register a new agent instance with configuration"""
        if config.name in self._agent_instances:
            logger.warning(f"Agent instance '{config.name}' already registered, overwriting")

        if config.name not in self._agent_types:
            raise ValueError(f"Agent type '{config.name}' not registered")

        agent_class = self._agent_types[config.name]
        agent_instance = agent_class(config)
        self._agent_instances[config.name] = agent_instance
        self._configurations[config.name] = config

        logger.info(f"Registered agent instance: {config.name}")
        return agent_instance

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Get an agent instance by name"""
        return self._agent_instances.get(name)

    def get_config(self, name: str) -> Optional[AgentConfig]:
        """Get an agent configuration by name"""
        return self._configurations.get(name)

    def list_agents(self) -> List[str]:
        """List all registered agent names"""
        return list(self._agent_instances.keys())

    def list_agent_types(self) -> List[str]:
        """List all registered agent types"""
        return list(self._agent_types.keys())

    def is_agent_enabled(self, name: str) -> bool:
        """Check if an agent is enabled"""
        config = self.get_config(name)
        return config is not None and config.enabled

    def unregister_agent(self, name: str):
        """Remove an agent instance from the registry"""
        if name in self._agent_instances:
            del self._agent_instances[name]
            if name in self._configurations:
                del self._configurations[name]
            logger.info(f"Unregistered agent: {name}")

    def create_and_register(self, config: AgentConfig) -> BaseAgent:
        """Create and register an agent in one step"""
        # Use TaskAgent as default if no specific type is registered
        if config.name not in self._agent_types:
            from .agents import TaskAgent
            self.register_agent_type(config.name, TaskAgent)

        return self.register_agent(config)

    async def execute_agent(self, name: str, task: str, context: Optional[Dict[str, any]] = None) -> Dict[str, any]:
        """Execute a registered agent"""
        agent = self.get_agent(name)
        if not agent:
            raise ValueError(f"Agent '{name}' not found in registry")

        if not self.is_agent_enabled(name):
            raise ValueError(f"Agent '{name}' is not enabled")

        return await agent.execute(task, context)
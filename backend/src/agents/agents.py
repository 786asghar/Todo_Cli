"""
Base Agent classes for the Agents SDK
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, AsyncGenerator
from .config import AgentConfig
import asyncio
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents in the system"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self.description = config.description
        self.enabled = config.enabled

    @abstractmethod
    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the agent's primary function"""
        pass

    async def validate_input(self, task: str, context: Optional[Dict[str, Any]]) -> bool:
        """Validate input before execution"""
        if not task or not task.strip():
            return False
        return True

    async def preprocess_context(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process and normalize context before execution"""
        if context is None:
            return {}
        return context.copy()


class TaskAgent(BaseAgent):
    """Agent specialized for task execution"""

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a task with the given context"""
        if not await self.validate_input(task, context):
            raise ValueError("Invalid input for agent execution")

        processed_context = await self.preprocess_context(context or {})

        # Simulate agent execution
        logger.info(f"Executing task '{task}' with context {processed_context}")

        # This would normally connect to an MCP server or AI provider
        # For now, we'll simulate the execution
        result = {
            "agent": self.name,
            "task": task,
            "status": "completed",
            "result": f"Simulated execution of: {task}",
            "context_used": processed_context,
            "timestamp": asyncio.get_event_loop().time()
        }

        return result


class PlanningAgent(BaseAgent):
    """Agent specialized for planning tasks"""

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute planning-related tasks"""
        if not await self.validate_input(task, context):
            raise ValueError("Invalid input for planning agent")

        processed_context = await self.preprocess_context(context or {})

        # Simulate planning execution
        logger.info(f"Planning task '{task}' with context {processed_context}")

        result = {
            "agent": self.name,
            "task": task,
            "status": "planned",
            "result": f"Planning completed for: {task}",
            "context_used": processed_context,
            "timestamp": asyncio.get_event_loop().time()
        }

        return result
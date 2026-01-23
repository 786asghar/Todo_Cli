"""
ChatbotAgent for Phase 3 implementation.
Serves as the primary interface between users and the system,
interpreting natural language input and determining appropriate agent routing.
"""

import re
from typing import Dict, Any, Optional
from agents.task_agent import TaskAgent
from agents.skill_agent import SkillAgent


class ChatbotAgent:
    """
    Primary interface agent that interprets natural language input
    and routes requests to appropriate specialized agents.
    Maintains conversation context and manages information flow.
    """

    def __init__(self, task_agent: TaskAgent, skill_agent: SkillAgent):
        """
        Initialize ChatbotAgent with access to specialized agents.

        Args:
            task_agent: Instance of TaskAgent for direct operations
            skill_agent: Instance of SkillAgent for complex operations
        """
        self.task_agent = task_agent
        self.skill_agent = skill_agent

    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a natural language request and route to appropriate agent.

        Args:
            user_input: Natural language request from user

        Returns:
            Dictionary with operation result and response
        """
        try:
            # Normalize input
            user_input = user_input.strip().lower()

            # Determine intent and route to appropriate agent
            intent_result = self._analyze_intent(user_input)

            if intent_result["intent"] == "add_task":
                return self._handle_add_task(intent_result["params"])
            elif intent_result["intent"] == "list_tasks":
                return self._handle_list_tasks()
            elif intent_result["intent"] == "update_task":
                return self._handle_update_task(intent_result["params"])
            elif intent_result["intent"] == "complete_task":
                return self._handle_complete_task(intent_result["params"])
            elif intent_result["intent"] == "incomplete_task":
                return self._handle_incomplete_task(intent_result["params"])
            elif intent_result["intent"] == "delete_task":
                return self._handle_delete_task(intent_result["params"])
            elif intent_result["intent"] == "complete_all":
                return self._handle_complete_all()
            elif intent_result["intent"] == "delete_all":
                return self._handle_delete_all()
            elif intent_result["intent"] == "get_summary":
                return self._handle_get_summary()
            elif intent_result["intent"] == "unknown":
                return {
                    "success": False,
                    "operation": "unknown",
                    "message": f"I didn't understand that command. Please try again with something like 'add task', 'list tasks', 'complete task 1', etc."
                }
            else:
                return {
                    "success": False,
                    "operation": "unknown",
                    "message": f"Unsupported operation: {intent_result['intent']}"
                }
        except Exception as e:
            return {
                "success": False,
                "operation": "error",
                "error": str(e),
                "message": f"Error processing request: {str(e)}"
            }

    def _analyze_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input to determine intent and extract parameters.

        Args:
            user_input: Normalized user input string

        Returns:
            Dictionary with intent and extracted parameters
        """
        # Patterns for different intents
        patterns = {
            "add_task": [
                r"add.*task.*\"([^\"]+)\"",
                r"add.*task.*\'([^\']+)\'",
                r"add.*task.*([^.!?]+)",
                r"create.*task.*\"([^\"]+)\"",
                r"create.*task.*\'([^\']+)\'",
                r"create.*task.*([^.!?]+)",
                r"make.*task.*\"([^\"]+)\"",
                r"make.*task.*\'([^\']+)\'",
                r"make.*task.*([^.!?]+)"
            ],
            "list_tasks": [
                r"list.*task",
                r"show.*task",
                r"display.*task",
                r"view.*task",
                r"all.*task",
                r"what.*task",
                r"my.*task"
            ],
            "update_task": [
                r"update.*task.*(\d+).*to.*\"([^\"]+)\"",
                r"update.*task.*(\d+).*to.*\'([^\']+)\'",
                r"change.*task.*(\d+).*to.*\"([^\"]+)\"",
                r"change.*task.*(\d+).*to.*\'([^\']+)\'",
                r"modify.*task.*(\d+).*to.*\"([^\"]+)\"",
                r"modify.*task.*(\d+).*to.*\'([^\']+)\'"
            ],
            "complete_task": [
                r"complete.*task.*(\d+)",
                r"finish.*task.*(\d+)",
                r"done.*task.*(\d+)",
                r"mark.*task.*(\d+).*as.*complete",
                r"mark.*task.*(\d+).*done"
            ],
            "incomplete_task": [
                r"mark.*task.*(\d+).*as.*incomplete",
                r"mark.*task.*(\d+).*as.*not.*done",
                r"incomplete.*task.*(\d+)",
                r"not.*done.*task.*(\d+)"
            ],
            "delete_task": [
                r"delete.*task.*(\d+)",
                r"remove.*task.*(\d+)",
                r"cancel.*task.*(\d+)"
            ],
            "complete_all": [
                r"complete.*all.*task",
                r"finish.*all.*task",
                r"mark.*all.*task.*as.*complete",
                r"done.*with.*all.*task"
            ],
            "delete_all": [
                r"delete.*all.*task",
                r"remove.*all.*task",
                r"clear.*all.*task",
                r"get.*rid.*of.*all.*task"
            ],
            "get_summary": [
                r"summary.*task",
                r"how.*many.*task",
                r"task.*summary",
                r"statistics.*task",
                r"count.*task"
            ]
        }

        # Check for each intent
        for intent, intent_patterns in patterns.items():
            for pattern in intent_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    groups = match.groups()

                    if intent == "add_task":
                        return {
                            "intent": intent,
                            "params": {"title": groups[0].strip() if groups else ""}
                        }
                    elif intent == "update_task":
                        if len(groups) >= 2:
                            try:
                                task_id = int(groups[0])
                                new_title = groups[1].strip()
                                return {
                                    "intent": intent,
                                    "params": {"task_id": task_id, "new_title": new_title}
                                }
                            except ValueError:
                                continue  # Skip if task_id is not a number
                    elif intent in ["complete_task", "incomplete_task", "delete_task"]:
                        if groups:
                            try:
                                task_id = int(groups[0])
                                return {
                                    "intent": intent,
                                    "params": {"task_id": task_id}
                                }
                            except ValueError:
                                continue  # Skip if task_id is not a number
                    else:
                        # For intents without specific parameters
                        return {
                            "intent": intent,
                            "params": {}
                        }

        # If no pattern matched, return unknown intent
        return {
            "intent": "unknown",
            "params": {"input": user_input}
        }

    def _handle_add_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle add task requests."""
        title = params.get("title", "").strip()
        if not title:
            return {
                "success": False,
                "operation": "add",
                "message": "Please provide a task title to add."
            }

        return self.task_agent.add_task(title)

    def _handle_list_tasks(self) -> Dict[str, Any]:
        """Handle list tasks requests."""
        return self.task_agent.list_tasks()

    def _handle_update_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update task requests."""
        task_id = params.get("task_id")
        new_title = params.get("new_title", "").strip()

        if task_id is None:
            return {
                "success": False,
                "operation": "update",
                "message": "Please specify which task to update and its new title."
            }

        if not new_title:
            return {
                "success": False,
                "operation": "update",
                "message": "Please provide a new title for the task."
            }

        return self.task_agent.update_task(task_id, new_title)

    def _handle_complete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle complete task requests."""
        task_id = params.get("task_id")

        if task_id is None:
            return {
                "success": False,
                "operation": "complete",
                "message": "Please specify which task to complete."
            }

        return self.task_agent.complete_task(task_id)

    def _handle_incomplete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incomplete task requests."""
        task_id = params.get("task_id")

        if task_id is None:
            return {
                "success": False,
                "operation": "incomplete",
                "message": "Please specify which task to mark as incomplete."
            }

        return self.task_agent.incomplete_task(task_id)

    def _handle_delete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle delete task requests."""
        task_id = params.get("task_id")

        if task_id is None:
            return {
                "success": False,
                "operation": "delete",
                "message": "Please specify which task to delete."
            }

        return self.task_agent.delete_task(task_id)

    def _handle_complete_all(self) -> Dict[str, Any]:
        """Handle complete all tasks requests."""
        return self.skill_agent.complete_all_tasks()

    def _handle_delete_all(self) -> Dict[str, Any]:
        """Handle delete all tasks requests."""
        return self.skill_agent.delete_all_tasks()

    def _handle_get_summary(self) -> Dict[str, Any]:
        """Handle get summary requests."""
        return self.skill_agent.get_task_summary()


class AgentOrchestrator:
    """
    Orchestrates the overall agent system and provides the main interface
    for the chatbot functionality.
    """

    def __init__(self):
        """Initialize the orchestrator with a fresh TodoCLI instance."""
        from todo_cli import TodoCLI

        self.todo_cli = TodoCLI()
        self.task_agent = TaskAgent(self.todo_cli)
        self.skill_agent = SkillAgent(self.task_agent)
        self.chatbot_agent = ChatbotAgent(self.task_agent, self.skill_agent)

    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input through the entire agent system.

        Args:
            user_input: Natural language input from user

        Returns:
            Dictionary with structured response
        """
        return self.chatbot_agent.process_request(user_input)

    def get_current_tasks(self) -> Dict[str, Any]:
        """Get current tasks directly from the system."""
        return self.task_agent.list_tasks()
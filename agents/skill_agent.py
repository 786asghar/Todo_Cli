"""
SkillAgent for Phase 3 implementation.
Handles complex, multi-step operations that require coordination
between multiple simpler operations.
"""

from typing import Dict, Any, List
from agents.task_agent import TaskAgent


class SkillAgent:
    """
    Agent responsible for coordinating complex, multi-step operations
    that require coordination between multiple task operations.
    Leverages TaskAgent for individual operations and ChatbotAgent for decision-making.
    """

    def __init__(self, task_agent: TaskAgent):
        """
        Initialize SkillAgent with access to TaskAgent.

        Args:
            task_agent: Instance of TaskAgent to coordinate operations
        """
        self.task_agent = task_agent

    def complete_all_tasks(self) -> Dict[str, Any]:
        """
        Mark all tasks as complete.

        Returns:
            Dictionary with operation result
        """
        try:
            # Get all tasks first
            list_result = self.task_agent.list_tasks()
            if not list_result["success"]:
                return {
                    "success": False,
                    "operation": "complete_all",
                    "message": "Failed to list tasks for completion"
                }

            completed_count = 0
            failed_count = 0
            messages = []

            for task in list_result.get("tasks", []):
                task_id = task["id"]
                result = self.task_agent.complete_task(task_id)
                if result["success"]:
                    completed_count += 1
                    messages.append(result["message"])
                else:
                    failed_count += 1
                    messages.append(result["message"])

            return {
                "success": True,
                "operation": "complete_all",
                "completed_count": completed_count,
                "failed_count": failed_count,
                "total_processed": len(list_result.get("tasks", [])),
                "messages": messages,
                "message": f"Attempted to complete {len(list_result.get('tasks', []))} tasks: {completed_count} succeeded, {failed_count} failed"
            }
        except Exception as e:
            return {
                "success": False,
                "operation": "complete_all",
                "error": str(e),
                "message": f"Error completing all tasks: {str(e)}"
            }

    def delete_all_tasks(self) -> Dict[str, Any]:
        """
        Delete all tasks.

        Returns:
            Dictionary with operation result
        """
        try:
            # Get all tasks first
            list_result = self.task_agent.list_tasks()
            if not list_result["success"]:
                return {
                    "success": False,
                    "operation": "delete_all",
                    "message": "Failed to list tasks for deletion"
                }

            deleted_count = 0
            failed_count = 0
            messages = []

            for task in list_result.get("tasks", []):
                task_id = task["id"]
                result = self.task_agent.delete_task(task_id)
                if result["success"]:
                    deleted_count += 1
                    messages.append(result["message"])
                else:
                    failed_count += 1
                    messages.append(result["message"])

            return {
                "success": True,
                "operation": "delete_all",
                "deleted_count": deleted_count,
                "failed_count": failed_count,
                "total_processed": len(list_result.get("tasks", [])),
                "messages": messages,
                "message": f"Attempted to delete {len(list_result.get('tasks', []))} tasks: {deleted_count} succeeded, {failed_count} failed"
            }
        except Exception as e:
            return {
                "success": False,
                "operation": "delete_all",
                "error": str(e),
                "message": f"Error deleting all tasks: {str(e)}"
            }

    def get_task_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all tasks including counts of completed/incomplete tasks.

        Returns:
            Dictionary with operation result and summary statistics
        """
        try:
            list_result = self.task_agent.list_tasks()
            if not list_result["success"]:
                return {
                    "success": False,
                    "operation": "summary",
                    "message": "Failed to get task list for summary"
                }

            tasks = list_result.get("tasks", [])
            total_count = len(tasks)
            completed_count = sum(1 for task in tasks if task.get("completed", False))
            incomplete_count = total_count - completed_count

            return {
                "success": True,
                "operation": "summary",
                "total_count": total_count,
                "completed_count": completed_count,
                "incomplete_count": incomplete_count,
                "tasks": tasks,
                "message": f"Task summary: {total_count} total, {completed_count} completed, {incomplete_count} incomplete"
            }
        except Exception as e:
            return {
                "success": False,
                "operation": "summary",
                "error": str(e),
                "message": f"Error getting task summary: {str(e)}"
            }

    def bulk_update_tasks(self, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update multiple tasks at once.

        Args:
            updates: List of dictionaries containing task_id and new_title

        Returns:
            Dictionary with operation result
        """
        try:
            updated_count = 0
            failed_count = 0
            messages = []

            for update in updates:
                task_id = update.get("task_id")
                new_title = update.get("new_title")

                if task_id is None or new_title is None:
                    failed_count += 1
                    messages.append(f"Invalid update format for task: {update}")
                    continue

                result = self.task_agent.update_task(task_id, new_title)
                if result["success"]:
                    updated_count += 1
                    messages.append(result["message"])
                else:
                    failed_count += 1
                    messages.append(result["message"])

            return {
                "success": True,
                "operation": "bulk_update",
                "updated_count": updated_count,
                "failed_count": failed_count,
                "total_processed": len(updates),
                "messages": messages,
                "message": f"Attempted to update {len(updates)} tasks: {updated_count} succeeded, {failed_count} failed"
            }
        except Exception as e:
            return {
                "success": False,
                "operation": "bulk_update",
                "error": str(e),
                "message": f"Error bulk updating tasks: {str(e)}"
            }
"""
TaskAgent for Phase 3 implementation.
Handles all direct task operations (add, list, update, complete, incomplete, delete)
while maintaining compatibility with existing Phase 1 functionality.
"""

from typing import Dict, List, Optional, Any
from todo_cli import TodoCLI, Task


class TaskAgent:
    """
    Specialized agent responsible for managing task operations.
    Operates on existing task data structures while maintaining
    compatibility with Phase 1 functionality.
    """

    def __init__(self, todo_cli: TodoCLI):
        """
        Initialize TaskAgent with access to existing TodoCLI instance.

        Args:
            todo_cli: Instance of the existing TodoCLI to maintain compatibility
        """
        self.todo_cli = todo_cli

    def add_task(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Add a new task using the existing functionality.

        Args:
            title: The title of the task to add

        Returns:
            Dictionary with operation result or None if failed
        """
        try:
            result = self.todo_cli.add_task(title)
            if result:
                return {
                    "success": True,
                    "operation": "add",
                    "task_id": result.id,
                    "title": result.title,
                    "completed": result.completed,
                    "message": f"Added task: {result}"
                }
            else:
                return {
                    "success": False,
                    "operation": "add",
                    "message": "Failed to add task"
                }
        except Exception as e:
            return {
                "success": False,
                "operation": "add",
                "error": str(e),
                "message": f"Error adding task: {str(e)}"
            }

    def list_tasks(self) -> Dict[str, Any]:
        """
        List all tasks using the existing functionality.

        Returns:
            Dictionary with operation result and task list
        """
        try:
            # We need to capture the output from list_tasks
            # Since the original method prints directly, we'll return the internal data
            tasks_data = []
            if not self.todo_cli.tasks:
                return {
                    "success": True,
                    "operation": "list",
                    "tasks": [],
                    "message": "No tasks found"
                }

            for task in sorted(self.todo_cli.tasks.values(), key=lambda t: t.id):
                tasks_data.append({
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed
                })

            return {
                "success": True,
                "operation": "list",
                "tasks": tasks_data,
                "message": f"Found {len(tasks_data)} tasks"
            }
        except Exception as e:
            return {
                "success": False,
                "operation": "list",
                "error": str(e),
                "message": f"Error listing tasks: {str(e)}"
            }

    def update_task(self, task_id: int, new_title: str) -> Dict[str, Any]:
        """
        Update a task using the existing functionality.

        Args:
            task_id: ID of the task to update
            new_title: New title for the task

        Returns:
            Dictionary with operation result
        """
        try:
            result = self.todo_cli.update_task(task_id, new_title)
            if result:
                return {
                    "success": True,
                    "operation": "update",
                    "task_id": task_id,
                    "message": f"Updated task {task_id}"
                }
            else:
                return {
                    "success": False,
                    "operation": "update",
                    "task_id": task_id,
                    "message": f"Failed to update task {task_id}"
                }
        except Exception as e:
            return {
                "success": False,
                "operation": "update",
                "task_id": task_id,
                "error": str(e),
                "message": f"Error updating task {task_id}: {str(e)}"
            }

    def complete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Mark a task as complete using the existing functionality.

        Args:
            task_id: ID of the task to complete

        Returns:
            Dictionary with operation result
        """
        try:
            result = self.todo_cli.complete_task(task_id)
            if result:
                task = self.todo_cli.tasks.get(task_id)
                return {
                    "success": True,
                    "operation": "complete",
                    "task_id": task_id,
                    "title": task.title if task else None,
                    "message": f"Completed task {task_id}: {task.title if task else 'Unknown'}"
                }
            else:
                return {
                    "success": False,
                    "operation": "complete",
                    "task_id": task_id,
                    "message": f"Failed to complete task {task_id}"
                }
        except Exception as e:
            return {
                "success": False,
                "operation": "complete",
                "task_id": task_id,
                "error": str(e),
                "message": f"Error completing task {task_id}: {str(e)}"
            }

    def incomplete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Mark a task as incomplete using the existing functionality.

        Args:
            task_id: ID of the task to mark as incomplete

        Returns:
            Dictionary with operation result
        """
        try:
            result = self.todo_cli.incomplete_task(task_id)
            if result:
                task = self.todo_cli.tasks.get(task_id)
                return {
                    "success": True,
                    "operation": "incomplete",
                    "task_id": task_id,
                    "title": task.title if task else None,
                    "message": f"Marked task {task_id} as incomplete: {task.title if task else 'Unknown'}"
                }
            else:
                return {
                    "success": False,
                    "operation": "incomplete",
                    "task_id": task_id,
                    "message": f"Failed to mark task {task_id} as incomplete"
                }
        except Exception as e:
            return {
                "success": False,
                "operation": "incomplete",
                "task_id": task_id,
                "error": str(e),
                "message": f"Error marking task {task_id} as incomplete: {str(e)}"
            }

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Delete a task using the existing functionality.

        Args:
            task_id: ID of the task to delete

        Returns:
            Dictionary with operation result
        """
        try:
            result = self.todo_cli.delete_task(task_id)
            if result:
                return {
                    "success": True,
                    "operation": "delete",
                    "task_id": task_id,
                    "message": f"Deleted task {task_id}"
                }
            else:
                return {
                    "success": False,
                    "operation": "delete",
                    "task_id": task_id,
                    "message": f"Failed to delete task {task_id}"
                }
        except Exception as e:
            return {
                "success": False,
                "operation": "delete",
                "task_id": task_id,
                "error": str(e),
                "message": f"Error deleting task {task_id}: {str(e)}"
            }
#!/usr/bin/env python3
"""
Phase-1 In-Memory Todo CLI Application

This implementation follows the Phase-1 specification for a single-user,
in-memory task management system with CLI operations. All functionality
is based strictly on the feature specification (task-crud.md) and SP.TASK
document.
"""

import sys
import argparse
from typing import Dict, List, Optional


class Task:
    """
    Represents a single task with ID, title, and completion status.

    Based on: Spec Section 3.1 (Task Attributes)
    """
    def __init__(self, task_id: int, title: str, completed: bool = False):
        self.id = task_id
        self.title = title
        self.completed = completed

    def __str__(self):
        status = "Complete" if self.completed else "Incomplete"
        return f"{self.id} - {self.title} [{status}]"


class TodoCLI:
    """
    In-memory Todo CLI application implementing Phase-1 requirements.

    Based on: SP.PLAN Task 1-11, SP.TASK Task 1-12
    """

    def __init__(self):
        """Initialize the in-memory task storage."""
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def _get_next_id(self) -> int:
        """Get the next available task ID."""
        while self.next_id in self.tasks:
            self.next_id += 1
        return self.next_id

    def add_task(self, title: str) -> Optional[Task]:
        """
        Add a new task with the provided title.

        Based on: Spec Section 2.1 (Add a Task), Spec Section 4.1 (Add Task Acceptance Criteria)
        SP.TASK Task 4: Implement Add Task Functionality
        """
        if not title or not title.strip():
            print("Error: Task title cannot be empty")
            return None

        task_id = self._get_next_id()
        task = Task(task_id, title.strip())
        self.tasks[task_id] = task
        print(f"Added task: {task}")
        self.next_id = task_id + 1  # Update next_id for efficiency
        return task

    def list_tasks(self):
        """
        Display all tasks with their ID, title, and completion status.

        Based on: Spec Section 2.2 (List Tasks), Spec Section 4.2 (List Tasks Acceptance Criteria)
        SP.TASK Task 5: Implement List Tasks Functionality
        """
        if not self.tasks:
            print("No tasks found")
            return

        for task in sorted(self.tasks.values(), key=lambda t: t.id):
            print(task)

    def update_task(self, task_id: int, new_title: str) -> bool:
        """
        Update the title of an existing task.

        Based on: Spec Section 2.3 (Update a Task), Spec Section 4.3 (Update Task Acceptance Criteria)
        SP.TASK Task 6: Implement Update Task Functionality
        """
        if not new_title or not new_title.strip():
            print("Error: Task title cannot be empty")
            return False

        if task_id not in self.tasks:
            print(f"Error: Task not found with ID: {task_id}")
            return False

        old_title = self.tasks[task_id].title
        self.tasks[task_id].title = new_title.strip()
        print(f"Updated task {task_id}: '{old_title}' -> '{new_title}'")
        return True

    def complete_task(self, task_id: int) -> bool:
        """
        Mark a task as complete.

        Based on: Spec Section 2.4 (Mark Task Complete/Incomplete),
        Spec Section 4.4 (Mark Task Complete/Incomplete Acceptance Criteria)
        SP.TASK Task 7: Implement Complete Task Functionality
        """
        if task_id not in self.tasks:
            print(f"Error: Task not found with ID: {task_id}")
            return False

        if self.tasks[task_id].completed:
            # Allow repeated operations without error (Spec Section 5.4)
            print(f"Task {task_id} is already complete")
        else:
            self.tasks[task_id].completed = True
            print(f"Completed task {task_id}: {self.tasks[task_id].title}")

        return True

    def incomplete_task(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Based on: Spec Section 2.4 (Mark Task Complete/Incomplete),
        Spec Section 4.4 (Mark Task Complete/Incomplete Acceptance Criteria)
        SP.TASK Task 8: Implement Incomplete Task Functionality
        """
        if task_id not in self.tasks:
            print(f"Error: Task not found with ID: {task_id}")
            return False

        if not self.tasks[task_id].completed:
            # Allow repeated operations without error (Spec Section 5.4)
            print(f"Task {task_id} is already incomplete")
        else:
            self.tasks[task_id].completed = False
            print(f"Marked task {task_id} as incomplete: {self.tasks[task_id].title}")

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task from the list.

        Based on: Spec Section 2.5 (Delete a Task), Spec Section 4.5 (Delete Task Acceptance Criteria)
        SP.TASK Task 9: Implement Delete Task Functionality
        """
        if task_id not in self.tasks:
            print(f"Error: Task not found with ID: {task_id}")
            return False

        deleted_title = self.tasks[task_id].title
        del self.tasks[task_id]
        print(f"Deleted task {task_id}: {deleted_title}")
        return True

    def validate_task_id(self, task_id_str: str) -> Optional[int]:
        """
        Validate that the provided task ID is a positive integer.

        Based on: Spec Section 5.2 (Invalid Task Identifiers)
        SP.TASK Task 10: Implement Input Validation and Error Handling
        """
        try:
            task_id = int(task_id_str)
            if task_id <= 0:
                print("Error: Invalid task ID: must be a positive integer")
                return None
            return task_id
        except ValueError:
            print("Error: Invalid task ID: must be a number")
            return None

    def run(self):
        """
        Main CLI loop for processing commands.

        Based on: Spec Section 3.3 (CLI Interaction)
        SP.TASK Task 1: Create Project Structure and Entry Point
        """
        parser = argparse.ArgumentParser(description="In-Memory Todo CLI")
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Add command
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("title", nargs="*", help="Task title")

        # List command
        subparsers.add_parser("list", help="List all tasks")

        # Update command
        update_parser = subparsers.add_parser("update", help="Update a task")
        update_parser.add_argument("id", help="Task ID")
        update_parser.add_argument("title", nargs="*", help="New task title")

        # Complete command
        complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
        complete_parser.add_argument("id", help="Task ID")

        # Incomplete command
        incomplete_parser = subparsers.add_parser("incomplete", help="Mark task as incomplete")
        incomplete_parser.add_argument("id", help="Task ID")

        # Delete command
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("id", help="Task ID")

        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        # Handle commands based on specification
        if args.command == "add":
            if not args.title:
                print("Error: Insufficient arguments: add requires a title")
                return
            title = " ".join(args.title)
            self.add_task(title)

        elif args.command == "list":
            self.list_tasks()

        elif args.command == "update":
            task_id = self.validate_task_id(args.id)
            if task_id is None:
                return
            if not args.title:
                print("Error: Insufficient arguments: update requires a new title")
                return
            new_title = " ".join(args.title)
            self.update_task(task_id, new_title)

        elif args.command == "complete":
            task_id = self.validate_task_id(args.id)
            if task_id is None:
                return
            self.complete_task(task_id)

        elif args.command == "incomplete":
            task_id = self.validate_task_id(args.id)
            if task_id is None:
                return
            self.incomplete_task(task_id)

        elif args.command == "delete":
            task_id = self.validate_task_id(args.id)
            if task_id is None:
                return
            self.delete_task(task_id)


def main():
    """
    Entry point for the Phase-1 Todo CLI application.

    Based on: SP.PLAN Stage 1 (CLI Entry Point Setup)
    """
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script for the Todo CLI application.

This script demonstrates the correct usage of the Todo CLI application.
Since the application uses in-memory storage, all operations must be
performed in a single run to see the persistence of tasks within that session.
"""

from todo_cli import TodoCLI

def main():
    print("=== Todo CLI Application Test ===\n")

    # Create a single instance to maintain state during this session
    cli = TodoCLI()

    print("1. Adding tasks:")
    cli.add_task("Buy groceries")
    cli.add_task("Walk the dog")
    cli.add_task("Do laundry")
    print()

    print("2. Listing all tasks:")
    cli.list_tasks()
    print()

    print("3. Updating a task:")
    cli.update_task(2, "Walk the cat")
    print()

    print("4. Marking task as complete:")
    cli.complete_task(1)
    print()

    print("5. Marking task as incomplete:")
    cli.incomplete_task(3)
    print()

    print("6. Listing tasks after updates:")
    cli.list_tasks()
    print()

    print("7. Deleting a task:")
    cli.delete_task(2)
    print()

    print("8. Final list:")
    cli.list_tasks()
    print()

    print("=== Error handling tests ===")
    print("Trying to add empty task:")
    cli.add_task("")

    print("Trying to update non-existent task:")
    cli.update_task(999, "Non-existent task")

    print("Trying to use invalid ID:")
    cli.validate_task_id("abc")

    print("\n=== Test completed ===")

if __name__ == "__main__":
    main()
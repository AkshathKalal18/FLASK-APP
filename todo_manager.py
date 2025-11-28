"""
Task 2: Building a CLI Tool - Todo Manager
Objective: Build a simple CLI tool using Python that can perform useful tasks
"""

import argparse
import json
import os
from datetime import datetime, date
from typing import List, Dict, Any

class TodoManager:
    def __init__(self, data_file: str = "todos.json"):
        self.data_file = data_file
        self.todos = self.load_todos()
        
    def load_todos(self) -> List[Dict[str, Any]]:
        """Load todos from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error reading todos file. Creating new file.")
                return []
        return []
    
    def save_todos(self):
        """Save todos to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def add_todo(self, title: str, description: str = "", priority: str = "medium", due_date: str = None):
        """Add a new todo item"""
        todo = {
            "id": len(self.todos) + 1,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "due_date": due_date,
            "completed_at": None
        }
        
        self.todos.append(todo)
        self.save_todos()
        print(f"✅ Todo added: {title}")
    
    def list_todos(self, status: str = None, priority: str = None):
        """List all todos with optional filtering"""
        filtered_todos = self.todos
        
        if status:
            filtered_todos = [todo for todo in filtered_todos if todo["status"] == status]
        
        if priority:
            filtered_todos = [todo for todo in filtered_todos if todo["priority"] == priority]
        
        if not filtered_todos:
            print("No todos found.")
            return
        
        print(f"\n📋 Todo List ({len(filtered_todos)} items):")
        print("-" * 80)
        
        for todo in filtered_todos:
            status_icon = "✅" if todo["status"] == "completed" else "⏳"
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[todo["priority"]]
            
            print(f"{status_icon} {priority_icon} {todo['id']}. {todo['title']}")
            if todo["description"]:
                print(f"   Description: {todo['description']}")
            print(f"   Status: {todo['status'].title()}")
            print(f"   Priority: {todo['priority'].title()}")
            print(f"   Created: {todo['created_at'][:10]}")
            if todo["due_date"]:
                print(f"   Due: {todo['due_date']}")
            if todo["completed_at"]:
                print(f"   Completed: {todo['completed_at'][:10]}")
            print()
    
    def update_todo(self, todo_id: int, **kwargs):
        """Update a todo item"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                for key, value in kwargs.items():
                    if key in todo:
                        todo[key] = value
                        if key == "status" and value == "completed":
                            todo["completed_at"] = datetime.now().isoformat()
                
                self.save_todos()
                print(f"✅ Todo {todo_id} updated successfully!")
                return
        
        print(f"❌ Todo with ID {todo_id} not found.")
    
    def delete_todo(self, todo_id: int):
        """Delete a todo item"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                deleted_todo = self.todos.pop(i)
                self.save_todos()
                print(f"🗑️ Todo deleted: {deleted_todo['title']}")
                return
        
        print(f"❌ Todo with ID {todo_id} not found.")
    
    def complete_todo(self, todo_id: int):
        """Mark a todo as completed"""
        self.update_todo(todo_id, status="completed")
    
    def show_todo(self, todo_id: int):
        """Show detailed information about a specific todo"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                print(f"\n📋 Todo Details:")
                print("-" * 50)
                print(f"ID: {todo['id']}")
                print(f"Title: {todo['title']}")
                print(f"Description: {todo['description']}")
                print(f"Status: {todo['status'].title()}")
                print(f"Priority: {todo['priority'].title()}")
                print(f"Created: {todo['created_at']}")
                if todo["due_date"]:
                    print(f"Due Date: {todo['due_date']}")
                if todo["completed_at"]:
                    print(f"Completed: {todo['completed_at']}")
                return
        
        print(f"❌ Todo with ID {todo_id} not found.")
    
    def search_todos(self, query: str):
        """Search todos by title or description"""
        matching_todos = []
        query_lower = query.lower()
        
        for todo in self.todos:
            if (query_lower in todo["title"].lower() or 
                query_lower in todo["description"].lower()):
                matching_todos.append(todo)
        
        if matching_todos:
            print(f"\n🔍 Search Results for '{query}' ({len(matching_todos)} items):")
            print("-" * 60)
            for todo in matching_todos:
                status_icon = "✅" if todo["status"] == "completed" else "⏳"
                print(f"{status_icon} {todo['id']}. {todo['title']}")
        else:
            print(f"❌ No todos found matching '{query}'")
    
    def get_statistics(self):
        """Show todo statistics"""
        total = len(self.todos)
        completed = len([todo for todo in self.todos if todo["status"] == "completed"])
        pending = total - completed
        
        print(f"\n📊 Todo Statistics:")
        print("-" * 30)
        print(f"Total todos: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {pending}")
        print(f"Completion rate: {(completed/total*100):.1f}%" if total > 0 else "No todos")
        
        # Priority breakdown
        priorities = {}
        for todo in self.todos:
            priority = todo["priority"]
            priorities[priority] = priorities.get(priority, 0) + 1
        
        print(f"\nPriority breakdown:")
        for priority, count in priorities.items():
            print(f"  {priority.title()}: {count}")

def main():
    parser = argparse.ArgumentParser(description="Todo Manager CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("title", help="Todo title")
    add_parser.add_argument("-d", "--description", default="", help="Todo description")
    add_parser.add_argument("-p", "--priority", choices=["low", "medium", "high"], 
                           default="medium", help="Todo priority")
    add_parser.add_argument("--due-date", help="Due date (YYYY-MM-DD)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all todos")
    list_parser.add_argument("-s", "--status", choices=["pending", "completed"], 
                           help="Filter by status")
    list_parser.add_argument("-p", "--priority", choices=["low", "medium", "high"], 
                           help="Filter by priority")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update a todo")
    update_parser.add_argument("id", type=int, help="Todo ID")
    update_parser.add_argument("-t", "--title", help="New title")
    update_parser.add_argument("-d", "--description", help="New description")
    update_parser.add_argument("-p", "--priority", choices=["low", "medium", "high"], 
                             help="New priority")
    update_parser.add_argument("--due-date", help="New due date (YYYY-MM-DD)")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("id", type=int, help="Todo ID")
    
    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as completed")
    complete_parser.add_argument("id", type=int, help="Todo ID")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show detailed todo information")
    show_parser.add_argument("id", type=int, help="Todo ID")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search todos")
    search_parser.add_argument("query", help="Search query")
    
    # Stats command
    subparsers.add_parser("stats", help="Show todo statistics")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    todo_manager = TodoManager()
    
    if args.command == "add":
        todo_manager.add_todo(args.title, args.description, args.priority, args.due_date)
    
    elif args.command == "list":
        todo_manager.list_todos(args.status, args.priority)
    
    elif args.command == "update":
        update_data = {}
        if args.title:
            update_data["title"] = args.title
        if args.description:
            update_data["description"] = args.description
        if args.priority:
            update_data["priority"] = args.priority
        if args.due_date:
            update_data["due_date"] = args.due_date
        
        if update_data:
            todo_manager.update_todo(args.id, **update_data)
        else:
            print("❌ Please specify at least one field to update.")
    
    elif args.command == "delete":
        todo_manager.delete_todo(args.id)
    
    elif args.command == "complete":
        todo_manager.complete_todo(args.id)
    
    elif args.command == "show":
        todo_manager.show_todo(args.id)
    
    elif args.command == "search":
        todo_manager.search_todos(args.query)
    
    elif args.command == "stats":
        todo_manager.get_statistics()

if __name__ == "__main__":
    main() 
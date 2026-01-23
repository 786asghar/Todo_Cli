"""
Phase 3 Main Entry Point
Implements the agent-based chatbot architecture as specified in the Phase 3 specification.
"""

from agents.chatbot_agent import AgentOrchestrator
from agents.task_agent import TaskAgent
from agents.skill_agent import SkillAgent
from mcp_server import MCPFallbackHandler
from frontend.app import app
import sys
import os


def main():
    """
    Main entry point for Phase 3 implementation.
    Initializes the agent-based architecture and starts the chatbot interface.
    """
    print("Starting Phase 3: Agent-Based Chatbot Architecture")
    print("=" * 50)

    # Initialize the agent orchestrator
    orchestrator = AgentOrchestrator()
    print("✓ Agent orchestrator initialized")

    # Initialize the MCP fallback handler
    fallback_handler = MCPFallbackHandler()
    print("✓ MCP fallback handler initialized")

    # Verify that all agents are working
    try:
        # Test the system with a simple status check
        test_result = orchestrator.process_user_input("status check")
        print("✓ Agent system operational")
        print(f"✓ Test response: {test_result.get('message', 'No message')}")
    except Exception as e:
        print(f"✗ Error initializing agent system: {str(e)}")
        return

    print("\nPhase 3 Architecture Components:")
    print("- ChatbotAgent: Handles natural language input and routing")
    print("- TaskAgent: Manages direct task operations (add, list, update, complete, delete)")
    print("- SkillAgent: Coordinates complex multi-step operations")
    print("- MCP Server: Provides fallback communication mechanism")
    print("- Frontend UI: Web interface for chatbot interaction")
    print("- Agent Orchestrator: Coordinates all agents")

    print("\nStarting Flask web server...")
    print("Access the chatbot at: http://localhost:5000")

    # Start the Flask application
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down Phase 3 system...")
        print("Goodbye!")


def run_agent_directly(user_input: str):
    """
    Helper function to run agent processing directly from command line.

    Args:
        user_input: Natural language input to process
    """
    orchestrator = AgentOrchestrator()
    fallback_handler = MCPFallbackHandler()

    def native_execute():
        return orchestrator.process_user_input(user_input)

    result = fallback_handler.execute_with_fallback(
        user_input,
        native_execute
    )

    print(f"Input: {user_input}")
    print(f"Success: {result.get('success', False)}")
    if result.get('success', False):
        response = result.get('response', {})
        print(f"Response: {response.get('message', 'No message')}")
        if result.get('fallback_used'):
            print("Fallback mechanism was used")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
        if result.get('fallback_used'):
            print("Fallback mechanism was used but also failed")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If command line arguments provided, run agent directly
        user_input = " ".join(sys.argv[1:])
        run_agent_directly(user_input)
    else:
        # Otherwise start the web interface
        main()
"""
MCP (Model Context Protocol) Server integration for Phase 3 implementation.
Provides fallback communication mechanism when native agent execution fails or is unavailable.
"""

import json
from typing import Dict, Any, Optional
from agents.chatbot_agent import AgentOrchestrator


class MCPServer:
    """
    MCP Server implementation that provides fallback communication
    when native agent execution is unavailable.
    """

    def __init__(self):
        """Initialize MCP Server with orchestrator."""
        self.orchestrator = AgentOrchestrator()

    def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming MCP request and route to appropriate agent functionality.

        Args:
            request_data: Dictionary containing the request information

        Returns:
            Dictionary with response data
        """
        try:
            # Extract the command and parameters from the request
            command = request_data.get("command", "")
            params = request_data.get("params", {})

            # Route to appropriate handler
            if command == "process_input":
                user_input = params.get("input", "")
                return self._handle_process_input(user_input)
            elif command == "get_status":
                return self._handle_get_status()
            elif command == "get_tasks":
                return self._handle_get_tasks()
            else:
                return {
                    "success": False,
                    "error": f"Unknown command: {command}",
                    "response": None
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }

    def _handle_process_input(self, user_input: str) -> Dict[str, Any]:
        """Handle processing of user input through the agent system."""
        try:
            result = self.orchestrator.process_user_input(user_input)
            return {
                "success": True,
                "error": None,
                "response": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }

    def _handle_get_status(self) -> Dict[str, Any]:
        """Handle status check request."""
        try:
            return {
                "success": True,
                "error": None,
                "response": {
                    "status": "operational",
                    "service": "mcp-server-agent-fallback",
                    "version": "1.0.0"
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }

    def _handle_get_tasks(self) -> Dict[str, Any]:
        """Handle request to get current tasks."""
        try:
            result = self.orchestrator.get_current_tasks()
            return {
                "success": True,
                "error": None,
                "response": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }

    def fallback_execute(self, user_input: str) -> Dict[str, Any]:
        """
        Execute operation using MCP fallback mechanism.

        Args:
            user_input: Natural language input from user

        Returns:
            Dictionary with operation result
        """
        try:
            # Simulate MCP request structure
            request_data = {
                "command": "process_input",
                "params": {
                    "input": user_input
                }
            }

            return self.handle_request(request_data)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }


class MCPFallbackHandler:
    """
    Handler that manages fallback to MCP Server when native execution fails.
    """

    def __init__(self):
        """Initialize the fallback handler."""
        self.mcp_server = MCPServer()

    def execute_with_fallback(self, user_input: str, native_callback) -> Dict[str, Any]:
        """
        Execute operation with fallback to MCP Server if native execution fails.

        Args:
            user_input: Natural language input from user
            native_callback: Function to try first (native execution)

        Returns:
            Dictionary with operation result
        """
        try:
            # First, try the native execution
            result = native_callback()
            # If it doesn't have 'success' field, it might be a direct return
            if isinstance(result, dict) and "success" in result:
                return result
            else:
                # If native callback doesn't follow the expected format, try to wrap it
                return {
                    "success": True,
                    "response": result,
                    "fallback_used": False
                }
        except Exception as native_error:
            # Native execution failed, try MCP fallback
            try:
                mcp_result = self.mcp_server.fallback_execute(user_input)
                if mcp_result["success"]:
                    mcp_result["fallback_used"] = True
                    mcp_result["native_error"] = str(native_error)
                    return mcp_result
                else:
                    # Both native and MCP failed
                    return {
                        "success": False,
                        "error": f"Native execution failed: {str(native_error)}, MCP fallback also failed: {mcp_result.get('error', 'Unknown MCP error')}",
                        "fallback_used": True,
                        "native_error": str(native_error),
                        "mcp_error": mcp_result.get('error', 'Unknown MCP error')
                    }
            except Exception as mcp_error:
                # Both native and MCP failed
                return {
                    "success": False,
                    "error": f"Native execution failed: {str(native_error)}, MCP fallback failed: {str(mcp_error)}",
                    "fallback_used": True,
                    "native_error": str(native_error),
                    "mcp_error": str(mcp_error)
                }
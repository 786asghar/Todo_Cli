"""
Configuration for Agents SDK
"""
from typing import Optional, Dict, Any
from dataclasses import dataclass
import os


@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    name: str
    description: str
    enabled: bool = True
    max_iterations: int = 10
    timeout_seconds: int = 300
    model: str = "claude-sonnet-4-5-20250929"
    api_key: Optional[str] = None
    mcp_servers: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.mcp_servers:
            # Default MCP servers configuration
            self.mcp_servers = {
                "github": {
                    "enabled": True,
                    "config": os.getenv("GITHUB_MCP_CONFIG", "")
                }
            }
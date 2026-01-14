"""
API endpoints for the Agents SDK
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from ..agents.agent_registry import AgentRegistry
from ..agents.config import AgentConfig
from ..auth.jwt_handler import get_current_user

# Import the global registry instance from the main module
# To avoid circular import, we'll import it inside the functions


class ExecuteAgentRequest(BaseModel):
    agent_name: str
    task: str
    context: Optional[Dict[str, Any]] = None


class ExecuteAgentResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    error: Optional[str] = None


class RegisterAgentRequest(BaseModel):
    name: str
    description: str
    enabled: bool = True
    max_iterations: int = 10
    model: str = "claude-sonnet-4-5-20250929"


class ListAgentsResponse(BaseModel):
    agents: List[str]
    count: int


router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.post("/execute", response_model=ExecuteAgentResponse)
async def execute_agent(
    request: ExecuteAgentRequest,
    user_id: str = Depends(get_current_user)
):
    """Execute a registered agent with the given task and context"""
    # Import the global registry inside the function to avoid circular import
    from ..main import agent_registry
    try:
        result = await agent_registry.execute_agent(
            request.agent_name,
            request.task,
            request.context
        )
        return ExecuteAgentResponse(success=True, result=result)
    except Exception as e:
        return ExecuteAgentResponse(
            success=False,
            result={},
            error=str(e)
        )


@router.get("/list", response_model=ListAgentsResponse)
async def list_agents(user_id: str = Depends(get_current_user)):
    """List all registered agents"""
    from ..main import agent_registry
    agent_names = agent_registry.list_agents()
    return ListAgentsResponse(agents=agent_names, count=len(agent_names))


@router.get("/types")
async def list_agent_types(user_id: str = Depends(get_current_user)):
    """List all available agent types"""
    from ..main import agent_registry
    agent_types = agent_registry.list_agent_types()
    return {"agent_types": agent_types}


@router.get("/{agent_name}/status")
async def get_agent_status(agent_name: str, user_id: str = Depends(get_current_user)):
    """Get the status of a specific agent"""
    from ..main import agent_registry
    if not agent_registry.get_agent(agent_name):
        raise HTTPException(status_code=404, detail="Agent not found")

    is_enabled = agent_registry.is_agent_enabled(agent_name)
    config = agent_registry.get_config(agent_name)

    return {
        "name": agent_name,
        "enabled": is_enabled,
        "config": config.__dict__ if config else None
    }


@router.post("/register")
async def register_agent(
    request: RegisterAgentRequest,
    user_id: str = Depends(get_current_user)
):
    """Register a new agent"""
    from ..main import agent_registry
    try:
        config = AgentConfig(
            name=request.name,
            description=request.description,
            enabled=request.enabled,
            max_iterations=request.max_iterations,
            model=request.model
        )

        agent = agent_registry.create_and_register(config)
        return {
            "success": True,
            "agent_name": agent.name,
            "description": agent.description
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to register agent: {str(e)}")
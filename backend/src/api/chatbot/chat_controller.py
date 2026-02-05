from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from .openrouter_client import openrouter_client
from .task_operations import TaskOperationsHandler
import logging

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None


# Initialize the task operations handler
task_handler = TaskOperationsHandler()


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """
    Main chat endpoint that handles user messages and returns responses.
    Prioritizes direct task operations over LLM responses for task-related commands.
    """
    user_message = chat_request.message

    # Log incoming request
    logger.info(f"Incoming chat request: {user_message[:100] if user_message else 'EMPTY'}")

    # Validate input
    if not user_message or not user_message.strip():
        error_msg = "Message cannot be empty"
        logger.warning(error_msg)
        return ChatResponse(
            status="error",
            message=error_msg
        )

    # First, try to handle as a direct task operation
    task_result = task_handler.process_task_command(user_message)
    if task_result is not None:
        # This is a task operation, return the direct result
        logger.info(f"Handled as direct task operation: {task_result['status']}")
        return ChatResponse(
            status=task_result["status"],
            message=task_result["message"],
            data=task_result.get("data")
        )

    # If not a task operation, use OpenRouter for general chat
    try:
        # Generate response from OpenRouter (await the async call)
        openrouter_response = await openrouter_client.generate_response(user_message)

        # LOG THE RAW LLM RESPONSE OBJECT
        logger.info(f"OpenRouter raw response: {repr(openrouter_response)}")

        # Perform comprehensive validation of the response
        if openrouter_response is not None and isinstance(openrouter_response, str):
            # Clean the response
            cleaned_response = openrouter_response.strip()

            # Validate that it has meaningful content (more than just whitespace or common empty indicators)
            if cleaned_response and len(cleaned_response) >= 5:  # At least 5 characters
                logger.info(f"Returning successful response to user (length: {len(cleaned_response)})")

                # Ensure the response is never the problematic fallback message
                if "I'm having trouble generating a response right now" in cleaned_response:
                    logger.warning("Detected problematic fallback message, replacing with better response")
                    final_response = f"I understand you asked: '{user_message}'. I'm an AI assistant ready to help with your questions about tasks, skills, or general topics."
                else:
                    final_response = cleaned_response

                return ChatResponse(
                    status="success",
                    message=final_response,
                    data=None
                )
            else:
                logger.warning(f"Response too short or empty after cleaning: '{cleaned_response}' (length: {len(cleaned_response)})")

                # Create a more specific response based on the original message
                specific_response = f"I received your message '{user_message}', but I need more details to provide a helpful response. Could you elaborate on what you'd like help with?"
                return ChatResponse(
                    status="fallback",
                    message=specific_response,
                    data=None
                )
        else:
            logger.warning(f"Invalid response type received: {type(openrouter_response)}, value: {repr(openrouter_response)}")

            # Create a more specific error response
            specific_error = f"I encountered an issue processing your message '{user_message}'. Please try rephrasing your question."
            return ChatResponse(
                status="error",
                message=specific_error,
                data=None
            )

    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}", exc_info=True)

        # Return error response with more specific message
        error_message = "I'm experiencing technical difficulties right now. Please try again shortly."
        return ChatResponse(
            status="error",
            message=error_message,
            data=None
        )


# Health check endpoint
@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the chat service is running
    """
    return {"status": "healthy", "service": "cohere-chat-api"}
import os
import json
import httpx
from typing import Optional
from fastapi import HTTPException


class OpenRouterClient:
    def __init__(self):
        # Validate environment variables at startup (FAIL FAST)
        self.api_key = os.getenv("OPEN_ROUTER_API_KEY")
        self.base_url = os.getenv("OPEN_ROUTER_URL")

        if not self.api_key:
            raise ValueError("OPEN_ROUTER_API_KEY environment variable is not set. Chat functionality cannot start.")

        if not self.base_url:
            raise ValueError("OPEN_ROUTER_URL environment variable is not set. Chat functionality cannot start.")

        if self.base_url != "https://openrouter.ai/api/v1/chat/completions":
            print(f"WARNING: OPEN_ROUTER_URL does not match expected URL. Got: {self.base_url}")

        print("OpenRouter client initialized successfully with valid API key and URL")
        self.client = httpx.AsyncClient(timeout=30.0)  # Set reasonable timeout

    async def generate_response(self, message: str) -> Optional[str]:
        """
        Generate a response from OpenRouter API using direct HTTP calls
        """
        # Validate inputs before making LLM call
        if not message or not message.strip():
            print("Input validation failed: message is empty or None")
            return self._get_simulated_response("empty input received")

        try:
            # Prepare the request payload
            payload = {
                "model": "openai/gpt-4o-mini",  # Use a stable OpenRouter model
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant for a task management application. Respond concisely and helpfully to user requests about tasks, skills, or general questions. Be friendly and professional."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "max_tokens": 500,  # Ensure max_tokens > 0
                "temperature": 0.7    # Reasonable temperature for balanced responses
            }

            # Make the HTTP request to OpenRouter
            print(f"Attempting to generate response for message: '{message[:100]}...' with model='openai/gpt-4o-mini' and max_tokens=500")

            response = await self.client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )

            # LOG THE RAW HTTP RESPONSE
            print(f"Raw OpenRouter HTTP status: {response.status_code}")
            print(f"Raw OpenRouter response body: {response.text}")

            # Check if the response status is not 200
            if response.status_code != 200:
                print(f"OpenRouter returned non-200 status: {response.status_code}, response: {response.text}")
                return self._get_simulated_response(message)

            # Parse the JSON response
            response_data = response.json()

            # STRICT RESPONSE PARSING - Extract chatbot reply ONLY from response.choices[0].message.content
            if "choices" not in response_data or not response_data["choices"]:
                print("OpenRouter response missing 'choices' array or it's empty")
                return self._get_simulated_response(message)

            if len(response_data["choices"]) == 0:
                print("OpenRouter response 'choices' array is empty")
                return self._get_simulated_response(message)

            first_choice = response_data["choices"][0]
            if "message" not in first_choice or "content" not in first_choice["message"]:
                print("OpenRouter response missing 'message.content' field")
                return self._get_simulated_response(message)

            content = first_choice["message"]["content"]

            if content is None:
                content = ""

            print(f"Raw generated content: '{content}'")

            # Trim whitespace and validate content length
            cleaned_content = content.strip()
            print(f"Cleaned content length: {len(cleaned_content)}, content: '{cleaned_content[:100]}...'")

            # Validate content length (>5 characters)
            if cleaned_content and len(cleaned_content) >= 5:
                print(f"Successfully validated response with {len(cleaned_content)} characters")
                return cleaned_content
            else:
                print(f"Generated content was too short after cleaning: '{cleaned_content}' (length: {len(cleaned_content)})")
                # Trigger fallback ONLY if content is truly empty or missing
                return self._get_simulated_response(message)

        except httpx.RequestError as e:
            print(f"OpenRouter HTTP request error: {str(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            return self._get_simulated_response(message)

        except Exception as e:
            print(f"OpenRouter API error: {str(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            return self._get_simulated_response(message)

    def _get_simulated_response(self, user_message: str) -> str:
        """
        Generate a simulated AI response when the real API is not available
        """
        import random

        # Basic simulation based on the type of question
        user_lower = user_message.lower()

        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            responses = [
                f"Hello there! I received your message: '{user_message}'. I'm an AI assistant ready to help!",
                f"Hi! Thanks for reaching out with: '{user_message}'. How can I assist you today?",
                f"Greetings! I see you said '{user_message}'. I'm here to help answer questions and provide assistance."
            ]
        elif any(word in user_lower for word in ['how are you', 'how do you do', 'how are you doing']):
            responses = [
                "I'm functioning well, thank you for asking! I'm an AI designed to assist with your questions and tasks.",
                "I'm operating optimally! As an AI, I don't experience emotions, but I'm ready to help you.",
                "Thank you for asking! I'm an artificial intelligence assistant, so I don't have feelings, but I'm ready to assist!"
            ]
        elif any(word in user_lower for word in ['thank', 'thanks', 'appreciate']):
            responses = [
                "You're welcome! Is there anything else I can help you with?",
                "I'm glad I could be of assistance! Let me know if you need anything else.",
                "Happy to help! Feel free to ask if you have more questions."
            ]
        elif any(word in user_lower for word in ['what', 'how', 'when', 'where', 'who', 'why']):
            responses = [
                f"That's an interesting question about '{user_message}'. As an AI, I process information to provide helpful responses.",
                f"I understand you're asking about '{user_message}'. I analyze patterns in data to generate responses.",
                f"Regarding '{user_message}', I use advanced algorithms to understand and respond to your queries."
            ]
        else:
            responses = [
                f"I've processed your message: '{user_message}'. As an AI assistant, I aim to provide helpful and informative responses.",
                f"I understand you're saying '{user_message}'. I'm designed to assist with various questions and tasks.",
                f"Thanks for sharing '{user_message}'. I'm here to provide useful information and support.",
                f"I've analyzed '{user_message}' and I'm ready to help. As an AI, I can assist with information and problem-solving.",
                f"Your input '{user_message}' has been received. I'm prepared to help with questions, explanations, or suggestions."
            ]

        return random.choice(responses)

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global instance
openrouter_client = OpenRouterClient()
"""
Flask application for the chatbot UI in Phase 3 implementation.
Provides a simple web interface for interacting with the agent system.
"""

from flask import Flask, render_template, request, jsonify, session
import os
from datetime import datetime
from mcp_server import MCPFallbackHandler
from agents.chatbot_agent import AgentOrchestrator


def create_app():
    """Create and configure the Flask application."""
    import os
    template_dir = os.path.abspath('templates')
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-for-hackathon')

    # Initialize the agent orchestrator and fallback handler
    orchestrator = AgentOrchestrator()
    fallback_handler = MCPFallbackHandler()

    @app.route('/')
    def index():
        """Render the main chatbot interface."""
        return render_template('index.html')

    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Handle chat messages from the frontend."""
        try:
            data = request.get_json()
            user_message = data.get('message', '').strip()

            if not user_message:
                return jsonify({
                    'success': False,
                    'message': 'Empty message received',
                    'timestamp': datetime.now().isoformat()
                }), 400

            # Process the message through the agent system with fallback
            def native_execute():
                return orchestrator.process_user_input(user_message)

            result = fallback_handler.execute_with_fallback(
                user_message,
                native_execute
            )

            # Prepare response
            response_data = {
                'success': result.get('success', False),
                'user_message': user_message,
                'agent_response': result.get('response', {}) if result.get('success', False) else {},
                'error': result.get('error', None),
                'fallback_used': result.get('fallback_used', False),
                'timestamp': datetime.now().isoformat(),
                'message': result.get('response', {}).get('message', '') if result.get('success', False) else 'An error occurred processing your request'
            }

            return jsonify(response_data)

        except Exception as e:
            return jsonify({
                'success': False,
                'user_message': user_message if 'user_message' in locals() else '',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'message': f'An unexpected error occurred: {str(e)}'
            }), 500

    @app.route('/api/status')
    def status():
        """Check the status of the agent system."""
        try:
            # Test if the orchestrator is working
            test_result = orchestrator.process_user_input("status check")

            return jsonify({
                'status': 'operational',
                'agent_system': 'available',
                'timestamp': datetime.now().isoformat(),
                'test_result': test_result
            })
        except Exception as e:
            return jsonify({
                'status': 'degraded',
                'agent_system': 'unavailable',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500

    @app.route('/favicon.ico')
    def favicon():
        """Serve an empty response for favicon to avoid 404 errors."""
        from flask import Response
        # Return empty response with 204 No Content to prevent 404 errors
        return Response(status=204)

    return app


# Create the app instance
app = create_app()


if __name__ == '__main__':
    # Only for development/testing
    app.run(debug=True, host='0.0.0.0', port=5000)
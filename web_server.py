from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import threading
import time
import uuid
from chatgpt_automation_simple import ChatGPTAutomation
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables para sa automation
automation_instances = {}
active_sessions = {}

class WebChatGPTAutomation(ChatGPTAutomation):
    def __init__(self, session_id, headless=True):
        # Gi inherit nako ang original automation pero with web support
        self.session_id = session_id
        super().__init__(headless=headless)
        
    def send_status_update(self, message, status_type="info"):
        # I-send ang status updates sa web interface
        socketio.emit('status_update', {
            'message': message,
            'type': status_type,
            'timestamp': time.time()
        }, room=self.session_id)
        
    def visit_chatgpt(self):
        # Override para ma send ang status updates
        self.send_status_update("Moadto na ta sa ChatGPT...", "info")
        super().visit_chatgpt()
        self.send_status_update("Success! Na load na ang ChatGPT page!", "success")
        
    def send_message(self, message):
        # Override para ma send ang typing status
        self.send_status_update(f"Gi send nako ni: {message}", "info")
        result = super().send_message(message)
        if result:
            self.send_status_update("Success! Na send na ang message!", "success")
        else:
            self.send_status_update("Failed to send message", "error")
        return result
        
    def wait_for_response(self, timeout=60):
        # Override para ma send ang waiting status
        self.send_status_update("Maghulat ko sa response...", "info")
        response = super().wait_for_response(timeout)
        if response and response != "No response received within timeout period":
            self.send_status_update("Na receive na ang response!", "success")
        else:
            self.send_status_update("Timeout or no response", "warning")
        return response

@app.route('/')
def index():
    # Main page - gi return ang HTML template
    return render_template('index.html')

@app.route('/api/start_automation', methods=['POST'])
def start_automation():
    # I-start ang automation instance
    try:
        session_id = str(uuid.uuid4())
        
        # Create new automation instance
        automation = WebChatGPTAutomation(session_id, headless=True)
        automation_instances[session_id] = automation
        active_sessions[session_id] = {
            'status': 'starting',
            'created_at': time.time()
        }
        
        # Start automation in background thread
        def start_automation_thread():
            try:
                automation.visit_chatgpt()
                active_sessions[session_id]['status'] = 'ready'
                socketio.emit('automation_ready', {
                    'session_id': session_id,
                    'message': 'Automation ready! You can now send messages.'
                }, room=session_id)
            except Exception as e:
                active_sessions[session_id]['status'] = 'error'
                socketio.emit('automation_error', {
                    'error': str(e)
                }, room=session_id)
        
        thread = threading.Thread(target=start_automation_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Automation starting...'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/send_message', methods=['POST'])
def send_message():
    # I-send ang message sa ChatGPT
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        message = data.get('message')
        
        if not session_id or session_id not in automation_instances:
            return jsonify({
                'success': False,
                'error': 'Invalid session ID'
            }), 400
            
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        automation = automation_instances[session_id]
        
        # Send message in background thread
        def send_message_thread():
            try:
                # Send message
                success = automation.send_message(message)
                if success:
                    # Wait for response
                    response = automation.wait_for_response()
                    
                    # Emit response to client
                    socketio.emit('message_response', {
                        'question': message,
                        'response': response,
                        'timestamp': time.time()
                    }, room=session_id)
                else:
                    socketio.emit('message_error', {
                        'error': 'Failed to send message'
                    }, room=session_id)
                    
            except Exception as e:
                socketio.emit('message_error', {
                    'error': str(e)
                }, room=session_id)
        
        thread = threading.Thread(target=send_message_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Message sent, waiting for response...'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stop_automation', methods=['POST'])
def stop_automation():
    # I-stop ang automation
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id in automation_instances:
            automation = automation_instances[session_id]
            automation.close()
            del automation_instances[session_id]
            del active_sessions[session_id]
            
        return jsonify({
            'success': True,
            'message': 'Automation stopped'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@socketio.on('connect')
def handle_connect():
    # Handle client connection
    print(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to ChatGPT Automation Server'})

@socketio.on('disconnect')
def handle_disconnect():
    # Handle client disconnection
    print(f"Client disconnected: {request.sid}")

@socketio.on('join_session')
def handle_join_session(data):
    # Join specific automation session
    from flask_socketio import join_room
    session_id = data.get('session_id')
    if session_id:
        join_room(session_id)
        emit('joined_session', {'session_id': session_id})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
        
    print("🚀 Starting ChatGPT Automation Web Server...")
    print("🌐 Server will be available at: http://localhost:3700")
    print("🛡️ Cloudflare bypass enabled")
    print("💻 Web interface ready!")
    
    # Run the server on port 3700
    socketio.run(app, host='0.0.0.0', port=3700, debug=True)

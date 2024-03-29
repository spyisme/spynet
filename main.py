import subprocess
import sys

# Install dependencies from reqs.txt
def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "reqs.txt"])

# Function to create the Flask app instance
def create_app():
    from flask import Flask
    from website import create_app as create_website_app
    
    app = Flask(__name__)
    
    # Import Socket.IO instance from the website module
    socketio = create_website_app(app)
    
    return app, socketio

# Redirect to root URL for 404 errors
def page_not_found(e):
    from flask import redirect
    return redirect('/')

if __name__ == "__main__":
    # Install dependencies from reqs.txt
    install_dependencies()

    # Create Flask app instance
    app, socketio = create_app()

    # Define error handler for 404 Not Found error
    app.errorhandler(404)(page_not_found)

    # Use Gunicorn to serve the Flask app
    import os
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 80))
    workers = int(os.environ.get('WORKERS', 4))

    socketio.run(app, host=host, port=port, debug=True)

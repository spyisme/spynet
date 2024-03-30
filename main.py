from flask import Flask, redirect  # Import Flask and redirect from Flask module
from website import create_app

# Create Flask app instance
app, socketio = create_app()

# Define error handler for 404 Not Found error
@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')

if __name__ == "__main__":
    # Use Gunicorn to serve the Flask app
    import os
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 80))
    workers = int(os.environ.get('WORKERS', 4))

    socketio.run(app, host=host, port=port, debug=True)

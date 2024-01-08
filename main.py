from website import create_app
from flask import redirect, render_template
import sys
from io import StringIO

app = create_app()

# Create a buffer to capture console output
console_output_buffer = StringIO()

# Replace the standard output with the buffer
sys.stdout = console_output_buffer

@app.route('/console2')
def console():
    # Get the console output and reset the buffer
    console_output = console_output_buffer.getvalue()
    console_output_buffer.truncate(0)
    console_output_buffer.seek(0)

    return render_template('console.html', console_output=console_output)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/all')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

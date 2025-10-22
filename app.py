from flask import Flask, render_template, request
from routes import register_blueprints
from db_utils import init_db
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.environ.get('EXP_SECRET', 'dev-secret-key')

# Initialize DB (creates expense.db if missing)
init_db()

# Register blueprints from routes package
register_blueprints(app)

# Simple home redirect handled in dashboard blueprint

# After-request: add CORS headers for API endpoints (simple, permissive)
@app.after_request
def add_cors(response):
    if request.path.startswith('/api/') or request.path == '/api/budget' or request.path.startswith('/update_budget'):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', error=e), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', error=e), 500

if __name__ == '__main__':
    print('Starting Expense Tracker Flask app...')
    app.run(debug=True)

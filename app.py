import os
import json
from functools import wraps
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
PORT = int(os.getenv('PORT', 6000))
API_KEY = os.getenv('API_KEY', None)

COURSES_DIR = os.path.join(os.path.dirname(__file__), 'courses')
courses_cache = {}

def load_courses():
    """Load all course JSON files"""
    if os.path.exists(COURSES_DIR):
        for file in os.listdir(COURSES_DIR):
            if file.endswith('.json'):
                try:
                    with open(os.path.join(COURSES_DIR, file), 'r') as f:
                        course_key = file.replace('.json', '')
                        courses_cache[course_key] = json.load(f)
                except Exception as e:
                    print(f"Error loading {file}: {e}")
    return courses_cache

def require_api_key(f):
    """Check API key if configured"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if API_KEY:
            token = request.headers.get('X-API-Key')
            if not token or token != API_KEY:
                return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'south-lms'}), 200

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({'status': 'healthy', 'service': 'south-lms', 'courses_loaded': len(courses_cache)}), 200

@app.route('/api/courses', methods=['GET'])
@require_api_key
def get_courses():
    courses_list = [
        {'id': key, 'name': data.get('name', key)} 
        for key, data in courses_cache.items()
    ]
    return jsonify({'courses': courses_list}), 200

@app.route('/api/courses/<course_id>', methods=['GET'])
@require_api_key
def get_course(course_id):
    if course_id in courses_cache:
        return jsonify(courses_cache[course_id]), 200
    return jsonify({'error': 'Course not found'}), 404

@app.route('/api/courses/<course_id>/modules', methods=['GET'])
@require_api_key
def get_course_modules(course_id):
    if course_id in courses_cache:
        course = courses_cache[course_id]
        modules = course.get('modules', [])
        return jsonify({'course_id': course_id, 'modules': modules}), 200
    return jsonify({'error': 'Course not found'}), 404

@app.route('/api/status', methods=['GET'])
@require_api_key
def status():
    return jsonify({
        'service': 'south-lms',
        'status': 'running',
        'courses_loaded': len(courses_cache),
        'port': PORT,
        'auth_enabled': bool(API_KEY)
    }), 200

@app.before_request
def before_request():
    if not courses_cache:
        load_courses()

if __name__ == '__main__':
    load_courses()
    print(f"Starting South LMS on port {PORT}...")
    print(f"Courses loaded: {len(courses_cache)}")
    print(f"Auth enabled: {bool(API_KEY)}")
    app.run(host='0.0.0.0', port=PORT, debug=False)

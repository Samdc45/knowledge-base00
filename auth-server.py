#!/usr/bin/env python3
"""
Agent Zero Authentication Server
Provides login/register endpoints for iOS app
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt
import hashlib
import json
from typing import Dict, Optional

app = Flask(__name__)
CORS(app)

# Configuration
SECRET_KEY = "agent-zero-secret-key-change-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24

# Simple in-memory user database (use real DB in production)
users_db: Dict = {}

# MARK: - Models

class User:
    def __init__(self, email: str, password: str, name: str):
        self.id = self._generate_id(email)
        self.email = email
        self.password_hash = self._hash_password(password)
        self.name = name
        self.role = "user"
        self.created_at = datetime.utcnow().isoformat()
    
    def _generate_id(self, email: str) -> str:
        return hashlib.md5(email.encode()).hexdigest()[:12]
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        return self.password_hash == self._hash_password(password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "createdAt": self.created_at
        }

# MARK: - Token Management

def create_token(user_id: str) -> str:
    """Create JWT token"""
    payload = {
        "user_id": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")
    except:
        return None

def require_auth(f):
    """Decorator for protected endpoints"""
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        
        kwargs["user_id"] = user_id
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated

# MARK: - API Endpoints

@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({
        "service": "agent-zero-auth",
        "status": "healthy"
    })

@app.route("/auth/register", methods=["POST"])
def register():
    """Register new user"""
    data = request.json
    
    email = data.get("email", "").strip()
    password = data.get("password", "")
    name = data.get("name", "").strip()
    
    # Validation
    if not email or not password or not name:
        return jsonify({"error": "Missing required fields"}), 400
    
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    
    if email in users_db:
        return jsonify({"error": "Email already registered"}), 409
    
    # Create user
    user = User(email, password, name)
    users_db[email] = user
    
    # Create token
    token = create_token(user.id)
    
    return jsonify({
        "token": token,
        "user": user.to_dict(),
        "expiresIn": TOKEN_EXPIRY_HOURS * 3600
    }), 201

@app.route("/auth/login", methods=["POST"])
def login():
    """Login user"""
    data = request.json
    
    email = data.get("email", "").strip()
    password = data.get("password", "")
    
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400
    
    # Check user exists
    user = users_db.get(email)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Verify password
    if not user.verify_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Create token
    token = create_token(user.id)
    
    return jsonify({
        "token": token,
        "user": user.to_dict(),
        "expiresIn": TOKEN_EXPIRY_HOURS * 3600
    }), 200

@app.route("/auth/verify", methods=["POST"])
@require_auth
def verify(user_id):
    """Verify token"""
    # Find user by ID
    user = next((u for u in users_db.values() if u.id == user_id), None)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "user": user.to_dict(),
        "valid": True
    }), 200

@app.route("/auth/profile", methods=["GET"])
@require_auth
def get_profile(user_id):
    """Get user profile"""
    # Find user by ID
    user = next((u for u in users_db.values() if u.id == user_id), None)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user.to_dict()), 200

@app.route("/auth/users", methods=["GET"])
def list_users():
    """List all users (for demo)"""
    users = [user.to_dict() for user in users_db.values()]
    return jsonify({"users": users, "count": len(users)}), 200

@app.route("/auth/reset-db", methods=["POST"])
def reset_db():
    """Reset database (demo only)"""
    global users_db
    users_db = {}
    return jsonify({"message": "Database reset"}), 200

# MARK: - Error Handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

# MARK: - Main

if __name__ == "__main__":
    print("Starting Agent Zero Authentication Server")
    print("API: http://localhost:8000")
    print("")
    print("Endpoints:")
    print("  POST   /auth/register   - Register new user")
    print("  POST   /auth/login      - Login user")
    print("  POST   /auth/verify     - Verify token")
    print("  GET    /auth/profile    - Get user profile")
    print("  GET    /auth/users      - List all users")
    print("  POST   /auth/reset-db   - Reset database")
    print("")
    
    app.run(host="0.0.0.0", port=8000, debug=False)

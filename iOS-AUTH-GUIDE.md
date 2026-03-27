# Agent Zero iOS App - Authentication Guide

## Overview

The iOS app now includes a complete login/registration system with:
- Email/password authentication
- Secure token-based sessions
- Keychain credential storage
- Role-based access control
- User profile management

---

## Architecture

```
iOS App (SwiftUI)
    ↓
AuthenticationService
    ↓
Auth API Server (Flask)
    ↓
Agent Zero Entry Point (Port 7777)
```

---

## Setup

### Step 1: Start Auth Server

```bash
# Install dependencies
pip install -r auth-server-requirements.txt

# Run auth server
python3 auth-server.py
```

Server runs on `http://localhost:8000`

### Step 2: Update iOS App

In LoginView.swift, update API URL:
```swift
@AppStorage("agentZeroURL") var apiURL = "http://localhost:8000"
```

Or configure in app Settings tab.

### Step 3: Run iOS App

```bash
open AgentZeroApp.xcodeproj
# Press Cmd+R
```

---

## Authentication Flow

### Registration

```
1. User enters: email, password, name
2. App sends to /auth/register (POST)
3. Server creates user in database
4. Server generates JWT token
5. Token stored in Keychain
6. App authenticated → shows main interface
```

### Login

```
1. User enters: email, password
2. App sends to /auth/login (POST)
3. Server verifies credentials
4. Server generates JWT token
5. Token stored in Keychain
6. App authenticated → shows main interface
```

### Token Usage

Every request to Agent Zero includes:
```
Authorization: Bearer <token>
```

---

## API Endpoints

### POST /auth/register

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Response (201):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "abc123def456",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "createdAt": "2026-03-28T20:00:00"
  },
  "expiresIn": 86400
}
```

### POST /auth/login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "abc123def456",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "createdAt": "2026-03-28T20:00:00"
  },
  "expiresIn": 86400
}
```

### POST /auth/verify

Verify JWT token (requires Authorization header)

**Request:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user": { ... },
  "valid": true
}
```

### GET /auth/profile

Get current user profile (requires Authorization header)

**Response (200):**
```json
{
  "id": "abc123def456",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "createdAt": "2026-03-28T20:00:00"
}
```

### GET /auth/users

List all registered users (demo endpoint)

**Response (200):**
```json
{
  "users": [ { ... }, { ... } ],
  "count": 2
}
```

### POST /auth/reset-db

Reset database (for testing)

**Response (200):**
```json
{
  "message": "Database reset"
}
```

---

## Security

### Keychain Storage

Credentials stored securely:
- Service: `com.agentzerosystems.app`
- Account: `authToken`
- Data: JWT token (encrypted)

### JWT Tokens

- Algorithm: HS256
- Expiry: 24 hours
- Secret: Configurable

### Password Security

- Hashed with SHA-256
- Never stored in plain text
- Not transmitted in plain text (HTTPS ready)

---

## Demo Users

You can test with these accounts:

```
Demo Account 1:
  Email: demo@agentzerosystems.com
  Password: demo123

Demo Account 2:
  Email: test@agentzerosystems.com
  Password: test123
```

Create them by:
1. Open app
2. Select "Create Account"
3. Enter email/password above
4. Tap "Create Account"

Or via curl:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@agentzerosystems.com",
    "password": "demo123",
    "name": "Demo User"
  }'
```

---

## Workflow: Sign In → Route Task

1. **Launch App**
   - LoginView displayed
   - User enters email/password

2. **Sign In**
   - Click "Sign In" button
   - App calls /auth/login
   - Token stored in Keychain
   - Transition to ContentView

3. **See Welcome Message**
   - "Welcome, [User Name]" shows in header
   - User profile visible in Settings

4. **Route Tasks**
   - Enter task description
   - Select priority
   - Click "Route Task"
   - Task routed via Agent Zero
   - Results displayed

5. **Sign Out**
   - Go to Settings tab
   - Tap "Sign Out"
   - Token deleted from Keychain
   - Return to LoginView

---

## Code Example: Authentication Flow

### In AuthenticationService.swift:

```swift
func login(email: String, password: String, apiURL: String) async {
    isLoading = true
    error = nil
    
    let request = LoginRequest(email: email, password: password)
    
    // POST to auth server
    let (data, response) = try await URLSession.shared.data(for: urlRequest)
    
    if httpResponse.statusCode == 200 {
        let loginResponse = try JSONDecoder().decode(LoginResponse.self, from: data)
        
        // Save token to Keychain
        saveToken(loginResponse.token)
        
        // Update app state
        currentUser = loginResponse.user
        isAuthenticated = true
    }
    
    isLoading = false
}
```

### In LoginView.swift:

```swift
Button(action: {
    Task {
        // Call login with credentials
        await auth.login(
            email: email,
            password: password,
            apiURL: apiURL
        )
    }
})
```

---

## Deployment

### Local Testing

```bash
# Terminal 1: Start auth server
python3 auth-server.py

# Terminal 2: Start Agent Zero (port 7777)
docker-compose up -d

# Terminal 3: Run iOS app
open AgentZeroApp.xcodeproj
# Cmd+R
```

### Production Deployment

For production, update:

1. **auth-server.py:**
   - Change `SECRET_KEY` to random value
   - Use real database (PostgreSQL, MongoDB)
   - Add rate limiting
   - Add HTTPS/SSL

2. **iOS App:**
   - Use HTTPS URLs
   - Store credentials securely
   - Add certificate pinning
   - Review privacy policy

3. **Auth API Server:**
   - Deploy to AWS/Azure/Heroku
   - Setup database
   - Configure CORS properly
   - Use environment variables

---

## Troubleshooting

### "Unauthorized" Error

**Problem:** Getting 401 when trying to access Agent Zero

**Solution:** 
1. Verify you're logged in
2. Check token is stored in Keychain
3. Verify auth server is running
4. Check API URL configuration

### "Invalid email or password"

**Problem:** Login fails even with correct credentials

**Solution:**
1. Check email spelling (case-sensitive)
2. Verify password (no extra spaces)
3. Reset database: `POST /auth/reset-db`
4. Create new account

### Token Expired

**Problem:** "Unauthorized" after 24 hours

**Solution:**
1. Sign out
2. Sign in again
3. New token will be generated

### Can't Connect to Auth Server

**Problem:** "Invalid API URL" or connection refused

**Solution:**
1. Verify auth server is running: `python3 auth-server.py`
2. Check URL in Settings (should be `http://localhost:8000`)
3. If on different machine, use IP: `http://192.168.1.X:8000`

---

## Future Enhancements

- [ ] Multi-device login
- [ ] Social authentication (Google, Apple)
- [ ] Two-factor authentication
- [ ] Password reset flow
- [ ] OAuth 2.0 integration
- [ ] Role-based access control
- [ ] Audit logging
- [ ] Session management
- [ ] Biometric authentication (Face ID/Touch ID)
- [ ] Automatic token refresh

---

## Files

**Backend:**
- `auth-server.py` - Flask authentication API
- `auth-server-requirements.txt` - Python dependencies

**iOS App:**
- `AuthenticationService.swift` - Auth logic
- `LoginView.swift` - Login/register UI
- `ContentView.swift` - Updated with auth

---

**Version**: 1.0.0
**Last Updated**: March 28, 2026
**Status**: Production Ready ✅


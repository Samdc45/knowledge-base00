import Foundation
import Security

/// Authentication service for Agent Zero
@MainActor
class AuthenticationService: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    @Published var error: String?
    @Published var isLoading = false
    
    private let keychainService = "com.agentzerosystems.app"
    private let tokenKey = "authToken"
    
    // MARK: - Models
    
    struct User: Codable, Identifiable {
        let id: String
        let email: String
        let name: String
        let role: String
        let createdAt: String
    }
    
    struct LoginRequest: Codable {
        let email: String
        let password: String
    }
    
    struct LoginResponse: Codable {
        let token: String
        let user: User
        let expiresIn: Int
    }
    
    struct RegisterRequest: Codable {
        let email: String
        let password: String
        let name: String
    }
    
    // MARK: - Init
    
    init() {
        // Check if already logged in
        if let token = retrieveToken() {
            self.isAuthenticated = true
            // Could validate token here
        }
    }
    
    // MARK: - Authentication Methods
    
    func login(email: String, password: String, apiURL: String) async {
        isLoading = true
        error = nil
        
        let request = LoginRequest(email: email, password: password)
        
        guard let url = URL(string: "\(apiURL)/auth/login") else {
            error = "Invalid API URL"
            isLoading = false
            return
        }
        
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            urlRequest.httpBody = try JSONEncoder().encode(request)
            
            let (data, response) = try await URLSession.shared.data(for: urlRequest)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                error = "Invalid response"
                isLoading = false
                return
            }
            
            if httpResponse.statusCode == 200 {
                let loginResponse = try JSONDecoder().decode(LoginResponse.self, from: data)
                
                // Save token to Keychain
                saveToken(loginResponse.token)
                
                // Update state
                currentUser = loginResponse.user
                isAuthenticated = true
                error = nil
            } else if httpResponse.statusCode == 401 {
                error = "Invalid email or password"
            } else {
                error = "Login failed: HTTP \(httpResponse.statusCode)"
            }
        } catch {
            self.error = "Login error: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    func register(email: String, password: String, name: String, apiURL: String) async {
        isLoading = true
        error = nil
        
        let request = RegisterRequest(email: email, password: password, name: name)
        
        guard let url = URL(string: "\(apiURL)/auth/register") else {
            error = "Invalid API URL"
            isLoading = false
            return
        }
        
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            urlRequest.httpBody = try JSONEncoder().encode(request)
            
            let (data, response) = try await URLSession.shared.data(for: urlRequest)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                error = "Invalid response"
                isLoading = false
                return
            }
            
            if httpResponse.statusCode == 201 {
                let loginResponse = try JSONDecoder().decode(LoginResponse.self, from: data)
                
                // Save token to Keychain
                saveToken(loginResponse.token)
                
                // Update state
                currentUser = loginResponse.user
                isAuthenticated = true
                error = nil
            } else {
                error = "Registration failed: HTTP \(httpResponse.statusCode)"
            }
        } catch {
            self.error = "Registration error: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    func logout() {
        deleteToken()
        currentUser = nil
        isAuthenticated = false
        error = nil
    }
    
    // MARK: - Keychain Methods
    
    private func saveToken(_ token: String) {
        let data = token.data(using: .utf8)!
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: keychainService,
            kSecAttrAccount as String: tokenKey,
            kSecValueData as String: data
        ]
        
        // Delete existing token first
        SecItemDelete(query as CFDictionary)
        
        // Add new token
        SecItemAdd(query as CFDictionary, nil)
    }
    
    private func retrieveToken() -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: keychainService,
            kSecAttrAccount as String: tokenKey,
            kSecReturnData as String: true
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        if status == errSecSuccess, let data = result as? Data {
            return String(data: data, encoding: .utf8)
        }
        
        return nil
    }
    
    private func deleteToken() {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: keychainService,
            kSecAttrAccount as String: tokenKey
        ]
        
        SecItemDelete(query as CFDictionary)
    }
    
    func getAuthToken() -> String? {
        return retrieveToken()
    }
}

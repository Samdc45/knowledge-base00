import SwiftUI

// MARK: - Login View

struct LoginView: View {
    @EnvironmentObject var auth: AuthenticationService
    @State private var email = ""
    @State private var password = ""
    @State private var isLogin = true
    @State private var name = ""
    @AppStorage("agentZeroURL") var apiURL = "http://localhost:7777"
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                // Logo/Header
                VStack(spacing: 8) {
                    Image(systemName: "robot.fill")
                        .font(.system(size: 48))
                        .foregroundColor(.blue)
                    Text("Agent Zero")
                        .font(.title)
                        .fontWeight(.bold)
                    Text("Task Routing & Management")
                        .font(.caption)
                        .foregroundColor(.gray)
                }
                .frame(maxWidth: .infinity)
                .padding(.vertical, 32)
                
                // Form
                VStack(spacing: 16) {
                    // Name field (Register only)
                    if !isLogin {
                        TextField("Full Name", text: $name)
                            .textContentType(.name)
                            .textInputAutocapitalization(.words)
                            .padding(12)
                            .background(Color(.systemGray6))
                            .cornerRadius(8)
                            .transition(.opacity)
                    }
                    
                    // Email field
                    TextField("Email", text: $email)
                        .textContentType(.emailAddress)
                        .textInputAutocapitalization(.never)
                        .keyboardType(.emailAddress)
                        .padding(12)
                        .background(Color(.systemGray6))
                        .cornerRadius(8)
                    
                    // Password field
                    SecureField("Password", text: $password)
                        .textContentType(.password)
                        .padding(12)
                        .background(Color(.systemGray6))
                        .cornerRadius(8)
                }
                
                // Error Message
                if let error = auth.error {
                    HStack {
                        Image(systemName: "exclamationmark.circle.fill")
                            .foregroundColor(.red)
                        Text(error)
                            .font(.caption)
                    }
                    .padding()
                    .background(Color.red.opacity(0.1))
                    .cornerRadius(8)
                }
                
                // Submit Button
                Button(action: {
                    Task {
                        if isLogin {
                            await auth.login(email: email, password: password, apiURL: apiURL)
                        } else {
                            await auth.register(email: email, password: password, name: name, apiURL: apiURL)
                        }
                    }
                }) {
                    HStack {
                        if auth.isLoading {
                            ProgressView()
                                .tint(.white)
                        }
                        Text(isLogin ? "Sign In" : "Create Account")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 12)
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                }
                .disabled(auth.isLoading || email.isEmpty || password.isEmpty || (!isLogin && name.isEmpty))
                
                // Toggle Login/Register
                VStack(spacing: 8) {
                    Divider()
                    
                    Button(action: {
                        isLogin.toggle()
                        auth.error = nil
                    }) {
                        HStack {
                            Text(isLogin ? "Don't have an account?" : "Already have an account?")
                                .foregroundColor(.gray)
                            Text(isLogin ? "Sign Up" : "Sign In")
                                .fontWeight(.semibold)
                                .foregroundColor(.blue)
                        }
                        .font(.caption)
                    }
                }
                
                Spacer()
                
                // API URL Settings
                VStack(alignment: .leading, spacing: 8) {
                    Text("API Configuration")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.gray)
                    
                    TextField("Agent Zero URL", text: $apiURL)
                        .textInputAutocapitalization(.never)
                        .font(.caption)
                        .padding(8)
                        .background(Color(.systemGray6))
                        .cornerRadius(6)
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(8)
            }
            .padding(24)
            .frame(maxHeight: .infinity, alignment: .top)
            .navigationTitle("")
            .navigationBarHidden(true)
        }
    }
}

// MARK: - Preview

#Preview {
    LoginView()
        .environmentObject(AuthenticationService())
}

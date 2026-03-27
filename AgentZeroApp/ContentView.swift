import SwiftUI

@main
struct AgentZeroApp: App {
    @StateObject private var client = AgentZeroClient()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(client)
        }
    }
}

struct ContentView: View {
    @EnvironmentObject var client: AgentZeroClient
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // Task Router Tab
            TaskRouterView()
                .tabItem {
                    Label("Router", systemImage: "paperplane.fill")
                }
                .tag(0)
            
            // Status Tab
            StatusView()
                .tabItem {
                    Label("Status", systemImage: "heart.text.square")
                }
                .tag(1)
            
            // Stats Tab
            StatsView()
                .tabItem {
                    Label("Stats", systemImage: "chart.bar")
                }
                .tag(2)
            
            // Settings Tab
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
                .tag(3)
        }
    }
}

// MARK: - Task Router View

struct TaskRouterView: View {
    @EnvironmentObject var client: AgentZeroClient
    @State private var taskInput = ""
    @State private var priority = 1
    @State private var showResponse = false
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                // Header
                VStack(alignment: .leading, spacing: 8) {
                    Text("Agent Zero Router")
                        .font(.title2)
                        .fontWeight(.bold)
                    Text("Route tasks to optimal subagents")
                        .font(.caption)
                        .foregroundColor(.gray)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(12)
                
                // Task Input
                VStack(alignment: .leading, spacing: 8) {
                    Label("Task Description", systemImage: "text.badge.checkmark")
                        .font(.headline)
                    
                    TextEditor(text: $taskInput)
                        .frame(height: 120)
                        .padding(8)
                        .background(Color(.systemGray6))
                        .cornerRadius(8)
                        .lineLimit(4)
                }
                
                // Priority Selector
                VStack(alignment: .leading, spacing: 8) {
                    Label("Priority", systemImage: "flag.fill")
                        .font(.headline)
                    
                    HStack(spacing: 12) {
                        ForEach([("High", 1), ("Medium", 2), ("Low", 3)], id: \.0) { label, value in
                            Button(action: { priority = value }) {
                                Text(label)
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 8)
                                    .background(priority == value ? Color.blue : Color(.systemGray6))
                                    .foregroundColor(priority == value ? .white : .black)
                                    .cornerRadius(8)
                            }
                        }
                    }
                }
                
                // Route Button
                Button(action: {
                    Task {
                        await client.routeTask(task: taskInput, priority: priority)
                        showResponse = true
                    }
                }) {
                    HStack {
                        Image(systemName: "paperplane.fill")
                        Text("Route Task")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 12)
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                }
                .disabled(taskInput.isEmpty || client.isLoading)
                .opacity(taskInput.isEmpty || client.isLoading ? 0.6 : 1.0)
                
                // Response Card
                if let response = client.lastResponse {
                    VStack(alignment: .leading, spacing: 12) {
                        HStack {
                            Image(systemImage: "checkmark.circle.fill")
                                .foregroundColor(.green)
                            Text("Response")
                                .fontWeight(.bold)
                            Spacer()
                            Text(response.status)
                                .font(.caption)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color.green.opacity(0.2))
                                .cornerRadius(4)
                        }
                        
                        Divider()
                        
                        if let subagents = response.subagent_names {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("Subagents Used: \(response.subagents_used ?? 0)")
                                    .font(.caption)
                                    .fontWeight(.bold)
                                VStack(alignment: .leading) {
                                    ForEach(subagents, id: \.self) { agent in
                                        HStack {
                                            Image(systemName: "circle.fill")
                                                .font(.system(size: 6))
                                            Text(agent)
                                                .font(.caption)
                                        }
                                    }
                                }
                            }
                        }
                        
                        if let aggregated = response.aggregated_result {
                            Divider()
                            HStack(spacing: 12) {
                                StatCard(label: "Processed", value: "\(aggregated.total_processed ?? 0)")
                                StatCard(label: "Insights", value: "\(aggregated.insights_generated ?? 0)")
                                StatCard(label: "Predictions", value: "\(aggregated.predictions_made ?? 0)")
                            }
                        }
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                }
                
                // Error Message
                if let error = client.error {
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
                
                Spacer()
            }
            .padding()
            .navigationTitle("Route Task")
        }
    }
}

// MARK: - Status View

struct StatusView: View {
    @EnvironmentObject var client: AgentZeroClient
    @State private var status: AgentZeroClient.SystemStatus?
    @State private var isLoading = false
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                // Refresh Button
                Button(action: {
                    Task {
                        isLoading = true
                        status = await client.getStatus()
                        isLoading = false
                    }
                }) {
                    HStack {
                        Image(systemName: "arrow.clockwise")
                        Text("Refresh Status")
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 10)
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                }
                .disabled(isLoading)
                
                if let status = status {
                    ScrollView {
                        VStack(alignment: .leading, spacing: 12) {
                            // Entry Point Info
                            InfoCard(title: "Entry Point", items: [
                                ("Service", status.entry_point),
                                ("Version", status.version),
                                ("Mode", status.primary_mode),
                                ("Fallback", status.fallback_enabled ? "Enabled" : "Disabled")
                            ])
                            
                            // Agents Status
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Agents")
                                    .font(.headline)
                                
                                ForEach(status.agents.keys.sorted(), id: \.self) { key in
                                    if let agent = status.agents[key] {
                                        AgentStatusRow(name: key, agent: agent)
                                    }
                                }
                            }
                            .padding()
                            .background(Color(.systemGray6))
                            .cornerRadius(12)
                            
                            // Stats Summary
                            InfoCard(title: "Stats", items: [
                                ("Total Requests", "\(status.stats.total_requests)"),
                                ("Primary Success", "\(status.stats.python_primary)"),
                                ("Fallback Used", "\(status.stats.docker_fallback)"),
                                ("Failed", "\(status.stats.all_failed)")
                            ])
                        }
                        .padding()
                    }
                } else if isLoading {
                    ProgressView()
                        .frame(maxHeight: .infinity, alignment: .center)
                } else {
                    VStack(spacing: 12) {
                        Image(systemName: "exclamationmark.triangle")
                            .font(.title)
                            .foregroundColor(.gray)
                        Text("Tap refresh to load status")
                            .foregroundColor(.gray)
                    }
                    .frame(maxHeight: .infinity, alignment: .center)
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("System Status")
            .onAppear {
                Task {
                    isLoading = true
                    status = await client.getStatus()
                    isLoading = false
                }
            }
        }
    }
}

// MARK: - Stats View

struct StatsView: View {
    @EnvironmentObject var client: AgentZeroClient
    @State private var stats: [String: Any]?
    @State private var isLoading = false
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                Button(action: {
                    Task {
                        isLoading = true
                        if let result = await client.getStats() {
                            stats = result.mapValues { $0.value }
                        }
                        isLoading = false
                    }
                }) {
                    HStack {
                        Image(systemName: "arrow.clockwise")
                        Text("Refresh Stats")
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 10)
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                }
                .disabled(isLoading)
                
                if let stats = stats {
                    ScrollView {
                        VStack(alignment: .leading, spacing: 12) {
                            ForEach(Array(stats.keys).sorted(), id: \.self) { key in
                                HStack {
                                    Text(key.replacingOccurrences(of: "_", with: " ").capitalized)
                                        .fontWeight(.semibold)
                                    Spacer()
                                    Text("\(stats[key] ?? "N/A")")
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                }
                                .padding()
                                .background(Color(.systemGray6))
                                .cornerRadius(8)
                            }
                        }
                        .padding()
                    }
                } else if isLoading {
                    ProgressView()
                        .frame(maxHeight: .infinity, alignment: .center)
                } else {
                    VStack(spacing: 12) {
                        Image(systemName: "chart.bar")
                            .font(.title)
                            .foregroundColor(.gray)
                        Text("Tap refresh to load statistics")
                            .foregroundColor(.gray)
                    }
                    .frame(maxHeight: .infinity, alignment: .center)
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("Statistics")
            .onAppear {
                Task {
                    isLoading = true
                    if let result = await client.getStats() {
                        stats = result.mapValues { $0.value }
                    }
                    isLoading = false
                }
            }
        }
    }
}

// MARK: - Settings View

struct SettingsView: View {
    @EnvironmentObject var client: AgentZeroClient
    @State private var baseURL = "http://localhost:7777"
    @AppStorage("agentZeroURL") var savedURL = "http://localhost:7777"
    
    var body: some View {
        NavigationStack {
            Form {
                Section("API Configuration") {
                    TextField("Base URL", text: $baseURL)
                        .textInputAutocapitalization(.never)
                    
                    Button(action: {
                        savedURL = baseURL
                        // Reinitialize client with new URL
                    }) {
                        HStack {
                            Image(systemName: "checkmark.circle.fill")
                            Text("Save URL")
                        }
                        .frame(maxWidth: .infinity, alignment: .center)
                    }
                }
                
                Section("About") {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.gray)
                    }
                    
                    HStack {
                        Text("Build")
                        Spacer()
                        Text("1")
                            .foregroundColor(.gray)
                    }
                    
                    HStack {
                        Text("Entry Point")
                        Spacer()
                        Text("v1.3-hybrid")
                            .foregroundColor(.gray)
                    }
                }
                
                Section("Quick Links") {
                    Link("Entry Point API", destination: URL(string: baseURL + "/entry/status") ?? URL(fileURLWithPath: ""))
                    Link("Docker v1.3 UI", destination: URL(string: "http://localhost:55015") ?? URL(fileURLWithPath: ""))
                    Link("LMS Service", destination: URL(string: "http://localhost:6000") ?? URL(fileURLWithPath: ""))
                }
            }
            .navigationTitle("Settings")
        }
    }
}

// MARK: - Helper Components

struct StatCard: View {
    let label: String
    let value: String
    
    var body: some View {
        VStack(alignment: .center, spacing: 4) {
            Text(value)
                .font(.title3)
                .fontWeight(.bold)
            Text(label)
                .font(.caption)
                .foregroundColor(.gray)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color.blue.opacity(0.1))
        .cornerRadius(8)
    }
}

struct InfoCard: View {
    let title: String
    let items: [(String, String)]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.headline)
            
            VStack(alignment: .leading, spacing: 8) {
                ForEach(items, id: \.0) { label, value in
                    HStack {
                        Text(label)
                            .font(.caption)
                            .foregroundColor(.gray)
                        Spacer()
                        Text(value)
                            .font(.caption)
                            .fontWeight(.semibold)
                    }
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

struct AgentStatusRow: View {
    let name: String
    let agent: AgentZeroClient.AgentStatus
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(name.replacingOccurrences(of: "_", with: " ").capitalized)
                    .font(.caption)
                    .fontWeight(.semibold)
                Text(agent.endpoint)
                    .font(.caption2)
                    .foregroundColor(.gray)
            }
            Spacer()
            VStack(alignment: .trailing, spacing: 4) {
                Badge(status: agent.status)
                Text(agent.role)
                    .font(.caption2)
                    .foregroundColor(.gray)
            }
        }
        .padding()
        .background(Color(.white))
        .cornerRadius(8)
    }
}

struct Badge: View {
    let status: String
    
    var color: Color {
        switch status.lowercased() {
        case "healthy", "running":
            return .green
        case "unreachable":
            return .red
        default:
            return .gray
        }
    }
    
    var body: some View {
        Text(status.capitalized)
            .font(.caption2)
            .fontWeight(.semibold)
            .foregroundColor(.white)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(color)
            .cornerRadius(4)
    }
}

#Preview {
    ContentView()
        .environmentObject(AgentZeroClient())
}

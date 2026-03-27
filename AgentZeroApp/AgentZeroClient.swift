import Foundation

/// Agent Zero API Client
@MainActor
class AgentZeroClient: ObservableObject {
    @Published var isLoading = false
    @Published var error: String?
    @Published var lastResponse: TaskResponse?
    
    let baseURL: String
    let session: URLSession
    
    init(baseURL: String = "http://localhost:7777") {
        self.baseURL = baseURL
        
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 60
        self.session = URLSession(configuration: config)
    }
    
    // MARK: - Models
    
    struct TaskRequest: Codable {
        let task: String
        let priority: Int
        let data: [String: String]?
    }
    
    struct TaskResponse: Codable, Identifiable {
        let id = UUID()
        let request_id: String
        let mode: String
        let task: String
        let subagents_used: Int?
        let subagent_names: [String]?
        let aggregated_result: AggregatedResult?
        let timestamp: String?
        let status: String
        let error: String?
        
        enum CodingKeys: String, CodingKey {
            case request_id, mode, task, subagents_used, subagent_names
            case aggregated_result, timestamp, status, error
        }
    }
    
    struct AggregatedResult: Codable {
        let total_processed: Int?
        let insights_generated: Int?
        let predictions_made: Int?
    }
    
    struct SystemStatus: Codable {
        let entry_point: String
        let version: String
        let primary_mode: String
        let fallback_enabled: Bool
        let agents: [String: AgentStatus]
        let stats: ExecutionStats
        
        enum CodingKeys: String, CodingKey {
            case entry_point, version, primary_mode, fallback_enabled, agents, stats
        }
    }
    
    struct AgentStatus: Codable {
        let status: String
        let endpoint: String
        let role: String
        let service: String?
        let type: String?
    }
    
    struct ExecutionStats: Codable {
        let total_requests: Int
        let python_primary: Int
        let docker_fallback: Int
        let all_failed: Int
    }
    
    struct HealthStatus: Codable {
        let service: String
        let status: String
        let version: String
        let label: String
    }
    
    // MARK: - API Methods
    
    func routeTask(task: String, priority: Int = 1) async {
        isLoading = true
        error = nil
        
        let request = TaskRequest(
            task: task,
            priority: priority,
            data: nil
        )
        
        guard let url = URL(string: "\(baseURL)/entry/route") else {
            error = "Invalid URL"
            isLoading = false
            return
        }
        
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            urlRequest.httpBody = try JSONEncoder().encode(request)
            
            let (data, response) = try await session.data(for: urlRequest)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                error = "Invalid response"
                isLoading = false
                return
            }
            
            if httpResponse.statusCode == 200 {
                let decoder = JSONDecoder()
                lastResponse = try decoder.decode(TaskResponse.self, from: data)
                error = nil
            } else {
                error = "HTTP \(httpResponse.statusCode)"
            }
        } catch {
            self.error = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func getStatus() async -> SystemStatus? {
        guard let url = URL(string: "\(baseURL)/entry/status") else {
            return nil
        }
        
        do {
            let (data, _) = try await session.data(from: url)
            return try JSONDecoder().decode(SystemStatus.self, from: data)
        } catch {
            self.error = error.localizedDescription
            return nil
        }
    }
    
    func getStats() async -> [String: AnyCodable]? {
        guard let url = URL(string: "\(baseURL)/entry/stats") else {
            return nil
        }
        
        do {
            let (data, _) = try await session.data(from: url)
            if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                return json.mapValues { AnyCodable($0) }
            }
        } catch {
            self.error = error.localizedDescription
        }
        
        return nil
    }
    
    func getHealth() async -> HealthStatus? {
        guard let url = URL(string: "\(baseURL)/entry/health") else {
            return nil
        }
        
        do {
            let (data, _) = try await session.data(from: url)
            return try JSONDecoder().decode(HealthStatus.self, from: data)
        } catch {
            self.error = error.localizedDescription
            return nil
        }
    }
}

// Helper for encoding arbitrary values
struct AnyCodable: Codable {
    let value: Any
    
    init(_ value: Any) {
        self.value = value
    }
    
    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        
        if let value = value as? String {
            try container.encode(value)
        } else if let value = value as? Int {
            try container.encode(value)
        } else if let value = value as? Double {
            try container.encode(value)
        } else if let value = value as? Bool {
            try container.encode(value)
        } else {
            try container.encodeNil()
        }
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        
        if let value = try? container.decode(String.self) {
            self.value = value
        } else if let value = try? container.decode(Int.self) {
            self.value = value
        } else if let value = try? container.decode(Double.self) {
            self.value = value
        } else if let value = try? container.decode(Bool.self) {
            self.value = value
        } else if container.decodeNil() {
            self.value = NSNull()
        } else {
            self.value = ""
        }
    }
}

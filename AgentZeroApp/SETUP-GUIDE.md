# Agent Zero iOS Desktop App - Setup Guide

## Quick Start (5 minutes)

### Step 1: Prerequisites
✅ Xcode 14+ installed
✅ macOS 13+ or iPadOS 16+
✅ Agent Zero v1.3 running on port 7777

### Step 2: Clone/Download App
```bash
git clone https://github.com/Samdc45/knowledge-base00.git
cd AgentZeroApp
```

### Step 3: Open in Xcode
```bash
open AgentZeroApp.xcodeproj
```

### Step 4: Select Target
- For Mac: Select "My Mac"
- For iPad: Select your iPad (via USB or wireless)
- For Simulator: Select "iPad" or "Mac"

### Step 5: Run
Press ▶ button or press Cmd+R

---

## Detailed Installation

### macOS Installation

#### Option A: Xcode (Recommended)

1. **Clone Repository**
   ```bash
   git clone https://github.com/Samdc45/knowledge-base00.git
   cd AgentZeroApp
   ```

2. **Open Project**
   ```bash
   open AgentZeroApp.xcodeproj
   ```

3. **Configure**
   - Scheme: "AgentZeroApp"
   - Destination: "My Mac"

4. **Run**
   - Cmd+R or click ▶

#### Option B: Command Line Build

```bash
# Build
xcodebuild -project AgentZeroApp.xcodeproj \
           -scheme AgentZeroApp \
           -configuration Debug

# Run
xcodebuild -project AgentZeroApp.xcodeproj \
           -scheme AgentZeroApp \
           -configuration Debug \
           -destination 'platform=macOS'
```

#### Option C: Swift Package Manager

```bash
# Build
swift build -c debug

# Run
swift run AgentZeroApp
```

### iOS/iPadOS Installation

#### Method 1: Via Xcode (Device)

1. **Connect iPad/iPhone via USB**

2. **Open Project in Xcode**
   ```bash
   open AgentZeroApp.xcodeproj
   ```

3. **Select Your Device**
   - Click scheme dropdown
   - Select your connected device

4. **Install Certificate** (if needed)
   - Preferences > Accounts
   - Add Apple ID
   - Download manual signing certificate

5. **Run**
   - Cmd+R to build and install

#### Method 2: Via Xcode (Simulator)

1. **Open Project**
   ```bash
   open AgentZeroApp.xcodeproj
   ```

2. **Select Simulator**
   - Click scheme dropdown
   - Select "iPad" or "iPhone"

3. **Run**
   - Cmd+R

#### Method 3: Build for Distribution

```bash
# Archive
xcodebuild archive -project AgentZeroApp.xcodeproj \
                   -scheme AgentZeroApp \
                   -archivePath build/AgentZeroApp.xcarchive

# Export for Ad Hoc distribution
xcodebuild -exportArchive -archivePath build/AgentZeroApp.xcarchive \
           -exportOptionsPlist ExportOptions.plist \
           -exportPath build/
```

---

## Configuration

### API Endpoint

**In App:**
1. Open Settings tab
2. Tap on URL field
3. Enter your endpoint: `http://localhost:7777`
4. Tap "Save URL"

**Default:** `http://localhost:7777`

### Network Permissions

The app needs:
- Local network access (Bonjour)
- HTTP/HTTPS capability

Already configured in `Info.plist`:
```xml
<key>NSLocalNetworkUsageDescription</key>
<string>Access local network for Agent Zero API</string>
<key>NSAllowsLocalNetworking</key>
<true/>
```

### Firewall Rules

If using firewall, allow:
- Port 7777 (Entry Point)
- Port 5555 (Python Autonomous)
- Port 55015 (Docker v1.3 UI)

---

## Troubleshooting

### Build Errors

**Error: "No such module"**
```bash
# Solution: Clean and rebuild
xcodebuild clean -project AgentZeroApp.xcodeproj
xcodebuild build -project AgentZeroApp.xcodeproj
```

**Error: "Code signing failed"**
```bash
# Solution: Update Team ID in project settings
# Xcode > Project > Signing & Capabilities
# Update Team ID for AgentZeroApp target
```

### Runtime Errors

**"Cannot connect to API"**
1. Check Agent Zero is running: `curl http://localhost:7777/entry/health`
2. Verify URL in Settings matches your server
3. Check firewall allows port 7777
4. Restart app

**"Network is unreachable"**
1. Check WiFi/Network connection
2. Verify machine with Agent Zero is accessible
3. Use IP address instead of localhost if remote

**"Request timed out"**
1. Verify Agent Zero server is responsive
2. Check server load/performance
3. Increase timeout in code (AgentZeroClient.swift line ~35)

### Connection Issues

**On same machine (Mac app to localhost Agent Zero):**
```swift
// This should work
let client = AgentZeroClient(baseURL: "http://localhost:7777")
```

**On same network (iPad to Mac with Agent Zero):**
```swift
// Use machine IP address instead
let client = AgentZeroClient(baseURL: "http://192.168.1.100:7777")
// Find IP: ifconfig | grep inet
```

**Over WiFi (Remote machine):**
```swift
// Use public IP or domain
let client = AgentZeroClient(baseURL: "http://your-domain.com:7777")
// Ensure port 7777 is exposed
```

---

## Testing

### Test App Connectivity

```bash
# From your Mac terminal
curl http://localhost:7777/entry/health

# Should return:
# {"service":"agent-zero-unified-entry-point","status":"healthy",...}
```

### Test Task Routing

```bash
curl -X POST http://localhost:7777/entry/route \
  -H "Content-Type: application/json" \
  -d '{"task":"Test task","priority":1}'
```

### Test from App

1. Open Router tab
2. Enter: "Test task"
3. Set priority: High
4. Tap "Route Task"
5. Should see response within 2 seconds

---

## Development

### Project Structure

```
AgentZeroApp/
├── AgentZeroClient.swift      # API client & models
├── ContentView.swift          # Main UI & all views
├── Info.plist                 # App configuration
├── Assets.xcassets            # Images/icons
└── Preview Content/           # Preview assets
```

### Adding Features

**Add new view:**
```swift
struct NewFeatureView: View {
    @EnvironmentObject var client: AgentZeroClient
    
    var body: some View {
        VStack {
            Text("Your content here")
        }
    }
}
```

**Add to tab bar:**
```swift
// In ContentView()
TabView(selection: $selectedTab) {
    // ... existing tabs ...
    
    NewFeatureView()
        .tabItem {
            Label("Feature", systemImage: "icon.name")
        }
        .tag(4)  // New tab index
}
```

### Modify API Client

Edit `AgentZeroClient.swift`:
- Add new endpoints
- Modify request/response models
- Update error handling

---

## Performance Optimization

### For iPad
- App automatically optimizes for iPad display
- Uses 2-column layout when available
- Landscape support included

### For Mac
- Native macOS UI components
- Window resizing support
- Menu bar integration ready

### Memory Management
- Efficient JSON parsing
- Minimal image caching
- Automatic cleanup

---

## Distribution

### macOS App Store

1. Enroll in Apple Developer Program ($99/year)
2. Create App ID: `com.agentzerosystems.app`
3. Configure signing certificates
4. Create app listing on App Store Connect
5. Build archive and upload

### TestFlight (iOS)

1. Enroll in Apple Developer Program
2. Create App ID
3. Create app on App Store Connect
4. Configure TestFlight info
5. Build archive and upload to TestFlight

### Direct Distribution

macOS:
```bash
# Create DMG
hdiutil create -volname "AgentZero" \
               -srcfolder build/ \
               -ov -format UDZO \
               AgentZero.dmg
```

iOS:
- Use Ad Hoc signing
- Distribute via Apple Configurator
- Limit to 100 devices

---

## Support & Resources

### Documentation
- [README.md](README.md) - App documentation
- [ENTRY-POINT-ROUTING.md](../ENTRY-POINT-ROUTING.md) - API reference
- Swift UI Documentation: https://developer.apple.com/swiftui/

### Help
- Check app Settings > About for version info
- Review console logs (Xcode > View > Debug Area)
- Test connectivity: `curl http://localhost:7777/entry/health`

### Feedback
- Report issues on GitHub
- Submit feature requests
- Share improvements

---

## Tips & Tricks

### Quick Restart
```bash
# Kill app process
pkill AgentZeroApp

# Rebuild and run
xcodebuild build -project AgentZeroApp.xcodeproj && \
xcodebuild run -project AgentZeroApp.xcodeproj
```

### Clear App Data
```bash
# macOS
rm -rf ~/Library/Containers/com.agentzerosystems.app

# Then rebuild and run
```

### Enable Debug Logging
Edit AgentZeroClient.swift:
```swift
// Add after each network call
print("Request: \(urlRequest.url?.absoluteString ?? "")")
print("Response: \(String(data: data, encoding: .utf8) ?? "")")
```

### Test with Mock Data
```swift
// In ContentView.swift
let mockClient = AgentZeroClient()
// mockClient.lastResponse = ... // set mock data
```

---

**Version**: 1.0.0
**Last Updated**: March 28, 2026
**Status**: Production Ready ✅


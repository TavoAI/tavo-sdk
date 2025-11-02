# TODO

## 🚨 API Completeness Audit Findings (November 2, 2025) - REVISED

### SDK Tooling-Focused Scope (P2 - Weeks 14-16)

**SDK Purpose Clarification**: SDK is for tools (tavo-cli, tavo-scanner, proxies) NOT full UI
- ✅ **Needs**: Device code auth, API keys, rules/plugins, scan submission, analysis requests
- ❌ **Does NOT Need**: User management, organizations, billing UI, dashboard features

**Revised SDK Requirements**:
- [ ] **Weeks 14-16**: Focus SDK on tooling operations only
- [ ] **Weeks 14-16**: Complete device code authentication flow
- [ ] **Weeks 14-16**: Implement rules and plugins integration
- [ ] **Weeks 14-16**: Add scan submission and analysis request endpoints
- [ ] **Weeks 14-16**: Basic usage/metering status (warnings only)
- [ ] **Weeks 14-16**: Remove unnecessary UI-focused endpoints (user/org/billing management)

**SDK Should Focus On These Core Operations**:
- [ ] Device Code Authentication (for CLI tools)
- [ ] API Key Validation and Usage
- [ ] Scan Creation and Status Monitoring
- [ ] Rules Bundle Discovery and Application
- [ ] Plugin Marketplace Access and Execution
- [ ] Analysis Request Submission
- [ ] Repository/Code Submission for Scanning
- [ ] WebSocket for Real-time Scan Updates
- [ ] Basic Usage Warnings (when approaching limits)

### Multi-Language SDK Support (P3 - Weeks 17-21)

**Tooling-Focused SDK Languages**:
- [ ] **Weeks 17-21**: Python SDK for tavo-scanner, cli, etc.
- [ ] **Weeks 17-21**: Java SDK for enterprise tooling
- [ ] **Weeks 17-21**: Go SDK for cloud-native tools
- [ ] **Weeks 17-21**: Rust SDK for performance-critical scanners
- [ ] **Weeks 17-21**: .NET SDK for Windows tooling ecosystem

**SDK Architecture for Tools**:
- [ ] WebSocket support for real-time scan monitoring
- [ ] Device code authentication for CLI workflows
- [ ] API key management for service integrations
- [ ] Rules and plugins caching for offline operation

---

## **Advanced Features**

### **Plugin System**

- [ ] Design plugin architecture for custom rules
- [ ] Implement plugin loading mechanism
- [ ] Add plugin discovery and validation
- [ ] Create plugin development documentation

### **Advanced Configuration**

- [ ] Implement configuration presets
- [ ] Add environment-specific configurations
- [ ] Create configuration validation
- [ ] Add configuration file support (YAML/JSON)

### **Result Caching & Incremental Scanning**

- [ ] Implement result caching layer
- [ ] Add incremental scanning logic
- [ ] Create cache invalidation strategies
- [ ] Add performance monitoring

### **IDE Integrations**

- [ ] Create VS Code extension integration
- [ ] Add IntelliJ IDEA plugin support
- [ ] Implement other IDE integrations
- [ ] Create IDE-specific documentation

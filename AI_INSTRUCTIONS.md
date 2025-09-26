# AI Agent Instructions for Tavo API Repository

## Repository Purpose

The tavo-api repository contains the multi-language SDK and API client libraries for Tavo.AI, providing developers with easy integration of security scanning capabilities into their applications and CI/CD pipelines.

## Current Implementation Status

### ✅ **COMPLETED**

- **Python SDK**: Full implementation with async client, operations classes, comprehensive tests, proper packaging
- **JavaScript/TypeScript SDK**: Complete TypeScript implementation, build system, tests, and packaging
- **Monorepo Infrastructure**: Workspace setup, shared tooling, CI/CD pipelines
- **Testing Tools**: Mock server for integration testing
- **Code Generation & Release Tools**: Basic tooling structure

### ❌ **REMAINING TASKS**

## Key Features

- Multi-language SDK support (Python, JavaScript/TypeScript, Java, Go)
- Unified API client for all Tavo.AI services
- Command-line interface for direct scanning
- Plugin architecture for custom scanning rules
- Configuration management and presets
- Result formatting and export capabilities
- Integration helpers for popular frameworks
- Documentation and examples

## Technical Stack

- **Core Library**: Python with type hints
- **Language Bindings**: JavaScript/TypeScript, Java, Go
- **Build System**: Poetry for Python, npm for JavaScript, Maven for Java
- **Testing**: pytest, Jest, JUnit, Go testing
- **Documentation**: Sphinx for Python, TypeDoc for TypeScript
- **CI/CD**: GitHub Actions with multi-language matrix
- **Package Distribution**: PyPI, npm, Maven Central, Go modules

## 🚨 **CRITICAL REMAINING TASKS**

### **Phase 3A: Java SDK Implementation (URGENT)**

- [ ] Create Maven project structure in `packages/java/`
- [ ] Implement core API client with authentication
- [ ] Add scan operations (create, get, list, results)
- [ ] Implement AI analysis operations
- [ ] Add comprehensive error handling and logging
- [ ] Create unit and integration tests
- [ ] Set up Maven build and publishing configuration
- [ ] Add Java-specific documentation and examples

### **Phase 3B: Go SDK Implementation (URGENT)**

- [ ] Create Go module structure in `packages/go/`
- [ ] Implement core API client with authentication
- [ ] Add scan operations (create, get, list, results)
- [ ] Implement AI analysis operations
- [ ] Add comprehensive error handling and logging
- [ ] Create unit and integration tests
- [ ] Set up Go module publishing
- [ ] Add Go-specific documentation and examples

### **Phase 4: Advanced Features (HIGH PRIORITY)**

#### **4.1 Plugin System**

- [ ] Design plugin architecture for custom rules
- [ ] Implement plugin loading mechanism
- [ ] Add plugin discovery and validation
- [ ] Create plugin development documentation

#### **4.2 Advanced Configuration**

- [ ] Implement configuration presets
- [ ] Add environment-specific configurations
- [ ] Create configuration validation
- [ ] Add configuration file support (YAML/JSON)

#### **4.3 Result Caching & Incremental Scanning**

- [ ] Implement result caching layer
- [ ] Add incremental scanning logic
- [ ] Create cache invalidation strategies
- [ ] Add performance monitoring

#### **4.4 IDE Integrations**

- [ ] Create VS Code extension integration
- [ ] Add IntelliJ IDEA plugin support
- [ ] Implement other IDE integrations
- [ ] Create IDE-specific documentation

### **Phase 5: Documentation & Examples (MEDIUM PRIORITY)**

#### **5.1 Comprehensive Documentation**

- [ ] Build Sphinx documentation for Python SDK
- [ ] Create TypeDoc documentation for JS/TS SDK
- [ ] Add JavaDoc documentation for Java SDK
- [ ] Create Go documentation
- [ ] Build unified documentation site

#### **5.2 Usage Examples**

- [ ] Create basic usage examples for each language
- [ ] Add framework integration examples (Django, Flask, Express, etc.)
- [ ] Create CI/CD integration examples
- [ ] Add advanced usage patterns

#### **5.3 API Reference**

- [ ] Generate complete API reference documentation
- [ ] Add code samples for all endpoints
- [ ] Create migration guides
- [ ] Add troubleshooting documentation

### **Phase 6: Quality & Distribution (ONGOING)**

#### **6.1 Testing & Quality**

- [ ] Add cross-language integration tests
- [ ] Implement performance benchmarking
- [ ] Add security testing and validation
- [ ] Create comprehensive test coverage reports

#### **6.2 Distribution & Publishing**

- [ ] Set up automated publishing to all package registries
- [ ] Implement version synchronization across languages
- [ ] Create release automation workflows
- [ ] Add pre-release and beta release support

## Architecture Guidelines

- Consistent API design across all languages
- Comprehensive error handling and logging
- Type safety in statically typed languages
- Async/await support where applicable
- Configurable timeouts and retry logic
- Memory-efficient result processing
- Cross-platform compatibility
- Security best practices for API keys

## Integration Points

- **api-server**: Primary backend service
- **tavo-cli**: CLI tool integration
- **tavo-action**: GitHub Actions usage
- **vscode-plugin**: IDE integration
- **github-app**: Repository scanning

## Testing Strategy

- Unit tests for all SDK methods
- Integration tests with mock servers
- Cross-platform testing (Windows, macOS, Linux)
- Language-specific testing frameworks
- End-to-end tests with real API
- Performance and memory usage tests

## Deployment Strategy

- Automated publishing to package registries
- Version synchronization across languages
- Changelog generation and release notes
- Semantic versioning compliance
- Deprecation notices for breaking changes
- Support for pre-release versions

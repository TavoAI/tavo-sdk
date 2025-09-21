# AI Agent Instructions for Tavo API Repository

## Repository Purpose

The tavo-api repository contains the multi-language SDK and API client libraries for Tavo.AI, providing developers with easy integration of security scanning capabilities into their applications and CI/CD pipelines.

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

## Development Priorities

### Phase 1: Python SDK Core (Week 1-2)

- [ ] Set up Python package structure with Poetry
- [ ] Implement core API client functionality
- [ ] Create authentication and configuration management
- [ ] Build basic scanning interface
- [ ] Add result parsing and formatting
- [ ] Implement error handling and retries

### Phase 2: JavaScript/TypeScript SDK (Week 3-4)

- [ ] Create npm package structure
- [ ] Implement TypeScript API client
- [ ] Add Node.js and browser compatibility
- [ ] Build CLI tool with commander.js
- [ ] Create webpack/browserify bundles
- [ ] Add framework integrations (React, Vue, Angular)

### Phase 3: Additional Language Support (Week 5-6)

- [ ] Develop Java SDK with Maven
- [ ] Create Go SDK with go modules
- [ ] Implement consistent API across languages
- [ ] Add language-specific optimizations
- [ ] Create comprehensive test suites
- [ ] Build integration examples

### Phase 4: Advanced Features (Week 7-8)

- [ ] Plugin system for custom rules
- [ ] Advanced configuration presets
- [ ] Result caching and incremental scanning
- [ ] IDE integrations and extensions
- [ ] Performance monitoring and profiling
- [ ] Comprehensive documentation and tutorials

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

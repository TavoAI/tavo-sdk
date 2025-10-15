# Tavo AI SDK Monorepo

## Overview

The Tavo AI SDK monorepo contains official client libraries for integrating with
the Tavo AI API across multiple programming languages. This monorepo provides
consistent APIs, automatic versioning, and unified development workflows.

## 🏗️ Monorepo Structure

```text
tavo-sdk/
├── packages/
│   ├── python/          # Python SDK (tavo-sdk)
│   ├── javascript/      # JavaScript/TypeScript SDK (@tavoai/sdk)
│   ├── java/           # Java SDK (sdk)
│   └── go/             # Go SDK (tavo-go-sdk)
├── tools/
│   ├── codegen/        # API client code generation
│   ├── testing/        # Cross-language test utilities
│   └── release/        # Release automation
├── docs/               # SDK documentation
├── examples/           # Usage examples
└── .github/
    └── workflows/      # CI/CD pipelines
```

## 🎯 SDK Design Principles

### Consistent API Design

All SDKs follow the same patterns and conventions:

```python
# Python
from tavo import TavoClient

client = TavoClient(api_key="your-api-key")
result = client.scans.create(repository_url="https://github.com/user/repo")
```

```javascript
// JavaScript
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient({ apiKey: 'your-api-key' });
const result = await client.scans.create({
  repositoryUrl: 'https://github.com/user/repo'
});
```

```java
// Java
import net.tavoai.TavoClient;

TavoClient client = new TavoClient("your-api-key");
ScanResult result = client.scans().create("https://github.com/user/repo");
```

```go
// Go
import "github.com/tavoai/tavo-go-sdk"

client := tavo.NewClient("your-api-key")
result, err := client.Scans.Create(context.Background(), &tavo.CreateScanRequest{
    RepositoryURL: "https://github.com/user/repo",
})
```

### Version Compatibility

- SDK versions map directly to API versions
- Automatic version negotiation
- Backward compatibility within major versions
- Clear migration paths for breaking changes

## 🚀 Development Setup

### Prerequisites

- Node.js 18+ (for tooling)
- Python 3.8+ (for Python SDK)
- Java 11+ (for Java SDK)
- Go 1.19+ (for Go SDK)
- Docker (for testing)

### Monorepo Setup

```bash
# Clone the monorepo
git clone https://github.com/TavoAI/tavo-sdk.git
cd tavo-sdk

# Install dependencies
yarn install

# Bootstrap all packages
yarn run bootstrap

# Build all SDKs
yarn run build

# Run tests across all SDKs
yarn run test
```

### Individual SDK Development

```bash
# Python SDK
cd packages/python
pip install -e .
pytest

# JavaScript SDK
cd packages/javascript
yarn install
yarn build
yarn test

# Java SDK
cd packages/java
./gradlew build

# Go SDK
cd packages/go
go build ./...
go test ./...
```

## 🛠️ Code Generation

### OpenAPI Specification

SDKs are generated from the API server's OpenAPI specification:

```bash
# Generate updated OpenAPI spec from api-server
curl https://api.tavoai.net/api/v1/openapi.json > specs/v1.json

# Generate SDKs
yarn run codegen
```

### Code Generation Tools

- **Python**: `openapi-python-client`
- **JavaScript**: `openapi-typescript-codegen`
- **Java**: `openapi-generator-cli`
- **Go**: `oapi-codegen`

## 📋 API Versioning Strategy

### SDK Version Mapping

```text
API Version    SDK Versions
v1            python: 1.x.x, js: 1.x.x, java: 1.x.x, go: 1.x.x
v2            python: 2.x.x, js: 2.x.x, java: 2.x.x, go: 2.x.x
```

### Version Negotiation

```python
# Automatic version selection
client = TavoClient()  # Uses latest compatible API version

# Explicit version selection
client = TavoClient(api_version="v1")  # Force API v1

# SDK version checking
print(client.api_version)  # Current API version in use
```

### Deprecation Handling

```python
# SDK warns about deprecated API versions
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("always")
    client = TavoClient(api_version="v1")  # Shows deprecation warning
```

## 🧪 Testing Strategy

### Cross-Language Testing

```bash
# Run all SDK tests
yarn run test:all

# Run integration tests against staging API
yarn run test:integration

# Run performance tests
yarn run test:performance
```

### Test Structure

```text
__tests__/
├── unit/           # Unit tests for each SDK
├── integration/    # API integration tests
├── compatibility/  # Cross-version compatibility tests
└── examples/       # Example validation tests
```

### Mock Server

For testing without hitting production APIs:

```bash
# Start mock server
yarn run mock:start

# Run tests against mock
TEST_ENV=mock yarn run test
```

## 📦 Release Process

### Automated Releases

```bash
# Release all SDKs
yarn run release

# Release specific SDK
yarn run release:python

# Release with specific version
yarn run release -- --version 1.2.3
```

### Release Checklist

- [ ] All tests passing
- [ ] API compatibility verified
- [ ] Documentation updated
- [ ] Examples tested
- [ ] Changelog generated
- [ ] Version tags created

### Package Registries

- **Python**: PyPI (`pip install tavo-sdk`)
- **JavaScript**: npm (`yarn add @tavoai/sdk`)
- **Java**: Maven Central (`groupId: net.tavoai`)
- **Go**: Go Modules (`github.com/tavoai/tavo-go-sdk`)

## 🔄 CI/CD Pipelines

### GitHub Actions Workflows

- **Test**: Run tests on all PRs
- **Build**: Build all SDKs on main branch
- **Release**: Automated releases on version tags
- **Integration**: Test against staging API

### Quality Gates

```yaml
# Required checks before merge
- Unit test coverage > 80%
- Integration tests passing
- Linting passing
- Type checking passing
- API compatibility verified
```

## 🤝 Contributing

### Development Workflow

1. **Create Feature Branch**

   ```bash
   git checkout -b feature/add-new-endpoint
   ```

2. **Update API Spec** (if needed)

   ```bash
   # Update OpenAPI spec
   curl https://api.tavoai.net/api/v1/openapi.json > specs/v1.json
   ```

3. **Regenerate SDKs**

   ```bash
   yarn run codegen
   ```

4. **Implement Changes**
   - Update SDK-specific code
   - Add tests
   - Update documentation

5. **Test Changes**

   ```bash
   yarn run test:affected  # Test only changed packages
   ```

6. **Create Pull Request**
   - Detailed description
   - Breaking changes clearly marked
   - Migration guide if needed

### Code Standards

#### Python

- Black formatting
- isort imports
- mypy type checking
- pytest testing

#### JavaScript/TypeScript

- ESLint
- Prettier
- Jest testing
- TypeScript strict mode

#### Java

- Google Java Style Guide
- Spotless formatting
- JUnit testing
- Maven build

#### Go

- `gofmt` formatting
- `go vet` checking
- Go testing framework
- Go modules

### Commit Convention

```text
feat(python): add async scan methods
fix(js): resolve authentication timeout
docs: update installation guide
refactor(java): simplify HTTP client
test(go): add integration tests
```

## 📚 SDK Documentation

### API Reference

Auto-generated from OpenAPI spec:

- [Python SDK Docs](https://docs.tavoai.net/python/)
- [JavaScript SDK Docs](https://docs.tavoai.net/javascript/)
- [Java SDK Docs](https://docs.tavoai.net/java/)
- [Go SDK Docs](https://docs.tavoai.net/go/)

### Usage Examples

```python
# Basic usage
from tavo import TavoClient

client = TavoClient(api_key="your-api-key")

# Create a scan
scan = client.scans.create(
    repository_url="https://github.com/user/repo",
    scan_type="security"
)

# Get results
results = client.scans.get_results(scan.id)

# List vulnerabilities
for vuln in results.vulnerabilities:
    print(f"{vuln.severity}: {vuln.title}")
```

### Migration Guides

- [Migrating from v1 to v2](docs/migration-v1-to-v2.md)
- [Breaking Changes](docs/breaking-changes.md)

## 🔒 Security

### API Key Management

```python
# Environment variable (recommended)
export TAVO_API_KEY="your-api-key"
client = TavoClient()

# Explicit key
client = TavoClient(api_key="your-api-key")

# Key rotation
client.update_api_key("new-api-key")
```

### Data Protection

- No sensitive data logging
- Secure credential handling
- TLS 1.3+ required
- Regular security audits

## 📊 Monitoring & Analytics

### SDK Analytics

```python
# Enable usage tracking (opt-in)
client = TavoClient(telemetry=True)

# Custom telemetry
client.on('request', (event) => {
    console.log(`API call: ${event.method} ${event.url}`);
});
```

### Error Tracking

- Automatic error reporting (opt-in)
- SDK version and environment info
- Anonymized usage statistics

## 🚨 Support & Issues

### Issue Reporting

- **Bug Reports**: Use language-specific labels
- **Feature Requests**: Check roadmap first
- **Security Issues**: <security@tavoai.net>

### Support Channels

- **Documentation**: <https://docs.tavoai.net>
- **Community Forum**: <https://community.tavoai.net>
- **Enterprise Support**: <support@tavoai.net>

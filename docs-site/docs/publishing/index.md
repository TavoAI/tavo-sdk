# Automated Publishing Pipelines

This document describes the comprehensive automated publishing pipelines for the Tavo AI SDK ecosystem.

## 🚀 Overview

The Tavo AI SDK ecosystem includes automated pipelines for:

- **Multi-language SDK publishing** to all major package registries
- **Continuous deployment** with automated dependency updates
- **Security scanning** and vulnerability detection
- **Cross-language integration testing**
- **Automated documentation** generation and deployment

## 📦 Publishing Pipelines

### Supported Package Registries

| Language | Registry | Workflow |
|----------|----------|----------|
| Python | PyPI | `publish-python.yml` |
| JavaScript/TypeScript | npm | `publish-javascript.yml` |
| Java | Maven Central | `publish-java.yml` |
| Go | Go Modules (pkg.go.dev) | `publish-go.yml` |
| .NET | NuGet | `publish-dotnet.yml` |
| Rust | Crates.io | `publish-rust.yml` |

### Release Process

#### Automated Releases

1. **Trigger**: Push to `main` branch or manual workflow dispatch
2. **Version Calculation**: Automatic semantic versioning based on commit history
3. **Build & Test**: All SDKs tested across multiple environments
4. **Publish**: Parallel publishing to all configured registries
5. **Documentation**: Automatic documentation updates
6. **Notifications**: Success/failure notifications

#### Manual Releases

```bash
# Trigger a patch release
gh workflow run release.yml -f release_type=patch

# Trigger a minor release
gh workflow run release.yml -f release_type=minor

# Trigger a major release
gh workflow run release.yml -f release_type=major

# Release specific packages only
gh workflow run release.yml -f release_type=patch -f packages="python,javascript"
```

### Required Secrets

Set these secrets in your GitHub repository settings:

#### PyPI

- `PYPI_API_TOKEN`: PyPI API token
- `TEST_PYPI_API_TOKEN`: TestPyPI API token (optional)

#### npm

- `NPM_TOKEN`: npm authentication token

#### Maven Central

- `MAVEN_USERNAME`: Sonatype OSSRH username
- `MAVEN_PASSWORD`: Sonatype OSSRH password
- `MAVEN_GPG_PASSPHRASE`: GPG key passphrase
- `GPG_PRIVATE_KEY`: Base64-encoded GPG private key

#### NuGet

- `NUGET_API_KEY`: NuGet API key

#### Crates.io

- `CRATES_IO_TOKEN`: Crates.io API token

## 🔄 Continuous Deployment

### Automated Dependency Updates

- **Trigger**: Daily at 2 AM UTC or manual
- **Process**:
  1. Check for outdated dependencies across all SDKs
  2. Update dependencies if available
  3. Run full test suite
  4. Create pull request with updates

### Security Scanning

- **Trigger**: On every push/PR, weekly schedule
- **Tools**:
  - Trivy for container scanning
  - Safety (Python)
  - npm audit (JavaScript)
  - OWASP Dependency Check (Java)
  - cargo audit (Rust)
  - CodeQL for static analysis

## 🧪 Integration Testing

### Cross-Language Compatibility

- **Trigger**: On pushes to main/develop, daily schedule
- **Tests**:
  - API compatibility across all SDKs
  - Data consistency validation
  - Performance benchmarking
  - Memory usage analysis

### Test Infrastructure

- Redis for caching tests
- PostgreSQL/MySQL for database tests
- Mock API server for integration tests
- Docker Compose for service orchestration

## 📚 Documentation Automation

### Automated Documentation

- **Trigger**: On pushes to main
- **Process**:
  1. Generate API documentation for all SDKs
  2. Build Docusaurus documentation site
  3. Validate code examples
  4. Deploy to GitHub Pages

### Documentation Tools

- **Docusaurus**: Main documentation site
- **Sphinx**: Python API docs
- **TypeDoc**: JavaScript API docs
- **Javadoc**: Java API docs
- **GoDoc**: Go API docs
- **DocFX**: .NET API docs
- **RustDoc**: Rust API docs

## 🔧 Configuration Files

### Package Configuration

Each SDK requires specific configuration files:

#### Python (`packages/python/`)

- `pyproject.toml`: Package metadata and dependencies
- `setup.py`: Legacy setup script
- `requirements.txt`: Runtime dependencies

#### JavaScript (`packages/javascript/`)

- `package.json`: Package metadata and scripts
- `tsconfig.json`: TypeScript configuration

#### Java (`packages/java/`)

- `pom.xml`: Maven configuration
- `settings.xml`: Maven settings (for publishing)

#### Go (`packages/go/`)

- `go.mod`: Module definition
- `go.sum`: Dependency checksums

#### .NET (`packages/dotnet/`)

- `TavoAI.csproj`: Project file
- `Directory.Build.props`: Common properties

#### Rust (`packages/rust/`)

- `Cargo.toml`: Package metadata
- `Cargo.lock`: Dependency lock file

## 🚨 Monitoring and Alerts

### Failure Notifications

- Slack/Discord webhooks for build failures
- Email notifications for security issues
- GitHub issues for critical problems

### Health Checks

- Daily dependency health checks
- Weekly security vulnerability scans
- Monthly performance regression tests

## 📊 Metrics and Reporting

### Publishing Metrics

- Publication success rates
- Download statistics from registries
- User adoption metrics

### Quality Metrics

- Test coverage reports
- Code quality scores
- Security vulnerability counts

### Performance Metrics

- Build times
- Test execution times
- Package sizes

## 🔒 Security Considerations

### Secret Management

- All secrets stored in GitHub Secrets
- No secrets in code or configuration files
- Regular rotation of API tokens

### Access Controls

- Branch protection rules
- Required reviews for releases
- Restricted access to publishing workflows

## 🐛 Troubleshooting

### Common Issues

#### Publishing Failures

1. **Authentication errors**: Check API tokens are valid
2. **Version conflicts**: Ensure version numbers are unique
3. **Build failures**: Check build logs for compilation errors

#### Test Failures

1. **Integration test timeouts**: Check service availability
2. **Dependency conflicts**: Review dependency updates
3. **Environment issues**: Verify runner configurations

### Debug Mode

Enable debug logging:

```bash
# For GitHub Actions
echo "ACTIONS_RUNNER_DEBUG=true" >> $GITHUB_ENV
echo "ACTIONS_STEP_DEBUG=true" >> $GITHUB_ENV
```

## 📝 Maintenance

### Regular Tasks

- **Monthly**: Review and update dependencies
- **Weekly**: Check security scan results
- **Daily**: Monitor CI/CD pipeline status

### Version Management

- Semantic versioning (MAJOR.MINOR.PATCH)
- Pre-release versions for testing
- Automatic version calculation based on commits

## 🎯 Best Practices

### Release Management

1. Use semantic versioning
2. Test thoroughly before releases
3. Document breaking changes
4. Communicate release schedules

### Code Quality

1. Maintain high test coverage
2. Regular security audits
3. Performance monitoring
4. Code review requirements

### Documentation

1. Keep examples up-to-date
2. Validate code snippets
3. Update API documentation
4. User-friendly error messages

---

## 🚀 Quick Start

1. **Set up secrets** in GitHub repository settings
2. **Configure packages** with proper metadata
3. **Test locally** before pushing to main
4. **Trigger release** via GitHub Actions or manual dispatch

For detailed setup instructions, see the individual SDK documentation.

---
sidebar_position: 1
---

# Tavo CLI

The Tavo CLI is a comprehensive security scanning tool that combines **OpenGrep** pattern-based analysis with **OPA (Open Policy Agent)** policy evaluation for advanced LLM security assessments.

## Installation

### Prerequisites

- Python 3.8+
- Git
- pipenv (recommended) or pip

### Automated Setup

```bash
# Clone the repository
git clone https://github.com/TavoAI/tavo-cli.git
cd tavo-cli

# Run the automated build script
./build.sh
```

The build script will:

- Set up Python virtual environment
- Install all dependencies
- Build OpenGrep from source
- Configure the CLI for use

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Build OpenGrep (requires Go)
cd opengrep
go build -o opengrep ./cmd/opengrep

# Install the CLI
pip install -e .
```

## Authentication

The CLI requires authentication to access Tavo AI services:

```bash
# Set your API key
export TAVO_API_KEY="your-api-key-here"

# Or configure via config file
tavo config set api_key "your-api-key-here"
```

## Quick Start

### Basic Code Scanning

```bash
# Scan a single file
tavo scan file.py

# Scan a directory
tavo scan ./src

# Scan with specific language
tavo scan --language python ./my_app

# Generate SARIF report
tavo scan --format sarif --output results.sarif ./src
```

### LLM Security Analysis

```bash
# Scan for LLM-specific vulnerabilities
tavo scan --rules llm-security ./ai_app

# Check for prompt injection patterns
tavo scan --rules prompt-injection ./chatbot

# Analyze AI model configurations
tavo scan --rules model-security ./models
```

## Usage

### Command Reference

#### `tavo scan`

Scan code for security vulnerabilities:

```bash
tavo scan [OPTIONS] PATH

Options:
  --language TEXT          Programming language (auto-detected if not specified)
  --rules TEXT             Rule categories to apply (comma-separated)
  --format TEXT            Output format: json, sarif, text [default: text]
  --output FILE            Output file path
  --severity TEXT          Minimum severity level: info, low, medium, high, critical
  --exclude TEXT           Patterns to exclude (comma-separated)
  --include TEXT           Patterns to include (comma-separated)
  --config FILE            Custom configuration file
  --api-enhanced           Enable AI-enhanced analysis
  --batch-size INTEGER     Batch size for API calls [default: 10]
  --timeout INTEGER        Scan timeout in seconds [default: 300]
  --verbose                Enable verbose output
  --quiet                  Suppress non-error output
```

#### `tavo config`

Manage CLI configuration:

```bash
tavo config [COMMAND] [OPTIONS]

Commands:
  get KEY          Get configuration value
  set KEY VALUE    Set configuration value
  list             List all configuration values
  reset            Reset to default configuration
```

#### `tavo rules`

Manage security rules:

```bash
tavo rules [COMMAND] [OPTIONS]

Commands:
  list             List available rules
  update           Update rules from Tavo AI
  validate FILE    Validate custom rule file
  import FILE      Import custom rules
  export FILE      Export current rules
```

#### `tavo report`

Generate and manage reports:

```bash
tavo report [COMMAND] [OPTIONS]

Commands:
  generate SCAN_ID    Generate detailed report from scan
  compare SCAN1 SCAN2 Compare two scan results
  trend PATH          Show vulnerability trends over time
  export FORMAT       Export report in specified format
```

### Configuration

Create a `.tavo.yaml` file in your project root:

```yaml
# Tavo CLI Configuration
api:
  key: "${TAVO_API_KEY}"
  base_url: "https://api.tavo.ai"
  timeout: 30

scanning:
  default_language: "python"
  exclude_patterns:
    - "**/test/**"
    - "**/tests/**"
    - "**/*.test.*"
    - "**/*.spec.*"
  include_patterns:
    - "**/*.py"
    - "**/*.js"
    - "**/*.ts"
    - "**/*.java"
    - "**/*.go"

rules:
  categories:
    - "security"
    - "llm-security"
    - "performance"
  custom_rules_path: "./custom-rules"

output:
  format: "sarif"
  severity_threshold: "medium"
  show_progress: true
  verbose: false
```

## Architecture

### Hybrid Scanning Engine

The CLI uses a hybrid approach combining multiple analysis techniques:

1. **Static Analysis (OpenGrep)**: Fast pattern matching for known vulnerabilities
2. **Policy Evaluation (OPA)**: Declarative policy-based security checks
3. **AI Enhancement**: Optional AI-powered analysis for complex scenarios

### Rule System

Rules are categorized and can be sourced from:

- **Bundled Rules**: Built-in security rules for common vulnerabilities
- **API Rules**: Dynamically fetched from Tavo AI service
- **Custom Rules**: User-defined rules in YAML/Rego format

### Output Formats

- **Text**: Human-readable console output
- **JSON**: Structured data for integration
- **SARIF**: Standard security report format for CI/CD tools

## Advanced Usage

### Custom Rules

Create custom security rules:

```yaml
# custom-rules/security.yaml
rules:
  - id: "custom-sql-injection"
    name: "Custom SQL Injection Detection"
    description: "Detect potential SQL injection in custom ORM"
    severity: "high"
    category: "security"
    language: "python"
    pattern: |
      execute\(".*" \+ .*\+ ".*"\)
    message: "Potential SQL injection via string concatenation"
    remediation: "Use parameterized queries or prepared statements"

  - id: "llm-prompt-leakage"
    name: "LLM Prompt Leakage"
    description: "Detect accidental exposure of system prompts"
    severity: "critical"
    category: "llm-security"
    language: "javascript"
    pattern: |
      console\.log\(.*prompt.*\)
    message: "System prompt may be leaked to console"
    remediation: "Remove debug logging of prompts in production"
```

### CI/CD Integration

#### GitHub Actions

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install Tavo CLI
      run: |
        git clone https://github.com/TavoAI/tavo-cli.git
        cd tavo-cli
        ./build.sh

    - name: Run Security Scan
      env:
        TAVO_API_KEY: ${{ secrets.TAVO_API_KEY }}
      run: |
        export PATH="$PWD/tavo-cli:$PATH"
        tavo scan --format sarif --output results.sarif ./src

    - name: Upload SARIF Report
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: results.sarif
```

#### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - security

security_scan:
  stage: security
  image: python:3.9
  before_script:
    - git clone https://github.com/TavoAI/tavo-cli.git
    - cd tavo-cli && ./build.sh
    - export PATH="$PWD:$PATH"
  script:
    - cd ..
    - tavo scan --format sarif --output gl-results.sarif .
  artifacts:
    reports:
      sast: gl-results.sarif
  only:
    - merge_requests
    - main
```

### IDE Integration

The CLI can be integrated with various IDEs:

#### VS Code Tasks

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Tavo Security Scan",
      "type": "shell",
      "command": "tavo",
      "args": ["scan", "--format", "json", "./src"],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
```

## Troubleshooting

### Common Issues

#### OpenGrep Build Failures

If OpenGrep fails to build:

```bash
# Ensure Go is installed
go version

# Clean and rebuild
cd opengrep
rm -rf opengrep
go mod tidy
go build -o opengrep ./cmd/opengrep
```

#### API Connection Issues

```bash
# Test API connectivity
curl -H "Authorization: Bearer $TAVO_API_KEY" https://api.tavo.ai/health

# Check configuration
tavo config list
```

#### Memory Issues

For large codebases:

```bash
# Increase batch size
tavo scan --batch-size 5 ./large-codebase

# Use streaming for very large files
tavo scan --stream ./very-large-file.py
```

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Testing

```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=tavo_cli --cov-report=html tests/
```

### Building Releases

```bash
# Create distribution packages
python setup.py sdist bdist_wheel

# Build OpenGrep
cd opengrep && go build -ldflags="-s -w" -o ../bin/opengrep ./cmd/opengrep

# Test the build
./build.sh
```

This CLI provides comprehensive security scanning capabilities with a focus on AI and LLM applications, offering both local analysis and cloud-enhanced features for advanced security assessment.

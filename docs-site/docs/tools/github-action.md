---
sidebar_position: 3
---

# GitHub Action

The Tavo AI GitHub Action enables automated security scanning in your CI/CD pipelines, providing comprehensive vulnerability detection and AI-enhanced analysis for every pull request and push.

## Quick Start

### Basic Setup

Add this to your `.github/workflows/security.yml`:

```yaml
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

    - name: Tavo AI Security Scan
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
```

### With SARIF Upload

```yaml
name: Security Scan with SARIF

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest
    permissions:
      security-events: write

    steps:
    - uses: actions/checkout@v3

    - name: Run Tavo Security Scan
      uses: TavoAI/tavo-action@v1
      id: tavo-scan
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        format: sarif
        output: results.sarif

    - name: Upload SARIF results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: results.sarif
      if: always()
```

## Inputs

### Required Inputs

| Input | Description | Example |
|-------|-------------|---------|
| `api-key` | Tavo AI API key for authentication | `${{ secrets.TAVO_API_KEY }}` |

### Optional Inputs

| Input | Description | Default | Example |
|-------|-------------|---------|---------|
| `path` | Path to scan | `.` | `./src` |
| `format` | Output format | `text` | `sarif`, `json` |
| `output` | Output file path | | `results.sarif` |
| `language` | Programming language | auto | `python`, `javascript` |
| `rules` | Rule categories (comma-separated) | `security,llm-security` | `security,performance` |
| `severity` | Minimum severity level | `info` | `medium`, `high` |
| `exclude` | Patterns to exclude | | `**/test/**,**/node_modules/**` |
| `include` | Patterns to include | | `**/*.py,**/*.js` |
| `config` | Custom config file | | `.tavo.yaml` |
| `batch-size` | API batch size | `10` | `5` |
| `timeout` | Scan timeout (seconds) | `300` | `600` |
| `fail-on` | Fail on severity level | | `high`, `critical` |
| `baseline` | Baseline file for comparison | | `baseline.json` |
| `upload-results` | Upload results to Tavo AI | `false` | `true` |
| `comment-pr` | Comment on pull requests | `false` | `true` |
| `github-token` | GitHub token for PR comments | `${{ github.token }}` | |

## Outputs

| Output | Description |
|--------|-------------|
| `results-file` | Path to the results file |
| `issue-count` | Total number of issues found |
| `high-severity-count` | Number of high severity issues |
| `critical-severity-count` | Number of critical severity issues |
| `scan-duration` | Time taken for the scan (seconds) |
| `exit-code` | Exit code (0 for success, 1 for failures) |

## Advanced Usage

### Multi-Language Projects

```yaml
name: Multi-Language Security Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Scan Python Code
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        path: ./backend
        language: python
        output: python-results.sarif

    - name: Scan JavaScript Code
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        path: ./frontend
        language: javascript
        output: js-results.sarif

    - name: Upload Results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: python-results.sarif
      if: always()

    - name: Upload JS Results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: js-results.sarif
      if: always()
```

### LLM-Specific Scanning

```yaml
name: AI Security Scan

on: [push, pull_request]

jobs:
  ai-security:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: LLM Security Analysis
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        rules: llm-security,prompt-injection,model-security
        format: sarif
        output: ai-security.sarif
        comment-pr: true

    - name: Upload AI Security Results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: ai-security.sarif
      if: always()
```

### Custom Rules and Configuration

```yaml
name: Custom Rules Scan

on: [push, pull_request]

jobs:
  custom-scan:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Custom Rules
      run: |
        mkdir -p .tavo/rules
        cat > .tavo/rules/custom.yaml << EOF
        rules:
          - id: "company-secret-pattern"
            name: "Company Secret Pattern"
            pattern: "company_secret_[a-zA-Z0-9]+"
            message: "Detected company secret pattern"
            severity: "high"
        EOF

    - name: Run Scan with Custom Rules
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        config: .tavo/config.yaml
        output: custom-scan.sarif

    - name: Upload Results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: custom-scan.sarif
      if: always()
```

### Pull Request Integration

```yaml
name: PR Security Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  security-review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0

    - name: Security Scan
      uses: TavoAI/tavo-action@v1
      id: security-scan
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        format: json
        output: pr-scan.json
        comment-pr: true
        github-token: ${{ secrets.GITHUB_TOKEN }}
        fail-on: high

    - name: Comment PR with Results
      if: always()
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const results = JSON.parse(fs.readFileSync('pr-scan.json', 'utf8'));

          const comment = `## 🔒 Security Scan Results

          **Issues Found:** ${results.summary.total}
          **High Severity:** ${results.summary.high}
          **Critical:** ${results.summary.critical}

          ${results.summary.total > 0 ? '⚠️ Please review the security findings above.' : '✅ No security issues detected.'}`;

          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });
```

### Baseline Comparisons

```yaml
name: Baseline Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  baseline-scan:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Create/Update Baseline
      if: github.ref == 'refs/heads/main'
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        output: baseline.json
        format: json

    - name: Upload Baseline
      if: github.ref == 'refs/heads/main'
      uses: actions/upload-artifact@v3
      with:
        name: security-baseline
        path: baseline.json

    - name: Compare with Baseline
      if: github.event_name == 'pull_request'
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        baseline: baseline.json
        output: comparison.json
        format: json
```

## Configuration Files

### `.tavo.yaml` Configuration

```yaml
# Tavo Action Configuration
version: "1.0"

scanning:
  default_language: "python"
  exclude_patterns:
    - "**/test/**"
    - "**/tests/**"
    - "**/*.test.*"
    - "**/*.spec.*"
    - "**/node_modules/**"
    - "**/venv/**"
    - "**/__pycache__/**"
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
  custom_rules_path: "./.tavo/rules"

output:
  format: "sarif"
  severity_threshold: "medium"
  show_progress: true

ai:
  enabled: true
  model: "gpt-4"
  temperature: 0.1
  max_tokens: 1000

github:
  comment_pr: true
  fail_on_high: true
  upload_sarif: true
```

### Custom Rules

```yaml
# .tavo/rules/custom-rules.yaml
rules:
  - id: "api-key-pattern"
    name: "API Key Pattern Detection"
    description: "Detects potential API key patterns"
    severity: "high"
    category: "security"
    pattern: |
      (api_key|apikey|API_KEY)\s*[:=]\s*['"][a-zA-Z0-9]{20,}['"]
    message: "Potential API key exposure"
    remediation: "Use environment variables or secure credential storage"

  - id: "llm-system-prompt-leak"
    name: "System Prompt Leakage"
    description: "Detects accidental exposure of LLM system prompts"
    severity: "critical"
    category: "llm-security"
    pattern: |
      (system_prompt|SYSTEM_PROMPT).*[:=].*You are an AI
    message: "System prompt may be exposed"
    remediation: "Do not hardcode system prompts in source code"
```

## Integration Examples

### With Other Security Tools

#### CodeQL Integration

```yaml
name: Comprehensive Security Analysis

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: javascript

    - name: Tavo Security Scan
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        format: sarif
        output: tavo-results.sarif

    - name: Autobuild
      uses: github/codeql-action/autobuild@v2

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2

    - name: Upload Tavo Results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: tavo-results.sarif
      if: always()
```

#### Dependency Scanning

```yaml
name: Dependency Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  depscan:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Safety Check
      run: safety check

    - name: Tavo Code Security Scan
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        rules: security,dependencies
        output: security-scan.sarif

    - name: Upload Security Results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: security-scan.sarif
      if: always()
```

### Container Security

```yaml
name: Container Security Scan

on: [push, pull_request]

jobs:
  container-security:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Build Docker Image
      run: docker build -t myapp .

    - name: Scan Container
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'image'
        scan-ref: 'myapp'

    - name: Tavo Source Code Scan
      uses: TavoAI/tavo-action@v1
      with:
        api-key: ${{ secrets.TAVO_API_KEY }}
        path: .
        exclude: "**/node_modules/**"
        output: source-scan.sarif

    - name: Upload Source Results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: source-scan.sarif
      if: always()
```

## Troubleshooting

### Common Issues

#### Authentication Failures

```yaml
# Ensure API key is set in repository secrets
# Go to: Settings → Secrets and variables → Actions
# Add: TAVO_API_KEY = your-api-key-here

- name: Debug Auth
  run: |
    echo "API Key length: ${#TAVO_API_KEY}"
    # Don't echo the actual key for security
```

#### Scan Timeouts

```yaml
- name: Long Running Scan
  uses: TavoAI/tavo-action@v1
  with:
    api-key: ${{ secrets.TAVO_API_KEY }}
    timeout: 1200  # 20 minutes
    batch-size: 5  # Smaller batches for large codebases
```

#### Large Repository Issues

```yaml
- name: Scan Large Repo
  uses: TavoAI/tavo-action@v1
  with:
    api-key: ${{ secrets.TAVO_API_KEY }}
    path: ./src  # Limit scan scope
    exclude: "**/test/**,**/docs/**,**/examples/**"
    batch-size: 3
```

### Debug Mode

Enable debug output:

```yaml
- name: Debug Scan
  uses: TavoAI/tavo-action@v1
  with:
    api-key: ${{ secrets.TAVO_API_KEY }}
  env:
    DEBUG: tavo:*
    VERBOSE: 1
```

### Exit Codes

- `0`: Success, no issues found or issues below threshold
- `1`: Issues found at or above fail threshold
- `2`: Configuration error
- `3`: Authentication error
- `4`: Network/timeout error
- `5`: Internal error

## Best Practices

### Security

- Store API keys in GitHub Secrets
- Use minimal required permissions
- Regularly rotate API keys
- Monitor for exposed credentials

### Performance

- Use specific paths instead of scanning entire repository
- Exclude unnecessary directories (tests, docs, etc.)
- Use appropriate batch sizes
- Cache dependencies when possible

### Integration

- Combine with other security tools
- Use SARIF for unified reporting
- Set up notifications for critical findings
- Establish baseline scans for regression detection

### Compliance

- Configure appropriate severity thresholds
- Set up regular scanning schedules
- Maintain audit trails of security scans
- Document security policies and procedures

This GitHub Action provides comprehensive security scanning capabilities with seamless CI/CD integration, supporting multiple languages, custom rules, and various output formats for complete security coverage in your development pipeline.

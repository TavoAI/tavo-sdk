# Tavo Scanner

The Tavo Scanner is a high-performance, local security scanning engine that provides comprehensive vulnerability detection for codebases. Built with modern scanning technologies, it offers both CLI and SDK integration options.

## Overview

The Tavo Scanner combines multiple scanning engines:

- **OpenGrep**: Pattern-based security rule matching
- **OPA (Open Policy Agent)**: Policy-based security analysis
- **Custom Rules Engine**: AI-enhanced vulnerability detection

## Installation

### Pre-built Binaries

Download the latest scanner binary for your platform:

```bash
# Linux
curl -L https://github.com/tavoai/tavo-scanner/releases/latest/download/tavo-scanner-linux -o tavo-scanner
chmod +x tavo-scanner

# macOS
curl -L https://github.com/tavoai/tavo-scanner/releases/latest/download/tavo-scanner-macos -o tavo-scanner
chmod +x tavo-scanner

# Windows
curl -L https://github.com/tavoai/tavo-scanner/releases/latest/download/tavo-scanner-windows.exe -o tavo-scanner.exe
```

### From Source

```bash
git clone https://github.com/tavoai/tavo-scanner
cd tavo-scanner
npm install
npm run build
```

## Quick Start

### CLI Usage

```bash
# Scan a directory
tavo-scanner /path/to/codebase

# Scan with specific bundle
tavo-scanner /path/to/codebase --bundle llm-security

# Output results to file
tavo-scanner /path/to/codebase --output results.json --format json

# Scan with custom rules
tavo-scanner /path/to/codebase --rules /path/to/custom-rules.yaml
```

### SDK Integration

#### JavaScript/TypeScript

```typescript
import { SecurityScanner, RuleManager } from '@tavoai/scanner';

const ruleManager = new RuleManager();
const scanner = new SecurityScanner(ruleManager);

// Scan a codebase
const result = await scanner.scanCodebase('./src', 'llm-security');

console.log(`Scan completed: ${result.passed ? 'PASSED' : 'FAILED'}`);
console.log(`Found ${result.vulnerabilities.length} vulnerabilities`);
```

#### Python

```python
from tavo.scanner import SecurityScanner, RuleManager

rule_manager = RuleManager()
scanner = SecurityScanner(rule_manager)

# Scan a codebase
result = await scanner.scan_codebase('./src', bundle_name='llm-security')

print(f"Scan completed: {'PASSED' if result.passed else 'FAILED'}")
print(f"Found {len(result.vulnerabilities)} vulnerabilities")
```

## Rule Bundles

### Available Bundles

- **`llm-security`**: OWASP LLM Top 10 vulnerabilities
- **`ai-ethics`**: AI ethics and bias detection
- **`compliance`**: Regulatory compliance rules
- **`infrastructure`**: Cloud and infrastructure security
- **`application`**: Web and API security

### Custom Rule Bundles

Create custom rule bundles for organization-specific requirements:

```yaml
# custom-rules.yaml
rules:
  - id: custom-sql-injection
    pattern: |
      SELECT .* FROM .* WHERE .* = ['"]\$\{.*\}['"]
    message: "Potential SQL injection vulnerability"
    severity: HIGH
    category: injection
    cwe: CWE-89

  - id: custom-api-key-exposure
    pattern: |
      (api_key|apikey|API_KEY).*['" ]*[=:]['" ]*[a-zA-Z0-9]{20,}['"]
    message: "Potential API key exposure"
    severity: CRITICAL
    category: secrets
    cwe: CWE-200
```

## Configuration

### Configuration File

Create a `.tavo-scanner.yaml` file in your project root:

```yaml
scanner:
  # Scan configuration
  include_patterns:
    - "*.py"
    - "*.js"
    - "*.ts"
    - "*.java"
    - "*.go"

  exclude_patterns:
    - "node_modules/**"
    - "venv/**"
    - "__pycache__/**"
    - "*.test.*"
    - "*.spec.*"

  # Rule configuration
  bundles:
    - llm-security
    - application

  # Output configuration
  output_format: json
  output_file: scan-results.json

  # Performance settings
  max_file_size: 10485760  # 10MB
  timeout: 300  # 5 minutes
```

### Environment Variables

```bash
# Scanner configuration
TAVO_SCANNER_CONFIG=/path/to/config.yaml
TAVO_SCANNER_CACHE_DIR=/tmp/tavo-cache

# Rule management
TAVO_RULES_CACHE_TTL=3600
TAVO_RULES_REPO=https://github.com/tavoai/tavo-rules

# Performance
TAVO_SCANNER_MAX_WORKERS=4
TAVO_SCANNER_TIMEOUT=300
```

## CLI Reference

### Commands

```bash
tavo-scanner [options] <path>

Scan a codebase for security vulnerabilities

Positionals:
  path  Path to scan (file or directory)                    [string] [required]

Options:
      --help         Show help                                           [boolean]
      --version      Show version number                                 [boolean]
  -b, --bundle       Rule bundle to use            [string] [default: "llm-security"]
  -r, --rules        Custom rules file                    [string]
  -o, --output       Output file                           [string]
  -f, --format       Output format (json, sarif, html)    [string] [default: "json"]
  -v, --verbose      Verbose output                       [boolean]
      --no-color     Disable colored output               [boolean]
      --config       Configuration file                   [string]
      --cache-dir    Cache directory                      [string]
      --max-workers  Maximum worker threads               [number] [default: 4]
      --timeout      Scan timeout in seconds              [number] [default: 300]
```

### Examples

```bash
# Basic scan
tavo-scanner ./src

# Scan with multiple bundles
tavo-scanner ./src --bundle llm-security --bundle application

# Scan specific file types
tavo-scanner ./src --include "*.py" --include "*.js"

# Generate SARIF report for CI/CD
tavo-scanner ./src --format sarif --output security-results.sarif

# Custom rules scan
tavo-scanner ./src --rules custom-security-rules.yaml

# Verbose output with timing
tavo-scanner ./src --verbose --format json
```

## Advanced SDK Integration

### Advanced JavaScript Usage

```typescript
import { SecurityScanner, RuleManager, OpenGrepEngine, OPAEngine } from '@tavoai/scanner';

// Initialize components
const ruleManager = new RuleManager({
  cacheDir: '/tmp/tavo-rules'
});

const opengrep = new OpenGrepEngine('/usr/local/bin/opengrep');
const opa = new OPAEngine('/usr/local/bin/opa');

const scanner = new SecurityScanner(ruleManager);

// Load custom rules
await ruleManager.downloadBundle('llm-security');

// Scan with custom options
const result = await scanner.scanCodebase('./src', 'llm-security', false);

// Process results
result.vulnerabilities.forEach(vuln => {
  console.log(`${vuln.severity}: ${vuln.message}`);
  console.log(`Location: ${vuln.file}:${vuln.line}`);
  console.log(`Rule: ${vuln.ruleId}`);
});
```

### Advanced Python Usage

```python
import asyncio
from tavo.scanner import SecurityScanner, RuleManager, OpenGrepEngine, OPAEngine

async def main():
    # Initialize components
    rule_manager = RuleManager(cache_dir='/tmp/tavo-rules')
    opengrep = OpenGrepEngine('/usr/local/bin/opengrep')
    opa = OPAEngine('/usr/local/bin/opa')

    scanner = SecurityScanner(rule_manager)

    # Load rules
    await rule_manager.download_bundle('llm-security')

    # Scan codebase
    result = await scanner.scan_codebase('./src', bundle_name='llm-security', use_binary=False)

    # Process results
    for vuln in result.vulnerabilities:
        print(f"{vuln.severity}: {vuln.message}")
        print(f"Location: {vuln.file}:{vuln.line}")
        print(f"Rule: {vuln.rule_id}")

asyncio.run(main())
```

## Output Formats

### JSON Output

```json
{
  "scan_id": "scan-12345",
  "timestamp": "2024-01-15T10:30:00Z",
  "target": "./src",
  "passed": false,
  "scan_time": 2.34,
  "vulnerabilities": [
    {
      "id": "llm01-001",
      "rule_id": "prompt-injection-basic",
      "severity": "HIGH",
      "category": "injection",
      "cwe": "CWE-77",
      "message": "Potential prompt injection vulnerability",
      "file": "src/chat.py",
      "line": 45,
      "column": 12,
      "code": "query = f\"SELECT * FROM users WHERE id = '{user_input}'\"",
      "confidence": 0.85,
      "evidence": {
        "pattern": "string interpolation with user input",
        "context": "SQL query construction"
      }
    }
  ],
  "summary": {
    "total_files": 15,
    "scanned_files": 12,
    "total_vulnerabilities": 3,
    "by_severity": {
      "CRITICAL": 0,
      "HIGH": 2,
      "MEDIUM": 1,
      "LOW": 0,
      "INFO": 0
    },
    "by_category": {
      "injection": 2,
      "secrets": 1
    }
  }
}
```

### SARIF Output

Standard SARIF format for integration with CI/CD tools and IDEs.

### HTML Output

Rich HTML reports with syntax highlighting and interactive features.

## Rule Development

### Rule Format

```yaml
rules:
  - id: rule-identifier
    name: Human readable name
    description: Detailed description
    pattern: |
      Regular expression pattern or
      multi-line pattern for matching
    message: Error message when rule matches
    severity: CRITICAL|HIGH|MEDIUM|LOW|INFO
    category: injection|secrets|auth|crypto|etc
    cwe: CWE-XXX
    confidence: 0.0-1.0
    languages: [python, javascript, java]
    tags: [tag1, tag2]
    metadata:
      owasp: LLM01
      source: custom
```

### Testing Rules

```bash
# Test rule against sample code
tavo-scanner test-rule --rule rule.yaml --code sample.py

# Validate rule syntax
tavo-scanner validate-rule --rule rule.yaml

# Benchmark rule performance
tavo-scanner benchmark-rule --rule rule.yaml --corpus /path/to/test-code
```

## Performance Optimization

### Large Codebases

```bash
# Use multiple workers
tavo-scanner ./large-codebase --max-workers 8

# Limit file size
tavo-scanner ./codebase --max-file-size 5242880  # 5MB

# Use binary scanner for better performance
tavo-scanner ./codebase --use-binary
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Security Scan
  uses: tavoai/scan-action@v1
  with:
    path: ./src
    bundle: llm-security
    format: sarif
    output: security-results.sarif

# GitLab CI
tavo_scan:
  script:
    - tavo-scanner ./src --format json --output results.json
  artifacts:
    reports:
      sast: results.json
```

## Troubleshooting

### Common Issues

#### Scanner not found

```bash
# Check if scanner is installed
which tavo-scanner

# Install scanner
npm install -g @tavoai/scanner
```

#### Rules not loading

```bash
# Clear rule cache
rm -rf ~/.tavoai/rules

# Re-download rules
tavo-scanner --clear-cache ./src
```

#### Memory issues

```bash
# Reduce worker count
tavo-scanner ./src --max-workers 2

# Increase Node.js memory limit
NODE_OPTIONS="--max-old-space-size=4096" tavo-scanner ./src
```

#### False positives

```bash
# Use rule exclusions
tavo-scanner ./src --exclude-rule RULE-001 --exclude-rule RULE-002

# Create .tavoignore file
echo "RULE-001" > .tavoignore
echo "RULE-002" >> .tavoignore
```

## Contributing

### Development Setup

```bash
git clone https://github.com/tavoai/tavo-scanner
cd tavo-scanner
npm install
npm run build
npm test
```

### Adding New Rules

1. Create rule definition in YAML
2. Add test cases
3. Update documentation
4. Submit pull request

### Engine Development

The scanner supports pluggable engines:

```typescript
class CustomEngine implements ScanEngine {
  async scan(filePath: string, rules: Rule[]): Promise<Vulnerability[]> {
    // Custom scanning logic
    return vulnerabilities;
  }
}

// Register custom engine
scanner.registerEngine('custom', new CustomEngine());
```

```

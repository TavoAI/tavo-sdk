---
sidebar_position: 2
---

# VSCode Plugin

The Tavo AI VSCode extension brings powerful security scanning capabilities directly into your development environment, providing real-time analysis and AI-enhanced security insights.

## Installation

### From VSCode Marketplace

1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "Tavo AI"
4. Click "Install"

### From Source

```bash
# Clone the repository
git clone https://github.com/TavoAI/vscode-plugin.git
cd vscode-plugin

# Install dependencies
npm install

# Build the extension
npm run build

# Package for installation
npm run package
```

Then install the generated `.vsix` file:

- Open VSCode
- Go to Extensions
- Click the "..." menu
- Select "Install from VSIX..."
- Choose the generated `.vsix` file

## Features

### Real-time Security Scanning

- **Automatic Analysis**: Scans files as you type and save
- **Inline Diagnostics**: Security issues appear directly in your code
- **Quick Fixes**: Apply suggested remediations with a single click

### AI-Powered Analysis

- **Context-Aware Scanning**: Understands code context and dependencies
- **LLM Security Focus**: Specialized detection for AI/ML applications
- **Intelligent Suggestions**: AI-generated remediation recommendations

### Multi-Language Support

- **Python**: Full support for Python applications
- **JavaScript/TypeScript**: Node.js and web applications
- **Java**: Enterprise applications
- **Go**: Cloud-native applications
- **C/C++**: System-level security
- **And more**: 20+ supported languages

## Configuration

### Extension Settings

Access settings through VSCode's settings UI or edit `settings.json`:

```json
{
  "tavo.scanOnSave": true,
  "tavo.scanOnType": false,
  "tavo.apiKey": "your-api-key-here",
  "tavo.severityThreshold": "medium",
  "tavo.includePatterns": [
    "**/*.py",
    "**/*.js",
    "**/*.ts",
    "**/*.java"
  ],
  "tavo.excludePatterns": [
    "**/node_modules/**",
    "**/venv/**",
    "**/__pycache__/**",
    "**/*.test.*",
    "**/*.spec.*"
  ],
  "tavo.enableAiEnhancement": true,
  "tavo.customRulesPath": "./.tavo/rules",
  "tavo.outputFormat": "vscode",
  "tavo.showProgress": true,
  "tavo.batchSize": 10
}
```

### Workspace Configuration

Create a `.tavo.json` file in your workspace root:

```json
{
  "version": "1.0",
  "scanning": {
    "enabled": true,
    "languages": ["python", "javascript"],
    "rules": {
      "categories": ["security", "llm-security", "performance"],
      "custom": "./rules/custom.yaml"
    },
    "exclusions": {
      "patterns": ["**/test/**", "**/tests/**"],
      "files": [".env", "secrets.json"]
    }
  },
  "reporting": {
    "format": "sarif",
    "output": "./reports/security-scan.sarif",
    "severity": "medium"
  },
  "ai": {
    "enabled": true,
    "model": "gpt-4",
    "temperature": 0.1,
    "maxTokens": 1000
  }
}
```

## Usage

### Manual Scanning

#### Scan Current File

- **Command Palette**: `Ctrl+Shift+P` → "Tavo: Scan Current File"
- **Context Menu**: Right-click in editor → "Scan with Tavo"
- **Keyboard Shortcut**: `Ctrl+Shift+S` (configurable)

#### Scan Workspace

- **Command Palette**: "Tavo: Scan Workspace"
- **Status Bar**: Click the Tavo icon in the status bar

#### Scan Selection

- Select code in editor
- **Context Menu**: "Scan Selection with Tavo"
- **Command Palette**: "Tavo: Scan Selection"

### Automatic Scanning

The extension automatically scans:

- **On Save**: When you save a file (configurable)
- **On Type**: As you type (configurable, may impact performance)
- **On Open**: When you open a file (configurable)

### Viewing Results

#### Problems Panel

Security issues appear in VSCode's Problems panel with:

- File and line number
- Severity level (Error, Warning, Info)
- Description and remediation suggestions

#### Tavo Panel

Access the dedicated Tavo panel:

- **View Menu**: View → Open View Pane → Tavo
- **Command Palette**: "Tavo: Show Results Panel"

The panel shows:

- **Summary**: Total issues by severity
- **File List**: Issues grouped by file
- **Rule Details**: Information about triggered rules
- **Timeline**: Historical scan results

### Quick Fixes

For many security issues, the extension provides quick fixes:

1. Click the lightbulb icon next to the issue
2. Select "Apply Tavo Fix"
3. Review the suggested change
4. Accept or modify the fix

## Commands

### Core Commands

| Command | Description | Keybinding |
|---------|-------------|------------|
| `tavo.scanCurrentFile` | Scan the currently active file | `ctrl+shift+s` |
| `tavo.scanWorkspace` | Scan the entire workspace | `ctrl+shift+alt+s` |
| `tavo.scanSelection` | Scan selected code | `ctrl+shift+e` |
| `tavo.showResults` | Show scan results panel | |
| `tavo.clearResults` | Clear all scan results | |
| `tavo.configure` | Open settings | |

### Advanced Commands

| Command | Description |
|---------|-------------|
| `tavo.createCustomRule` | Create a new custom rule |
| `tavo.importRules` | Import rules from file |
| `tavo.exportResults` | Export scan results |
| `tavo.showRuleDetails` | Show detailed rule information |
| `tavo.runQuickFix` | Apply quick fix for current issue |

## Custom Rules

### Creating Custom Rules

1. **Command Palette**: "Tavo: Create Custom Rule"
2. Choose rule type (pattern-based or AI-enhanced)
3. Define the rule properties
4. Test against sample code
5. Save to workspace

### Rule Format

```yaml
# custom-rules.yaml
rules:
  - id: "custom-api-key-exposure"
    name: "API Key Exposure"
    description: "Detects potential API key exposure in logs"
    severity: "high"
    category: "security"
    language: "python"
    pattern: |
      (log|print).*API_KEY.*
    message: "Potential API key exposure in logging statement"
    remediation: "Remove sensitive data from logs or use secure logging"
    tags: ["logging", "credentials"]

  - id: "llm-prompt-injection"
    name: "LLM Prompt Injection"
    description: "Detects potential prompt injection vulnerabilities"
    severity: "critical"
    category: "llm-security"
    language: "javascript"
    aiEnhanced: true
    pattern: |
      prompt.*\+.*userInput
    message: "Potential prompt injection vulnerability"
    remediation: "Validate and sanitize user input before including in prompts"
    tags: ["llm", "injection", "ai-security"]
```

### Rule Testing

Test custom rules before deployment:

```javascript
// Test code for prompt injection rule
const userInput = "Tell me about " + req.body.input;
const prompt = `You are a helpful assistant. ${userInput}`;
```

## Integration

### CI/CD Integration

Export scan results for CI/CD pipelines:

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Tavo Scan
        uses: TavoAI/tavo-action@v1
        with:
          api-key: ${{ secrets.TAVO_API_KEY }}
          format: sarif
          output: results.sarif

      - name: Upload Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Add to .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tavo-scan
        name: Tavo Security Scan
        entry: tavo scan --format json
        language: system
        files: \.(py|js|ts|java|go)$
        pass_filenames: false
```

### GitHub Code Scanning

The extension integrates with GitHub Code Scanning:

1. Export results in SARIF format
2. Upload to GitHub Security tab
3. View results in security dashboard
4. Set up code scanning alerts

## Performance

### Optimization Tips

#### Large Workspaces

```json
{
  "tavo.scanOnType": false,
  "tavo.scanOnSave": true,
  "tavo.batchSize": 5,
  "tavo.includePatterns": ["src/**", "lib/**"],
  "tavo.excludePatterns": ["**/node_modules/**", "**/dist/**"]
}
```

#### High-Frequency Editing

```json
{
  "tavo.debounceDelay": 1000,
  "tavo.scanOnType": false,
  "tavo.enableIncrementalScan": true
}
```

### Resource Usage

- **Memory**: ~50-200MB depending on workspace size
- **CPU**: Minimal impact during normal editing
- **Network**: API calls only when AI enhancement is enabled

## Troubleshooting

### Common Issues

#### Authentication Problems

```json
// Check API key in settings
{
  "tavo.apiKey": "your-valid-api-key"
}
```

#### Scanning Not Working

1. Check language support
2. Verify file patterns
3. Check exclusion rules
4. Review error logs in Output panel

#### Performance Issues

1. Disable real-time scanning
2. Increase debounce delay
3. Limit scan scope
4. Exclude large directories

### Debug Mode

Enable debug logging:

```json
{
  "tavo.debug": true
}
```

View logs in VSCode's Output panel under "Tavo Debug".

### Reset Extension

If issues persist:

1. Disable the extension
2. Reload VSCode window
3. Clear workspace state: `Ctrl+Shift+P` → "Developer: Reload Window"
4. Re-enable extension

## Development

### Contributing

1. Fork the repository
2. Install dependencies: `npm install`
3. Build: `npm run build`
4. Test: `npm test`
5. Debug: Press F5 to launch extension development host

### Architecture

The extension consists of:

- **Extension Host**: Main extension logic
- **Language Server**: Handles scanning and analysis
- **Webview**: Results display panel
- **Configuration**: Settings management

### Testing

```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e
```

### Building Releases

```bash
# Create package
npm run package

# Publish to marketplace
npm run publish
```

This extension provides seamless integration of Tavo AI's security scanning capabilities into the VSCode development workflow, offering both automated and manual scanning options with comprehensive customization and integration capabilities.

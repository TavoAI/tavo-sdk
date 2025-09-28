# Tavo Scanner

Standalone security scanner binary for Tavo AI. Provides local security scanning capabilities using OpenGrep and OPA engines.

## Status

✅ **Completed:**
- Scanner package structure with CLI interface
- Automatic engine downloading (OpenGrep and OPA)
- Cross-platform binary bundling
- Rule bundle loading from tavo-rules repository
- JSON/text output formats
- Integration with vscode-plugin, tavo-cli, and SDKs
- **Rule format conversion: All 32 LLM security rules converted to OpenGrep pattern format**

🚀 **Ready for Production:**
- Full OWASP LLM Top 10 coverage
- Functional vulnerability detection
- Cross-platform scanning capabilities

## Installation

### Binary Release (Recommended)

Download the latest binary release for your platform from the [releases page](https://github.com/TavoAI/tavo-api/releases).

The binary is self-contained and includes all dependencies and engines - no Python installation required.

**Automated Releases**: Binaries are automatically built and released for Linux, Windows, and macOS via GitHub Actions.

```bash
# Make executable and run
chmod +x tavo-scanner
./tavo-scanner --help
```

### From Source

```bash
git clone https://github.com/TavoAI/tavo-api.git
cd tavo-api/packages/scanner

# Download engines
chmod +x download_engines.sh
./download_engines.sh

# Install
pip install -e .
```

### As Binary

Download the appropriate binary for your platform from the [releases page](https://github.com/TavoAI/tavo-api/releases).

The binary is self-contained and includes all dependencies and engines - no Python installation required.

## Usage

### Command Line

```bash
# Scan a file
python tavo_scanner.py /path/to/file.py

# Scan a directory
python tavo_scanner.py /path/to/project

# Use specific rule bundle
python tavo_scanner.py --bundle llm-security /path/to/code

# Get text output
python tavo_scanner.py --format text /path/to/code

# Verbose output
python tavo_scanner.py --verbose /path/to/code
```

### JSON Output

```json
{
  "vulnerabilities": [],
    {
      "check_id": "rule-id",
      "message": "Security issue description",
      "path": "/path/to/file",
      "start": {"line": 10, "col": 5},
      "end": {"line": 10, "col": 15}
    }
  ],
  "passed": false,
  "scan_time": 1.23,
  "bundle": "llm-security",
  "rules_used": 42
}
```

### Exit Codes

- `0`: Scan passed (no vulnerabilities found)
- `1`: Scan failed (vulnerabilities found or error)

## Next Steps

1. **Rule Format Conversion**: Convert existing regex-based rules in `tavo-rules/bundles/` to OpenGrep pattern format
2. **Binary Packaging**: Create PyInstaller builds for cross-platform distribution
3. **CI/CD Pipeline**: Set up automated binary builds and releases
4. **Rule Testing**: Add comprehensive test cases for rule validation
5. **Performance Optimization**: Optimize scanning performance for large codebases

## Integration

### VS Code Plugin

```typescript
import { spawn } from 'child_process';

const scanner = spawn('tavo-scanner', ['--format', 'json', path]);
scanner.stdout.on('data', (data) => {
  const results = JSON.parse(data.toString());
  // Process results
});
```

### Tavo CLI

```bash
# The CLI can use the scanner binary directly
tavo-scanner /path/to/code > results.json
```

### SDK Integration

```python
import subprocess
import json

def scan_with_binary(path: str) -> dict:
    result = subprocess.run(
        ['tavo-scanner', '--format', 'json', path],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

## Building Binaries

### Automated Build (Recommended)

Use the provided build script for consistent builds:

```bash
# From the tavo-api root directory
./build_binary.sh
```

This creates a standalone executable in `packages/scanner/dist/tavo-scanner`.

### Manual Build with PyInstaller

```bash
pip install pyinstaller PyYAML

# Build with all dependencies included
pyinstaller --onefile --hidden-import yaml --add-data "engines:engines" --name tavo-scanner tavo_scanner.py

# The binary will be in dist/tavo-scanner
```

### Cross-Platform Builds

Use CI/CD to build for multiple platforms:

```yaml
# GitHub Actions example
- name: Build Linux binary
  run: |
    pyinstaller --onefile tavo_scanner.py
    mv dist/tavo_scanner dist/tavo-scanner-linux-amd64

- name: Build macOS binary
  run: |
    pyinstaller --onefile tavo_scanner.py
    mv dist/tavo_scanner dist/tavo-scanner-darwin-amd64

- name: Build Windows binary
  run: |
    pyinstaller --onefile tavo_scanner.py
    mv dist/tavo_scanner.exe dist/tavo-scanner-windows-amd64.exe
```

## Engines

The scanner bundles OpenGrep and OPA binaries for local scanning:

- **OpenGrep**: Fast semantic code pattern matching
- **OPA**: Policy evaluation for complex security rules

Engines are automatically downloaded during installation or can be manually downloaded:

```bash
./download_engines.sh
```

## Rule Bundles

The scanner uses rule bundles from the `tavo-rules` repository. By default, it looks for bundles in:

1. Local workspace (`./tavo-rules/bundles/`)
2. Cached downloads (`~/.tavoai/rules/`)

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
flake8 tavo_scanner.py

# Format code
black tavo_scanner.py
```

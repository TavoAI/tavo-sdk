# Scanner Binary Release Process

This document explains how to create releases of the Tavo Scanner binaries for multiple platforms.

## Automated Release Workflow

The `scanner-binary-release.yml` workflow automatically builds binaries for:

- Linux (x64)
- Windows (x64)
- macOS (x64)
- macOS (ARM64)

## Triggering Releases

### Manual Release (Recommended)

1. Go to GitHub Actions → Scanner Binary Release
2. Click "Run workflow"
3. Enter version tag (e.g., `v1.0.0`)
4. Optionally mark as prerelease
5. Click "Run workflow"

### Automatic Release

The workflow also triggers automatically when:
- Code is pushed to `main` branch affecting scanner files
- Commit message contains "release"

## Release Artifacts

Each release contains:
- `tavo-scanner-linux-x64.tar.gz`
- `tavo-scanner-macos-x64.tar.gz`
- `tavo-scanner-macos-arm64.tar.gz`
- `tavo-scanner-windows-x64.zip`

## Local Testing

Before releasing, test the build script locally:

```bash
# Build for current platform
./build_binary.sh

# Test the binary
cd packages/scanner/dist
./tavo-scanner --help
```

## CI/CD Requirements

The workflow requires:
- GitHub Actions with appropriate permissions
- `GITHUB_TOKEN` secret (automatically provided)
- Cross-platform runners (ubuntu-latest, windows-latest, macos-latest)

## Troubleshooting

### Build Failures
- Check that `download_engines.sh` works on all platforms
- Verify PyInstaller can access all dependencies
- Ensure the scanner imports are correct

### Release Failures
- Check GitHub token permissions
- Verify version tag format
- Ensure artifacts are properly uploaded

### Binary Issues
- Test binaries on target platforms
- Verify engines are properly bundled
- Check file permissions (especially on Unix systems)

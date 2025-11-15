# Tavo SDK GitHub Secrets Setup

This guide explains how to set up GitHub repository secrets and variables for Tavo SDK publishing workflows.

## Overview

The Tavo SDK repository needs various API keys, tokens, and credentials for automated publishing to different package registries (NuGet, npm, Maven Central, Crates.io, etc.).

This system provides:
- **Templated secrets management** - Define secrets in a template file
- **Automated GitHub setup** - Script loads secrets into GitHub repository
- **Security** - Secrets stored securely, templates are placeholders only

## Quick Start

### 1. Prerequisites

```bash
# Install GitHub CLI
# https://cli.github.com/

# Authenticate
gh auth login

# Ensure you're in the tavo-sdk repository
cd /path/to/tavo-sdk
```

### 2. Prepare Secrets Template

```bash
# Copy the template
cp templates/github-secrets-template.env .secrets/github-secrets-filled.env

# Edit with your actual values
nano .secrets/github-secrets-filled.env
```

### 3. Load Secrets to GitHub

```bash
# Run the setup script
./scripts/setup-github-secrets.sh .secrets/github-secrets-filled.env
```

## Available Secrets

### Publishing Credentials

| Secret | Purpose | Where to Get |
|--------|---------|--------------|
| `NUGET_API_KEY` | NuGet package publishing | https://www.nuget.org/account/apikeys |
| `GPG_PRIVATE_KEY` | Package signing | `gpg --export-secret-keys --armor KEY_ID` |
| `GPG_PASSPHRASE` | GPG key passphrase | Your GPG key passphrase |
| `MAVEN_USERNAME` | Maven Central username | Sonatype JIRA username |
| `MAVEN_PASSWORD` | Maven Central password | Sonatype JIRA password |
| `CRATES_IO_TOKEN` | Rust crate publishing | https://crates.io/me (API tokens) |
| `GO_SDK_ACCESS_TOKEN` | Go module publishing | GitHub PAT with repo/packages permissions |
| `VSCE_PAT` | VS Code extension publishing | https://marketplace.visualstudio.com/manage/publishers/ |
| `OVSX_PAT` | Open VSX extension publishing | https://open-vsx.org/user-settings/tokens |

### Notifications

| Secret | Purpose | Where to Get |
|--------|---------|--------------|
| `SLACK_WEBHOOK_URL` | Build notifications | https://api.slack.com/apps → Incoming Webhooks |

### Repository Variables

These become GitHub repository variables (not secrets):

| Variable | Purpose | Default |
|----------|---------|---------|
| `NODE_VERSION` | Node.js version for builds | `20` |
| `PYTHON_VERSION` | Python version for builds | `3.11` |
| `GO_VERSION` | Go version for builds | `1.21` |
| `DOTNET_VERSION` | .NET version for builds | `8.0.x` |
| `JAVA_VERSION` | Java version for builds | `17` |
| `RUST_VERSION` | Rust version for builds | `stable` |
| `*_REGISTRY` | Package registry URLs | Various |

## Template File Format

```bash
# Secrets (become GitHub repository secrets)
NUGET_API_KEY=USER_REPLACE_WITH_YOUR_NUGET_API_KEY
SLACK_WEBHOOK_URL=USER_REPLACE_WITH_YOUR_SLACK_WEBHOOK_URL

# Variables (become GitHub repository variables)
NODE_VERSION=20
PYTHON_VERSION=3.11
```

## Security Notes

- **Never commit actual secrets** - Only commit placeholder templates
- **Use strong, unique credentials** for each service
- **Rotate credentials regularly** - Especially API keys and tokens
- **Limit permissions** - Use the minimum required permissions for each token
- **Monitor usage** - Check API dashboards for unusual activity

## Troubleshooting

### GitHub CLI Authentication

```bash
# Check auth status
gh auth status

# Re-authenticate if needed
gh auth login
```

### Permission Errors

Ensure your GitHub account has:
- **Repository admin access** for the tavo-sdk repository
- **Permission to manage secrets and variables**

### Template File Not Found

```bash
# Create templates directory if missing
mkdir -p templates

# Copy template from infra if needed
cp ../infra/templates/github-secrets-template.env templates/
```

## Updating Secrets

To update existing secrets:

1. Edit your filled template: `nano .secrets/github-secrets-filled.env`
2. Update the values
3. Re-run the setup script: `./scripts/setup-github-secrets.sh .secrets/github-secrets-filled.env`

The script will update existing secrets and add new ones.

## Workflow Integration

Once secrets are set up, workflows can access them using:

```yaml
# In GitHub Actions workflow
- name: Publish to NuGet
  run: dotnet nuget push *.nupkg --api-key ${{ secrets.NUGET_API_KEY }}

- name: Use Node version
  uses: actions/setup-node@v4
  with:
    node-version: ${{ vars.NODE_VERSION }}
```

## Support

For questions about specific publishing credentials, check the documentation for each package registry:

- [NuGet API Keys](https://docs.microsoft.com/en-us/nuget/quickstart/create-and-publish-a-package#publish-to-nugetorg)
- [Maven Central](https://central.sonatype.org/publish/publish-guide/)
- [Crates.io Tokens](https://doc.rust-lang.org/cargo/reference/publishing.html)
- [VS Code Extensions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)

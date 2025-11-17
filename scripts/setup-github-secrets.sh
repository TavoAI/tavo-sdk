#!/bin/bash
# GitHub Secrets Setup
# Loads secrets from template into GitHub repository
#
# Usage: ./setup-github-secrets.sh [secrets-file]
# Example: ./setup-github-secrets.sh templates/github-secrets-template.env

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default template file
TEMPLATE_FILE="${1:-templates/github-secrets-template.env}"

# Full path to template
if [[ "$TEMPLATE_FILE" == /* ]] || [[ "$TEMPLATE_FILE" == .*/* ]]; then
    TEMPLATE_PATH="$TEMPLATE_FILE"
else
    TEMPLATE_PATH="$REPO_ROOT/$TEMPLATE_FILE"
fi

echo "🚀 Setting up Website GitHub Secrets"
echo "===================================="
echo ""
echo "Template file: $TEMPLATE_PATH"
echo ""

# Check if template exists
if [ ! -f "$TEMPLATE_PATH" ]; then
    echo -e "${RED}❌ Template file not found: $TEMPLATE_PATH${NC}"
    exit 1
fi

# Check if GitHub CLI is available and authenticated
if ! command -v gh >/dev/null 2>&1; then
    echo -e "${RED}❌ GitHub CLI not found. Install with: https://cli.github.com/${NC}"
    exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
    echo -e "${RED}❌ Not authenticated with GitHub CLI. Run: gh auth login${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Processing secrets from template...${NC}"
echo ""

secrets_set=0
variables_set=0
errors=0

# Process each line in the template
while IFS='=' read -r key value; do
    # Skip comments and empty lines
    [[ "$key" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$key" ]] && continue

    # Remove inline comments
    value="${value%%#*}"

    # Trim whitespace
    key="${key#"${key%%[![:space:]]*}"}"
    key="${key%"${key##*[![:space:]]}"}"
    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"

    # Skip empty values
    [[ -z "$value" ]] && continue

    echo -n "Setting $key... "

    # Check if it looks like a placeholder (contains REPLACE_WITH)
    if [[ "$value" == *"REPLACE_WITH"* ]]; then
        echo -e "${YELLOW}⚠️  SKIPPED (placeholder value)${NC}"
        continue
    fi

    # Determine if this should be a secret or variable
    if [[ "$key" == *"_SECRET" ]] || [[ "$key" == *"_KEY" ]] || [[ "$key" == *"_TOKEN" ]] || [[ "$key" == *"_PASSWORD" ]] || [[ "$key" == *"_PASSPHRASE" ]] || [[ "$key" == *"_PAT" ]] || [[ "$key" == *"_USERNAME" ]] || [[ "$key" == *"_WEBHOOK_URL" ]]; then
        # This is a secret - use gh secret set
        if echo -n "$value" | gh secret set "$key" 2>/dev/null; then
            echo -e "${GREEN}✅ SECRET${NC}"
            ((secrets_set++))
        else
            echo -e "${RED}❌ SECRET FAILED${NC}"
            ((errors++))
        fi
    else
        # This is a variable - use gh variable set
        if gh variable set "$key" --body "$value" 2>/dev/null; then
            echo -e "${GREEN}✅ VARIABLE${NC}"
            ((variables_set++))
        else
            echo -e "${RED}❌ VARIABLE FAILED${NC}"
            ((errors++))
        fi
    fi

done < "$TEMPLATE_PATH"

echo ""
echo -e "${BLUE}📊 Summary:${NC}"
echo "  Secrets set: $secrets_set"
echo "  Variables set: $variables_set"
if [ $errors -gt 0 ]; then
    echo -e "  ${RED}Errors: $errors${NC}"
fi

echo ""
if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✅ All GitHub secrets and variables set successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  Some secrets/variables failed to set. Check above for details.${NC}"
fi

echo ""
echo -e "${BLUE}🔧 Manual Setup Required:${NC}"
echo "  1. Fill in placeholder values in: $TEMPLATE_PATH"
echo "  2. Re-run this script: ./scripts/setup-github-secrets.sh"
echo ""
echo -e "${BLUE}📝 Note:${NC}"
echo "  Secrets with 'REPLACE_WITH' in the value are skipped."
echo "  Update the template file with actual values before running."

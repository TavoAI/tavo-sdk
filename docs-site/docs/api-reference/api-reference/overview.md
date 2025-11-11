# API Reference

The Tavo AI API provides comprehensive security scanning and AI model analysis capabilities.

## Available Endpoints

This API reference covers 26 main endpoint categories:

- **Ai Analysis** - [ai_analysis](ai_analysis.md)
- **Ai Analysis Core** - [ai_analysis_core](ai_analysis_core.md)
- **Ai Bulk Operations** - [ai_bulk_operations](ai_bulk_operations.md)
- **Ai Performance Quality** - [ai_performance_quality](ai_performance_quality.md)
- **Ai Results Export** - [ai_results_export](ai_results_export.md)
- **Ai Risk Compliance** - [ai_risk_compliance](ai_risk_compliance.md)
- **Code Submission** - [code_submission](code_submission.md)
- **Device Auth** - [device_auth](device_auth.md)
- **Health** - [health](health.md)
- **Jobs** - [jobs](jobs.md)
- **Plugin Execution** - [plugin_execution](plugin_execution.md)
- **Plugin Marketplace** - [plugin_marketplace](plugin_marketplace.md)
- **Registry** - [registry](registry.md)
- **Repositories** - [repositories](repositories.md)
- **Repository Connections** - [repository_connections](repository_connections.md)
- **Repository Providers** - [repository_providers](repository_providers.md)
- **Repository Webhooks** - [repository_webhooks](repository_webhooks.md)
- **Rules** - [rules](rules.md)
- **Scan Bulk Operations** - [scan_bulk_operations](scan_bulk_operations.md)
- **Scan Management** - [scan_management](scan_management.md)
- **Scan Rules** - [scan_rules](scan_rules.md)
- **Scan Schedules** - [scan_schedules](scan_schedules.md)
- **Scan Tools** - [scan_tools](scan_tools.md)
- **Scanner Integration** - [scanner_integration](scanner_integration.md)


## Authentication

All API endpoints require authentication. The following methods are supported:

### API Key Authentication
```bash
Authorization: Bearer your-api-key
# or
X-API-Key: your-api-key
```

### JWT Token Authentication
```bash
Authorization: Bearer your-jwt-token
```

### Device Code Authentication
```bash
X-Device-Code: your-device-code
```

## Base URL

```
https://api.tavoai.net/api/v1
```

## Response Format

All responses are JSON formatted. Successful responses include:

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

Error responses include:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": { ... }
  }
}
```

## Rate Limiting

API requests are subject to rate limiting:

- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1000 requests/hour
- **Enterprise Tier**: Custom limits

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

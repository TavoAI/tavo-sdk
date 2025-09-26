---
sidebar_position: 3
---

# Authentication

Learn how to authenticate with the Tavo AI API using different methods.

## API Key Authentication

The primary authentication method is API key authentication. API keys are tied to your account and provide access to all Tavo AI services.

### Obtaining an API Key

1. Sign up for a Tavo AI account at [tavoai.org](https://tavoai.org)
2. Navigate to your dashboard
3. Go to Settings > API Keys
4. Generate a new API key
5. Store it securely (never commit to version control)

### Using API Keys

```python
# Python
from tavo import TavoClient

client = TavoClient(api_key="your-api-key-here")
```

```javascript
// JavaScript/TypeScript
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient({
  apiKey: 'your-api-key-here'
});
```

```java
// Java
import ai.tavo.TavoClient;
import ai.tavo.TavoConfig;

TavoConfig config = TavoConfig.builder()
    .apiKey("your-api-key-here")
    .build();

TavoClient client = new TavoClient(config);
```

```go
// Go
import "github.com/TavoAI/tavo-go-sdk/tavo"

config := tavo.NewConfig().WithAPIKey("your-api-key-here")
client := tavo.NewClient(config)
```

## JWT Token Authentication

For advanced integrations, JWT tokens provide more granular access control.

### Obtaining JWT Tokens

JWT tokens are typically obtained through the authentication endpoints:

```python
# Python - Login to get JWT token
auth_result = client.auth().login("username", "password")
jwt_token = auth_result["access_token"]

# Use JWT token for subsequent requests
config = TavoConfig(jwt_token=jwt_token)
authenticated_client = TavoClient(config)
```

```javascript
// JavaScript - Login to get JWT token
const authResult = await client.auth().login('username', 'password');
const jwtToken = authResult.access_token;

// Use JWT token for subsequent requests
const authenticatedClient = new TavoClient({
  jwtToken: jwtToken
});
```

```java
// Java - Login to get JWT token
Map<String, Object> authResult = client.auth().login("username", "password");
String jwtToken = (String) authResult.get("access_token");

// Use JWT token for subsequent requests
TavoConfig config = TavoConfig.builder()
    .jwtToken(jwtToken)
    .build();
TavoClient authenticatedClient = new TavoClient(config);
```

```go
// Go - Login to get JWT token
authResult, err := client.Auth().Login("username", "password")
if err != nil {
    log.Fatal(err)
}
jwtToken := authResult["access_token"].(string)

// Use JWT token for subsequent requests
config := tavo.NewConfig().WithJWTToken(jwtToken)
authenticatedClient := tavo.NewClient(config)
```

## Environment Variable Configuration

For security and convenience, use environment variables:

```bash
# Set API key
export TAVO_API_KEY="your-api-key-here"

# Optional: Set base URL for custom deployments
export TAVO_BASE_URL="https://your-custom-api.tavo.ai"
```

```python
# Python - Automatically uses environment variables
from tavo import TavoClient

client = TavoClient()  # Reads TAVO_API_KEY automatically
```

```javascript
// JavaScript - Automatically uses environment variables
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient();  // Reads process.env.TAVO_API_KEY
```

```java
// Java - Automatically uses environment variables
import ai.tavo.TavoClient;

TavoClient client = new TavoClient();  // Reads System.getenv("TAVO_API_KEY")
```

```go
// Go - Automatically uses environment variables
import "github.com/TavoAI/tavo-go-sdk/tavo"

config := tavo.NewConfig()  // Reads os.Getenv("TAVO_API_KEY")
client := tavo.NewClient(config)
```

## Security Best Practices

### API Key Security

- **Never commit API keys to version control**
- Use environment variables or secure key management systems
- Rotate API keys regularly
- Use different keys for different environments (dev/staging/prod)

### JWT Token Security

- JWT tokens have expiration times
- Implement token refresh logic for long-running applications
- Store tokens securely (not in local storage for web apps)
- Validate token expiration before making requests

### Environment-Specific Keys

```bash
# Development
export TAVO_API_KEY="dev-key-123"

# Staging
export TAVO_API_KEY="staging-key-456"

# Production
export TAVO_API_KEY="prod-key-789"
```

### Key Rotation

```python
# Python - Implement key rotation
import os
from tavo import TavoClient

def get_client():
    api_key = os.getenv('TAVO_API_KEY')
    if not api_key:
        raise ValueError("TAVO_API_KEY environment variable not set")
    return TavoClient(api_key=api_key)

client = get_client()
```

## Troubleshooting Authentication

### Common Issues

**401 Unauthorized**
- Check that your API key is correct and active
- Verify the key hasn't expired
- Ensure proper environment variable configuration

**403 Forbidden**
- Check that your account has the necessary permissions
- Verify you're using the correct API endpoints for your plan

**429 Too Many Requests**
- Implement proper rate limiting in your application
- Consider upgrading your plan for higher limits

### Testing Authentication

```python
# Python - Test authentication
try:
    health = client.health_check()
    print("Authentication successful!")
except Exception as e:
    print(f"Authentication failed: {e}")
```

```javascript
// JavaScript - Test authentication
try {
  const health = await client.healthCheck();
  console.log('Authentication successful!');
} catch (error) {
  console.error('Authentication failed:', error);
}
```

```java
// Java - Test authentication
try {
    Map<String, Object> health = client.healthCheck();
    System.out.println("Authentication successful!");
} catch (TavoException e) {
    System.err.println("Authentication failed: " + e.getMessage());
}
```

```go
// Go - Test authentication
health, err := client.HealthCheck()
if err != nil {
    log.Printf("Authentication failed: %v", err)
} else {
    fmt.Println("Authentication successful!")
}
```

# Scan Tools API

## Endpoints

### GET `/tools`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `active_only` | `boolean` |  | query |  |

**Response:**

Returns `List[ScanToolInfo]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/tools' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.tools.get_tools()
```

---

### GET `/tools/{tool_name}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `tool_name` | `string` | ✓ | query |  |

**Response:**

Returns `ScanToolInfo`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/tools/{tool_name}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.tools.get_tools(param='value')
```

---

### GET `/templates`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `tool` | `string` |  | query |  |
| `category` | `string` |  | query |  |
| `language` | `string` |  | query |  |
| `active_only` | `boolean` |  | query |  |

**Response:**

Returns `List[ScanTemplateInfo]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/templates' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.templates.get_templates()
```

---

### GET `/templates/{template_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `template_id` | `string` | ✓ | query |  |

**Response:**

Returns `ScanTemplateInfo`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/templates/{template_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.templates.get_templates(param='value')
```

---

### POST `/validate-configuration`



**Response:**

Returns `ScanConfigurationValidationResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/validate-configuration' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.validate-configuration.post_validate-configuration()
```

---

### GET `/repositories/{repository_id}/settings`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | query |  |

**Response:**

Returns `RepositoryScanSettings`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/repositories/{repository_id}/settings' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.repositories.get_repositories(param='value')
```

---

### PUT `/repositories/{repository_id}/settings`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | body |  |
| `settings` | `RepositoryScanSettings` | ✓ | body |  |

**Response:**

Returns `RepositoryScanSettings`

**Example:**

```bash
curl -X PUT 'https://api.tavoai.net/api/v1/repositories/{repository_id}/settings' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.repositories.put_repositories(param='value')
```

---

### POST `/validate-access`



**Response:**

Returns `RepositoryAccessValidationResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/validate-access' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.validate-access.post_validate-access()
```

---


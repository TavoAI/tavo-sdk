# Repository Webhooks API

## Endpoints

### POST `/github`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `x_hub_signature_256` | `string` |  | body |  |
| `x_github_event` | `string` |  | body |  |
| `x_github_delivery` | `string` |  | body |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/github' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.github.post_github()
```

---

### POST `/{repository_id}/setup`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | body |  |

**Response:**

Returns `WebhookSetupResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{repository_id}/setup' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{repository_id}.post_{repository_id}(param='value')
```

---

### GET `/{repository_id}/status`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | query |  |

**Response:**

Returns `WebhookStatusResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{repository_id}/status' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{repository_id}.get_{repository_id}(param='value')
```

---

### DELETE `/{repository_id}/webhook`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | body |  |

**Response:**

Returns `Dict[str, str]`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/{repository_id}/webhook' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{repository_id}.delete_{repository_id}(param='value')
```

---


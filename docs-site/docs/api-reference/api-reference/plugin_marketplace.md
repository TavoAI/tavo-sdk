# Plugin Marketplace API

## Endpoints

### GET `/marketplace`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_type` | `string` |  | query |  |
| `category` | `string` |  | query |  |
| `pricing_tier` | `string` |  | query |  |
| `search` | `string` |  | query |  |
| `is_official` | `boolean` |  | query |  |
| `is_vetted` | `boolean` |  | query |  |
| `min_rating` | `number` |  | query |  |
| `page` | `number` |  | query |  |
| `per_page` | `number` |  | query |  |
| `sort_by` | `string` |  | query |  |
| `sort_order` | `string` |  | query |  |

**Response:**

Returns `PluginListResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/marketplace' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.marketplace.get_marketplace()
```

---

### GET `/{plugin_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | query |  |

**Response:**

Returns `PluginResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{plugin_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.get_{plugin_id}(param='value')
```

---

### POST `/{plugin_id}/install`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | body |  |
| `organization_id` | `string` |  | body |  |

**Response:**

Returns `PluginInstallationResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{plugin_id}/install' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.post_{plugin_id}(param='value')
```

---

### GET `/{plugin_id}/download`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | query |  |
| `version` | `string` |  | query |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{plugin_id}/download' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.get_{plugin_id}(param='value')
```

---

### GET `/installed`



**Response:**

Returns `List[PluginInstallationResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/installed' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.installed.get_installed()
```

---

### PUT `/{plugin_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | body |  |
| `plugin_data` | `PluginUpdate` | ✓ | body |  |

**Response:**

Returns `PluginResponse`

**Example:**

```bash
curl -X PUT 'https://api.tavoai.net/api/v1/{plugin_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.put_{plugin_id}(param='value')
```

---

### DELETE `/{plugin_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/{plugin_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.delete_{plugin_id}(param='value')
```

---

### POST `/{plugin_id}/publish`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | body |  |

**Response:**

Returns `PluginResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{plugin_id}/publish' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.post_{plugin_id}(param='value')
```

---

### POST `/{plugin_id}/versions`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | body |  |
| `version_data` | `PluginVersionCreate` | ✓ | body |  |

**Response:**

Returns `PluginVersionResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{plugin_id}/versions' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.post_{plugin_id}(param='value')
```

---

### GET `/{plugin_id}/versions`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | query |  |

**Response:**

Returns `List[PluginVersionResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{plugin_id}/versions' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.get_{plugin_id}(param='value')
```

---

### GET `/{plugin_id}/reviews`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | query |  |
| `page` | `number` |  | query |  |
| `limit` | `number` |  | query |  |
| `min_rating` | `number` |  | query |  |
| `sort_by` | `string` |  | query |  |
| `sort_order` | `string` |  | query |  |

**Response:**

Returns `List[PluginReviewResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{plugin_id}/reviews' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.get_{plugin_id}(param='value')
```

---

### POST `/{plugin_id}/reviews`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | body |  |
| `review_data` | `PluginReviewCreate` | ✓ | body |  |

**Response:**

Returns `PluginReviewResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{plugin_id}/reviews' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.post_{plugin_id}(param='value')
```

---

### GET `/{plugin_id}/reviews/{review_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | query |  |
| `review_id` | `string` | ✓ | query |  |

**Response:**

Returns `PluginReviewResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{plugin_id}/reviews/{review_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.get_{plugin_id}(param='value')
```

---

### PUT `/{plugin_id}/reviews/{review_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | body |  |
| `review_id` | `string` | ✓ | body |  |
| `review_update` | `PluginReviewUpdate` | ✓ | body |  |

**Response:**

Returns `PluginReviewResponse`

**Example:**

```bash
curl -X PUT 'https://api.tavoai.net/api/v1/{plugin_id}/reviews/{review_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.put_{plugin_id}(param='value')
```

---

### DELETE `/{plugin_id}/reviews/{review_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | body |  |
| `review_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/{plugin_id}/reviews/{review_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.delete_{plugin_id}(param='value')
```

---

### POST `/{plugin_id}/reviews/{review_id}/helpful`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | body |  |
| `review_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{plugin_id}/reviews/{review_id}/helpful' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{plugin_id}.post_{plugin_id}(param='value')
```

---


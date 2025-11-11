# Repositories API

## Endpoints

### POST `/sync`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `background_tasks` | `BackgroundTasks` | ✓ | body |  |

**Response:**

Returns `List[RepositoryResponse]`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/sync' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.sync.post_sync()
```

---

### GET `/`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `connection_id` | `string` |  | query |  |
| `language` | `string` |  | query |  |
| `scan_enabled` | `boolean` |  | query |  |
| `search` | `string` |  | query |  |
| `page` | `number` |  | query |  |
| `per_page` | `number` |  | query |  |

**Response:**

Returns `RepositoryListResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client..get_()
```

---

### GET `/{repository_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | query |  |

**Response:**

Returns `RepositoryResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{repository_id}' \
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

### PUT `/{repository_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | body |  |
| `repository_update` | `RepositoryUpdate` | ✓ | body |  |

**Response:**

Returns `RepositoryResponse`

**Example:**

```bash
curl -X PUT 'https://api.tavoai.net/api/v1/{repository_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{repository_id}.put_{repository_id}(param='value')
```

---

### DELETE `/{repository_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/{repository_id}' \
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

### GET `/{repository_id}/scans`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | query |  |
| `limit` | `number` |  | query |  |

**Response:**

Returns `List[ScanInDB]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{repository_id}/scans' \
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

### POST `/{repository_id}/scan`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | body |  |
| `background_tasks` | `BackgroundTasks` | ✓ | body |  |

**Response:**

Returns `ScanInDB`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{repository_id}/scan' \
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

### GET `/{repository_id}/branches`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | query |  |

**Response:**

Returns `List[RepositoryBranchResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{repository_id}/branches' \
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

### POST `/{repository_id}/pause`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | body |  |

**Response:**

Returns `RepositoryResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{repository_id}/pause' \
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

### POST `/{repository_id}/resume`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | body |  |

**Response:**

Returns `RepositoryResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{repository_id}/resume' \
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

### GET `/{repository_id}/analytics`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | query |  |
| `timeframe` | `string` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{repository_id}/analytics' \
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

### GET `/{repository_id}/badge`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | query |  |
| `style` | `string` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{repository_id}/badge' \
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

### GET `/{repository_id}/activity`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | query |  |
| `limit` | `number` |  | query |  |

**Response:**

Returns `List[Dict[str, Any]]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{repository_id}/activity' \
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


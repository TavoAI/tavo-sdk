# Repository Connections API

## Endpoints

### POST `/`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `connection_in` | `RepositoryConnectionCreate` | ✓ | body |  |

**Response:**

Returns `RepositoryConnectionResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client..post_()
```

---

### GET `/`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `provider_id` | `string` |  | query |  |
| `connection_type` | `string` |  | query |  |
| `is_active` | `boolean` |  | query |  |

**Response:**

Returns `List[RepositoryConnectionResponse]`

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

### GET `/{connection_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `connection_id` | `string` | ✓ | query |  |

**Response:**

Returns `RepositoryConnectionResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{connection_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{connection_id}.get_{connection_id}(param='value')
```

---

### PUT `/{connection_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `connection_id` | `string` | ✓ | body |  |
| `connection_update` | `RepositoryConnectionUpdate` | ✓ | body |  |

**Response:**

Returns `RepositoryConnectionResponse`

**Example:**

```bash
curl -X PUT 'https://api.tavoai.net/api/v1/{connection_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{connection_id}.put_{connection_id}(param='value')
```

---

### DELETE `/{connection_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `connection_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/{connection_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{connection_id}.delete_{connection_id}(param='value')
```

---

### POST `/{connection_id}/validate`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `connection_id` | `string` | ✓ | body |  |

**Response:**

Returns `ConnectionValidationResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{connection_id}/validate' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{connection_id}.post_{connection_id}(param='value')
```

---

### POST `/{connection_id}/refresh`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `connection_id` | `string` | ✓ | body |  |

**Response:**

Returns `RepositoryConnectionResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{connection_id}/refresh' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{connection_id}.post_{connection_id}(param='value')
```

---


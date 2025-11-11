# Scan Management API

## Endpoints

### POST `/`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_in` | `ScanCreate` | ✓ | body |  |

**Response:**

Returns `dict`

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
| `skip` | `number` |  | query |  |
| `limit` | `number` |  | query |  |
| `status_filter` | `string` |  | query |  |
| `organization_id` | `string` |  | query |  |

**Response:**

Returns `List[ScanSchema]`

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

### GET `/{scan_id:uuid}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{scan_id:uuid}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{scan_id:uuid}.get_{scan_id:uuid}(param='value')
```

---

### GET `/{scan_id:uuid}/results`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | query |  |
| `severity_filter` | `string` |  | query |  |
| `rule_type_filter` | `string` |  | query |  |
| `limit` | `number` |  | query |  |

**Response:**

Returns `List[ScanResultSchema]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{scan_id:uuid}/results' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{scan_id:uuid}.get_{scan_id:uuid}(param='value')
```

---

### POST `/{scan_id:uuid}/cancel`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | body |  |

**Response:**

Returns `dict`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/{scan_id:uuid}/cancel' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{scan_id:uuid}.post_{scan_id:uuid}(param='value')
```

---


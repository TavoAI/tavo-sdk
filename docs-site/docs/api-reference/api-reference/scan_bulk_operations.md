# Scan Bulk Operations API

## Endpoints

### POST `/bulk/initiate`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_requests` | `ScanCreate[]` | ✓ | body |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/bulk/initiate' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.bulk.post_bulk()
```

---

### POST `/bulk/cancel`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_ids` | `string[]` | ✓ | body |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/bulk/cancel' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.bulk.post_bulk()
```

---

### DELETE `/bulk/delete`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_ids` | `string[]` | ✓ | body |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/bulk/delete' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.bulk.delete_bulk()
```

---

### GET `/bulk/status`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_ids` | `string[]` |  | query |  |
| `organization_id` | `string` |  | query |  |
| `status_filter` | `string` |  | query |  |
| `limit` | `number` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/bulk/status' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.bulk.get_bulk()
```

---


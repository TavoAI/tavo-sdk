# Ai Bulk Operations API

## Endpoints

### DELETE `/bulk/delete`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `analysis_ids` | `string[]` |  | body |  |

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

### PUT `/bulk/update-status`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `analysis_updates` | `Dict[str, Any][]` |  | body |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X PUT 'https://api.tavoai.net/api/v1/bulk/update-status' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.bulk.put_bulk()
```

---

### GET `/bulk/export`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `analysis_ids` | `string[]` |  | query |  |
| `export_format` | `string` |  | query |  |

**Response:**

Returns `Any`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/bulk/export' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.bulk.get_bulk()
```

---


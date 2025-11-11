# Ai Analysis Core API

## Endpoints

### GET `/analyses`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `skip` | `number` |  | query |  |
| `limit` | `number` |  | query |  |
| `scan_id` | `string` |  | query |  |
| `analysis_type` | `string` |  | query |  |
| `status` | `string` |  | query |  |
| `start_date` | `string` |  | query |  |
| `end_date` | `string` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/analyses' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.analyses.get_analyses()
```

---

### GET `/analyses/{analysis_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `analysis_id` | `string` | ✓ | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/analyses/{analysis_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.analyses.get_analyses(param='value')
```

---


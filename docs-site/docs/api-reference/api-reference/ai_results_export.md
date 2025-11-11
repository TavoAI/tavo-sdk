# Ai Results Export API

## Endpoints

### GET `/results`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `skip` | `number` |  | query |  |
| `limit` | `number` |  | query |  |
| `scan_id` | `string` |  | query |  |
| `analysis_type` | `string` |  | query |  |
| `severity` | `string` |  | query |  |
| `start_date` | `string` |  | query |  |
| `end_date` | `string` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/results' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.results.get_results()
```

---

### GET `/results/export`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `format` | `string` |  | query |  |
| `scan_id` | `string` |  | query |  |
| `analysis_type` | `string` |  | query |  |
| `start_date` | `string` |  | query |  |
| `end_date` | `string` |  | query |  |

**Response:**

Returns `Response`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/results/export' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.results.get_results()
```

---


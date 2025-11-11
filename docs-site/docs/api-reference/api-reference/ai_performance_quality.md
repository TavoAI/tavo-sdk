# Ai Performance Quality API

## Endpoints

### GET `/performance-metrics`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `start_date` | `string` |  | query |  |
| `end_date` | `string` |  | query |  |
| `analysis_type` | `string` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/performance-metrics' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.performance-metrics.get_performance-metrics()
```

---

### GET `/quality-review/{scan_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/quality-review/{scan_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.quality-review.get_quality-review(param='value')
```

---


# Jobs API

## Endpoints

### GET `/status/{job_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `job_id` | `string` | ✓ | query |  |

**Response:**

Returns `JobStatus`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/status/{job_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.status.get_status(param='value')
```

---

### GET `/dashboard`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `limit` | `number` |  | query |  |
| `authorization` | `string` |  | query |  |
| `x_api_key` | `string` |  | query |  |

**Response:**

Returns `JobSummary`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/dashboard' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.dashboard.get_dashboard()
```

---


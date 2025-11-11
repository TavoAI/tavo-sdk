# Ai Risk Compliance API

## Endpoints

### GET `/risk-scores`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `skip` | `number` |  | query |  |
| `limit` | `number` |  | query |  |
| `scan_id` | `string` |  | query |  |
| `min_score` | `number` |  | query |  |
| `max_score` | `number` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/risk-scores' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.risk-scores.get_risk-scores()
```

---

### GET `/compliance-reports`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `skip` | `number` |  | query |  |
| `limit` | `number` |  | query |  |
| `scan_id` | `string` |  | query |  |
| `framework` | `string` |  | query |  |
| `status` | `string` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/compliance-reports' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.compliance-reports.get_compliance-reports()
```

---

### GET `/predictive-analyses`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `skip` | `number` |  | query |  |
| `limit` | `number` |  | query |  |
| `scan_id` | `string` |  | query |  |
| `prediction_type` | `string` |  | query |  |
| `confidence_threshold` | `number` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/predictive-analyses' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.predictive-analyses.get_predictive-analyses()
```

---


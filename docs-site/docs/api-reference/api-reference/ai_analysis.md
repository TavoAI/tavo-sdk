# Ai Analysis API

## Endpoints

### POST `/analyze/{scan_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | body |  |
| `background_tasks` | `BackgroundTasks` | ✓ | body |  |

**Response:**

Returns `CodeFixResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/analyze/{scan_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.analyze.post_analyze(param='value')
```

---

### POST `/classify/{scan_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | body |  |
| `background_tasks` | `BackgroundTasks` | ✓ | body |  |

**Response:**

Returns `VulnerabilityClassificationResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/classify/{scan_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.classify.post_classify(param='value')
```

---

### POST `/risk-score/{scan_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | body |  |

**Response:**

Returns `RiskScoreResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/risk-score/{scan_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.risk-score.post_risk-score(param='value')
```

---

### POST `/compliance/{scan_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `number` | ✓ | body |  |
| `framework` | `string` |  | body |  |

**Response:**

Returns `ComplianceReportResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/compliance/{scan_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.compliance.post_compliance(param='value')
```

---

### POST `/predictive/{scan_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | body |  |

**Response:**

Returns `PredictiveAnalysisResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/predictive/{scan_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.predictive.post_predictive(param='value')
```

---

### GET `/fix-suggestions`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `search` | `string` |  | query |  |
| `status` | `string` |  | query |  |
| `severity` | `string` |  | query |  |
| `analysis_type` | `string` |  | query |  |
| `limit` | `number` |  | query |  |
| `offset` | `number` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/fix-suggestions' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.fix-suggestions.get_fix-suggestions()
```

---

### GET `/predictive`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `time_horizon` | `string` |  | query |  |
| `severity` | `string` |  | query |  |
| `prediction_type` | `string` |  | query |  |
| `analysis_type` | `string` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/predictive' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.predictive.get_predictive()
```

---

### GET `/compliance`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `framework` | `string` |  | query |  |
| `status` | `string` |  | query |  |
| `risk_level` | `string` |  | query |  |
| `category` | `string` |  | query |  |

**Response:**

Returns `Dict[str, Any]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/compliance' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.compliance.get_compliance()
```

---


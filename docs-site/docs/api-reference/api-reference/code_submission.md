# Code Submission API

## Endpoints

### POST `/submit/code`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `files` | `UploadFile[]` |  | body |  |
| `scan_config` | `Dict` |  | body |  |
| `repository_name` | `string` |  | body |  |
| `branch` | `string` |  | body |  |
| `commit_sha` | `string` |  | body |  |

**Response:**

Returns `dict`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/submit/code' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.submit.post_submit()
```

---

### POST `/submit/repository`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_url` | `string` |  | body |  |
| `snapshot_data` | `Dict` |  | body |  |
| `scan_config` | `Dict` |  | body |  |
| `branch` | `string` |  | body |  |
| `commit_sha` | `string` |  | body |  |

**Response:**

Returns `dict`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/submit/repository' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.submit.post_submit()
```

---

### POST `/submit/analysis`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `code_content` | `string` |  | body |  |
| `language` | `string` |  | body |  |
| `analysis_type` | `string` |  | body |  |
| `rules` | `string[]` |  | body |  |
| `plugins` | `string[]` |  | body |  |
| `context` | `Dict` |  | body |  |

**Response:**

Returns `dict`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/submit/analysis' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.submit.post_submit()
```

---

### GET `/scans/{scan_id}/status`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | query |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/scans/{scan_id}/status' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.scans.get_scans(param='value')
```

---

### GET `/scans/{scan_id}/results/summary`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scan_id` | `string` | ✓ | query |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/scans/{scan_id}/results/summary' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.scans.get_scans(param='value')
```

---


# Registry API

## Endpoints

### GET `/marketplace`



**Response:**

Returns `PaginatedResponse[ArtifactBundleList]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/marketplace' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.marketplace.get_marketplace()
```

---

### GET `/categories`



**Response:**

Returns `List[CategoryResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/categories' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.categories.get_categories()
```

---

### POST `/bundles`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle` | `ArtifactBundleCreate` | ✓ | body |  |

**Response:**

Returns `ArtifactBundleDetail`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/bundles' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.bundles.post_bundles()
```

---

### GET `/bundles/{bundle_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | query |  |

**Response:**

Returns `ArtifactBundleDetail`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/bundles/{bundle_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.get_bundles(param='value')
```

---

### PUT `/bundles/{bundle_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | body |  |
| `bundle_update` | `ArtifactBundleUpdate` | ✓ | body |  |

**Response:**

Returns `ArtifactBundleDetail`

**Example:**

```bash
curl -X PUT 'https://api.tavoai.net/api/v1/bundles/{bundle_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.put_bundles(param='value')
```

---

### DELETE `/bundles/{bundle_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/bundles/{bundle_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.delete_bundles(param='value')
```

---

### GET `/bundles/{bundle_id}/download`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | query |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/bundles/{bundle_id}/download' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.get_bundles(param='value')
```

---

### POST `/bundles/{bundle_id}/install`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | body |  |
| `installation` | `BundleInstallationCreate` | ✓ | body |  |

**Response:**

Returns `BundleInstallationResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/bundles/{bundle_id}/install' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.post_bundles(param='value')
```

---

### GET `/my-bundles`



**Response:**

Returns `List[BundleInstallationResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/my-bundles' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.my-bundles.get_my-bundles()
```

---

### POST `/execute/code-rule`



**Response:**

Returns `ArtifactExecutionResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/execute/code-rule' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.execute.post_execute()
```

---

### GET `/executions/{execution_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `execution_id` | `string` | ✓ | query |  |

**Response:**

Returns `ArtifactExecutionResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/executions/{execution_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.executions.get_executions(param='value')
```

---

### GET `/my-executions`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `page` | `number` |  | query |  |
| `per_page` | `number` |  | query |  |

**Response:**

Returns `PaginatedResponse[ArtifactExecutionResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/my-executions' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.my-executions.get_my-executions()
```

---

### POST `/bundles/{bundle_id}/rate`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | body |  |
| `rating` | `BundleRatingCreate` | ✓ | body |  |

**Response:**

Returns `BundleRatingResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/bundles/{bundle_id}/rate' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.post_bundles(param='value')
```

---

### POST `/bundles/{bundle_id}/review`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | body |  |
| `review` | `BundleReviewCreate` | ✓ | body |  |

**Response:**

Returns `BundleReviewResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/bundles/{bundle_id}/review' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.post_bundles(param='value')
```

---

### GET `/bundles/{bundle_id}/reviews`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | query |  |
| `page` | `number` |  | query |  |
| `per_page` | `number` |  | query |  |

**Response:**

Returns `PaginatedResponse[BundleReviewResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/bundles/{bundle_id}/reviews' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.get_bundles(param='value')
```

---

### GET `/bundles/{bundle_id}/versions`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | query |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/bundles/{bundle_id}/versions' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.get_bundles(param='value')
```

---

### GET `/bundles/{bundle_id}/changelog`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | query |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/bundles/{bundle_id}/changelog' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.bundles.get_bundles(param='value')
```

---


# Rules API

## Endpoints

### GET `/bundles`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `category` | `string` |  | query |  |
| `official_only` | `boolean` |  | query |  |
| `page` | `number` |  | query |  |
| `per_page` | `number` |  | query |  |

**Response:**

Returns `RuleBundleList`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/bundles' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.bundles.get_bundles()
```

---

### POST `/bundles/{bundle_id}/install`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | body |  |
| `installation` | `RuleBundleInstallationCreate` | ✓ | body |  |

**Response:**

Returns `RuleBundleInstallationSchema`

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

### GET `/bundles/{bundle_id}/rules`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | query |  |

**Response:**

Returns `List[RuleSchema]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/bundles/{bundle_id}/rules' \
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

### POST `/validate`



**Response:**

Returns `RuleValidationResult`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/validate' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.validate.post_validate()
```

---

### GET `/updates`



**Response:**

Returns `List[RuleBundleUpdates]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/updates' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.updates.get_updates()
```

---

### DELETE `/bundles/{bundle_id}/install`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/bundles/{bundle_id}/install' \
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

### GET `/organizations/{organization_id}/bundles`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `organization_id` | `string` | ✓ | query |  |

**Response:**

Returns `List[RuleBundleSchema]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/organizations/{organization_id}/bundles' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.organizations.get_organizations(param='value')
```

---

### POST `/organizations/{organization_id}/bundles/{bundle_id}/install`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `organization_id` | `string` | ✓ | body |  |
| `bundle_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/organizations/{organization_id}/bundles/{bundle_id}/install' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.organizations.post_organizations(param='value')
```

---

### DELETE `/organizations/{organization_id}/bundles/{bundle_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `organization_id` | `string` | ✓ | body |  |
| `bundle_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/organizations/{organization_id}/bundles/{bundle_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.organizations.delete_organizations(param='value')
```

---

### GET `/organizations/{organization_id}/rules`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `organization_id` | `string` | ✓ | query |  |
| `category` | `string` |  | query |  |
| `severity` | `string` |  | query |  |

**Response:**

Returns `List[RuleSchema]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/organizations/{organization_id}/rules' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.organizations.get_organizations(param='value')
```

---

### GET `/organizations/{organization_id}/rules/stats`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `organization_id` | `string` | ✓ | query |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/organizations/{organization_id}/rules/stats' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.organizations.get_organizations(param='value')
```

---


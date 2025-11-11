# Scanner Integration API

## Endpoints

### GET `/rules/discover`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `category` | `string` |  | query |  |
| `language` | `string` |  | query |  |
| `scanner_type` | `string` |  | query |  |
| `limit` | `number` |  | query |  |

**Response:**

Returns `ListResponse[RuleBundleSchema]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/rules/discover' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.rules.get_rules()
```

---

### GET `/rules/bundle/{bundle_id}/rules`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | query |  |
| `severity` | `string` |  | query |  |
| `language` | `string` |  | query |  |
| `limit` | `number` |  | query |  |

**Response:**

Returns `ListResponse[RuleSchema]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/rules/bundle/{bundle_id}/rules' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.rules.get_rules(param='value')
```

---

### POST `/rules/bundle/{bundle_id}/use`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `bundle_id` | `string` | ✓ | body |  |
| `scan_id` | `string` |  | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/rules/bundle/{bundle_id}/use' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.rules.post_rules(param='value')
```

---

### GET `/plugins/discover`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_type` | `string` |  | query |  |
| `language` | `string` |  | query |  |
| `scanner_integration` | `boolean` |  | query |  |
| `limit` | `number` |  | query |  |

**Response:**

Returns `ListResponse[PluginResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/plugins/discover' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.plugins.get_plugins()
```

---

### GET `/plugins/{plugin_id}/config`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` | ✓ | query |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/plugins/{plugin_id}/config' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.plugins.get_plugins(param='value')
```

---

### POST `/scanner/heartbeat`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scanner_version` | `string` | ✓ | body |  |
| `scanner_type` | `string` |  | body |  |
| `active_rules` | `string[]` |  | body |  |
| `active_plugins` | `string[]` |  | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/scanner/heartbeat' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.scanner.post_scanner()
```

---

### GET `/scanner/recommendations`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `scanner_type` | `string` |  | query |  |
| `current_rules` | `string[]` |  | query |  |
| `current_plugins` | `string[]` |  | query |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/scanner/recommendations' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.scanner.get_scanner()
```

---


# Scan Rules API

## Endpoints

### POST `/rules`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `rule_in` | `ScanRuleCreate` | ✓ | body |  |

**Response:**

Returns `ScanRuleSchema`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/rules' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.rules.post_rules()
```

---

### GET `/rules`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `skip` | `number` |  | query |  |
| `limit` | `number` |  | query |  |
| `tool_filter` | `string` |  | query |  |
| `category_filter` | `string` |  | query |  |
| `severity_filter` | `string` |  | query |  |
| `language_filter` | `string` |  | query |  |
| `is_active` | `boolean` |  | query |  |
| `organization_id` | `string` |  | query |  |

**Response:**

Returns `List[ScanRuleSchema]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/rules' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.rules.get_rules()
```

---

### GET `/rules/{rule_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `rule_id` | `string` | ✓ | query |  |

**Response:**

Returns `ScanRuleSchema`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/rules/{rule_id}' \
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

### POST `/rules/upload`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `file` | `UploadFile` |  | body |  |
| `organization_id` | `string` |  | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/rules/upload' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.rules.post_rules()
```

---

### PUT `/rules/{rule_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `rule_id` | `string` | ✓ | body |  |
| `rule_update` | `ScanRuleUpdate` | ✓ | body |  |

**Response:**

Returns `ScanRuleSchema`

**Example:**

```bash
curl -X PUT 'https://api.tavoai.net/api/v1/rules/{rule_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.rules.put_rules(param='value')
```

---

### DELETE `/rules/{rule_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `rule_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/rules/{rule_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.rules.delete_rules(param='value')
```

---


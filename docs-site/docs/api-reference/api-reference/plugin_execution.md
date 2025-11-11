# Plugin Execution API

## Endpoints

### POST `/execute`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `background_tasks` | `BackgroundTasks` | ✓ | body |  |

**Response:**

Returns `PluginExecutionResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/execute' \
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

Returns `PluginExecutionResponse`

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

### GET `/executions`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `plugin_id` | `string` |  | query |  |
| `limit` | `number` |  | query |  |

**Response:**

Returns `List[PluginExecutionResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/executions' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.executions.get_executions()
```

---


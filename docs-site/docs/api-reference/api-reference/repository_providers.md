# Repository Providers API

## Endpoints

### GET `/`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `enabled_only` | `boolean` |  | query |  |

**Response:**

Returns `List[RepositoryProviderResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client..get_()
```

---

### GET `/{provider_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `provider_id` | `string` | ✓ | query |  |

**Response:**

Returns `RepositoryProviderResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{provider_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{provider_id}.get_{provider_id}(param='value')
```

---


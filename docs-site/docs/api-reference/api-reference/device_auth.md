# Device Auth API

## Endpoints

### POST `/code`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `client_id` | `string` |  | body |  |
| `client_name` | `string` |  | body |  |

**Response:**

Returns `dict`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/code' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.code.post_code()
```

---

### POST `/token`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `device_code` | `string` | ✓ | body |  |

**Response:**

Returns `dict`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/token' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.token.post_token()
```

---

### GET `/info`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `user_code` | `string` | ✓ | query |  |

**Response:**

Returns `dict`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/info' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.info.get_info()
```

---

### POST `/approve`



**Response:**

Returns `dict`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/approve' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.approve.post_approve()
```

---

### POST `/code/cli`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `client_name` | `string` |  | body |  |

**Response:**

Returns `dict`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/code/cli' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.code.post_code()
```

---

### GET `/code/{device_code}/status`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `device_code` | `string` | ✓ | query |  |

**Response:**

Returns `dict`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/code/{device_code}/status' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.code.get_code(param='value')
```

---

### GET `/usage/warnings`



**Response:**

Returns `dict`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/usage/warnings' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.usage.get_usage()
```

---

### GET `/limits`



**Response:**

Returns `dict`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/limits' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client.limits.get_limits()
```

---


# Scan Schedules API

## Endpoints

### POST `/`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `schedule_in` | `ScanScheduleCreate` | ✓ | body |  |

**Response:**

Returns `ScanScheduleResponse`

**Example:**

```bash
curl -X POST 'https://api.tavoai.net/api/v1/' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
result = client..post_()
```

---

### GET `/repository/{repository_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `repository_id` | `string` | ✓ | query |  |

**Response:**

Returns `List[ScanScheduleResponse]`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/repository/{repository_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.repository.get_repository(param='value')
```

---

### GET `/{schedule_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `schedule_id` | `string` | ✓ | query |  |

**Response:**

Returns `ScanScheduleResponse`

**Example:**

```bash
curl -X GET 'https://api.tavoai.net/api/v1/{schedule_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{schedule_id}.get_{schedule_id}(param='value')
```

---

### PUT `/{schedule_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `schedule_id` | `string` | ✓ | body |  |
| `schedule_update` | `ScanScheduleUpdate` | ✓ | body |  |

**Response:**

Returns `ScanScheduleResponse`

**Example:**

```bash
curl -X PUT 'https://api.tavoai.net/api/v1/{schedule_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{schedule_id}.put_{schedule_id}(param='value')
```

---

### DELETE `/{schedule_id}`



**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| `schedule_id` | `string` | ✓ | body |  |

**Response:**

Returns `None`

**Example:**

```bash
curl -X DELETE 'https://api.tavoai.net/api/v1/{schedule_id}' \
  -H 'Authorization: Bearer your-api-key' \
  -H 'Content-Type: application/json'
```

```python
from tavo import TavoClient

client = TavoClient(api_key='your-api-key')
# Example with path parameters
result = client.{schedule_id}.delete_{schedule_id}(param='value')
```

---


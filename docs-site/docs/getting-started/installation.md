---
sidebar_position: 1
---

# Installation

Install the Tavo AI SDK in your preferred programming language.

## Python SDK

### Requirements
- Python 3.8 or higher
- pip package manager

### Installation

```bash
pip install tavo-ai
```

### Verify Installation

```python
import tavo
print(tavo.__version__)
```

## JavaScript/TypeScript SDK

### Requirements
- Node.js 16 or higher
- npm or yarn package manager

### Installation

```bash
npm install @tavoai/sdk
# or
yarn add @tavoai/sdk
```

### TypeScript Support

The SDK includes full TypeScript definitions. No additional setup required.

```typescript
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient({
  apiKey: 'your-api-key'
});
```

## Java SDK

### Requirements
- Java 11 or higher
- Maven 3.6+ or Gradle 6.0+

### Maven Installation

Add to your `pom.xml`:

```xml
<dependency>
    <groupId>ai.tavo</groupId>
    <artifactId>tavo-java-sdk</artifactId>
    <version>0.1.0</version>
</dependency>
```

### Gradle Installation

Add to your `build.gradle`:

```gradle
implementation 'ai.tavo:tavo-java-sdk:0.1.0'
```

## Go SDK

### Requirements
- Go 1.19 or higher

### Installation

```bash
go get github.com/TavoAI/tavo-go-sdk
```

### Verify Installation

```go
package main

import (
    "fmt"
    "github.com/TavoAI/tavo-go-sdk/tavo"
)

func main() {
    config := tavo.NewConfig()
    fmt.Println("SDK installed successfully!")
}
```

## Environment Setup

### API Key Configuration

Set your API key using environment variables:

```bash
# Linux/macOS
export TAVO_API_KEY="your-api-key-here"

# Windows
set TAVO_API_KEY="your-api-key-here"
```

### Base URL Configuration (Optional)

```bash
export TAVO_BASE_URL="https://api.tavo.ai"
```

## Next Steps

Once installed, proceed to [Configuration](./configuration) to set up your SDK.
---
sidebar_position: 1
---

# Tavo AI SDK Documentation

Welcome to the official documentation for the **Tavo AI SDK** - a comprehensive multi-language SDK for integrating AI security and compliance capabilities into your applications.

## What is Tavo AI?

Tavo AI provides advanced AI security analysis, compliance reporting, and risk assessment for AI implementations. Our SDK allows developers to easily integrate AI security scanning, vulnerability detection, and compliance monitoring into their applications and CI/CD pipelines.

## Multi-Language Support

The Tavo AI SDK is available in four major programming languages:

- **Python** - Native async support, perfect for data science and ML workflows
- **JavaScript/TypeScript** - Browser and Node.js support with full TypeScript definitions
- **Java** - Enterprise-grade SDK with Maven support
- **Go** - High-performance SDK for cloud-native applications

## Key Features

- 🔍 **AI Security Scanning** - Detect vulnerabilities in AI models and prompts
- 📊 **Compliance Reporting** - Generate ISO 42001 and OWASP LLM Top 10 reports
- 🚀 **CI/CD Integration** - Seamless integration with GitHub Actions, Jenkins, and more
- 🛡️ **Risk Assessment** - Automated risk scoring and mitigation recommendations
- 📈 **Real-time Monitoring** - Production AI traffic analysis and alerting
- 🔧 **Framework Integration** - Ready-to-use integrations for popular frameworks

## Quick Start

Choose your preferred language to get started:

```bash
# Python
pip install tavo-ai

# JavaScript/TypeScript
npm install @tavoai/sdk

# Java
<dependency>
    <groupId>net.tavoai</groupId>
    <artifactId>sdk</artifactId>
    <version>0.1.0</version>
</dependency>

# Go
go get github.com/TavoAI/tavo-go-sdk
```

## Basic Usage

```python
# Python
from tavo import TavoClient

client = TavoClient(api_key="your-api-key")
result = client.scan_code("def hello(): print('world')")
```

```javascript
// JavaScript/TypeScript
import { TavoClient } from '@tavoai/sdk';

const client = new TavoClient({ apiKey: 'your-api-key' });
const result = await client.scanCode("console.log('hello world');");
```

```java
// Java
import net.tavoai.TavoClient;
import net.tavoai.TavoConfig;

TavoConfig config = TavoConfig.builder()
    .apiKey("your-api-key")
    .build();

TavoClient client = new TavoClient(config);
Map<String, Object> result = client.getScans().createScan(scanData);
```

```go
// Go
import "github.com/TavoAI/tavo-go-sdk/tavo"

config := tavo.NewConfig().WithAPIKey("your-api-key")
client := tavo.NewClient(config)
result, err := client.Scans().CreateScan(scanData)
```

## Support

- 📖 **Documentation** - Comprehensive guides and API references
- 💬 **Community** - Join our Discord community for support
- 🐛 **Issues** - Report bugs on GitHub
- 📧 **Enterprise** - Contact sales for enterprise support

## Next Steps

- [Get Started](./getting-started/installation) - Installation and setup
- [Examples](./examples/django) - Framework-specific examples

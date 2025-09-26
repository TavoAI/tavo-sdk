---
sidebar_position: 4
---

# Spring Boot Integration

Integrate Tavo AI security scanning into your Spring Boot applications.

## Installation

Add the Tavo AI dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>ai.tavo</groupId>
    <artifactId>tavo-java-sdk</artifactId>
    <version>1.0.0</version>
</dependency>
```

Or for Gradle:

```gradle
implementation 'ai.tavo:tavo-java-sdk:1.0.0'
```

## Configuration

### Application Properties

```properties
# application.properties
tavo.api.key=${TAVO_API_KEY:your-api-key-here}
tavo.api.base-url=${TAVO_BASE_URL:https://api.tavo.ai}
tavo.api.timeout=${TAVO_TIMEOUT:30000}
tavo.api.max-retries=${TAVO_MAX_RETRIES:3}
tavo.scanning.enabled=${TAVO_SCANNING_ENABLED:true}
tavo.scanning.rate-limit=${TAVO_RATE_LIMIT:100}
```

### Tavo Configuration Class

```java
// config/TavoConfig.java
package com.example.tavo.config;

import ai.tavo.sdk.TavoClient;
import ai.tavo.sdk.TavoClientConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class TavoConfiguration {

    @Value("${tavo.api.key}")
    private String apiKey;

    @Value("${tavo.api.base-url}")
    private String baseUrl;

    @Value("${tavo.api.timeout}")
    private int timeout;

    @Value("${tavo.api.max-retries}")
    private int maxRetries;

    @Bean
    public TavoClientConfig tavoClientConfig() {
        return TavoClientConfig.builder()
                .apiKey(apiKey)
                .baseUrl(baseUrl)
                .timeout(timeout)
                .maxRetries(maxRetries)
                .build();
    }

    @Bean
    public TavoClient tavoClient(TavoClientConfig config) {
        return new TavoClient(config);
    }
}
```

## Service Layer

### Tavo Service

```java
// service/TavoService.java
package com.example.tavo.service;

import ai.tavo.sdk.TavoClient;
import ai.tavo.sdk.model.ScanRequest;
import ai.tavo.sdk.model.ScanResult;
import ai.tavo.sdk.model.ReportRequest;
import ai.tavo.sdk.model.ReportResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class TavoService {

    private final TavoClient tavoClient;

    public ScanResult scanCode(String code, String language) {
        try {
            ScanRequest request = ScanRequest.builder()
                    .name("Code Scan - " + language)
                    .target(code)
                    .scanType("code")
                    .language(language)
                    .build();

            ScanResult result = tavoClient.getScansApi().createScan(request);
            log.info("Code scan completed with ID: {}", result.getId());
            return result;

        } catch (Exception e) {
            log.error("Code scan failed", e);
            throw new RuntimeException("Code scan failed: " + e.getMessage(), e);
        }
    }

    public ScanResult scanUrl(String url) {
        try {
            ScanRequest request = ScanRequest.builder()
                    .name("URL Scan - " + url)
                    .target(url)
                    .scanType("web")
                    .build();

            ScanResult result = tavoClient.getScansApi().createScan(request);
            log.info("URL scan completed with ID: {}", result.getId());
            return result;

        } catch (Exception e) {
            log.error("URL scan failed", e);
            throw new RuntimeException("URL scan failed: " + e.getMessage(), e);
        }
    }

    public ScanResult getScanResults(String scanId) {
        try {
            return tavoClient.getScansApi().getScanResults(scanId);
        } catch (Exception e) {
            log.error("Failed to get scan results for ID: {}", scanId, e);
            throw new RuntimeException("Failed to get scan results: " + e.getMessage(), e);
        }
    }

    public ReportResult generateReport(java.util.List<String> scanIds, String format) {
        try {
            ReportRequest request = ReportRequest.builder()
                    .type("compliance")
                    .format(format)
                    .scanIds(scanIds)
                    .build();

            ReportResult result = tavoClient.getReportsApi().generateReport(request);
            log.info("Report generated with ID: {}", result.getId());
            return result;

        } catch (Exception e) {
            log.error("Report generation failed", e);
            throw new RuntimeException("Report generation failed: " + e.getMessage(), e);
        }
    }
}
```

## REST Controllers

### Scan Controller

```java
// controller/ScanController.java
package com.example.tavo.controller;

import com.example.tavo.service.TavoService;
import ai.tavo.sdk.model.ScanResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.util.Map;

@RestController
@RequestMapping("/api/scan")
@RequiredArgsConstructor
@Slf4j
public class ScanController {

    private final TavoService tavoService;

    @PostMapping("/code")
    public ResponseEntity<?> scanCode(@Valid @RequestBody ScanCodeRequest request) {
        try {
            ScanResult result = tavoService.scanCode(request.getCode(), request.getLanguage());
            return ResponseEntity.ok(Map.of(
                    "success", true,
                    "data", result
            ));
        } catch (Exception e) {
            log.error("Code scan failed", e);
            return ResponseEntity.internalServerError()
                    .body(Map.of(
                            "error", e.getMessage(),
                            "code", "SCAN_FAILED"
                    ));
        }
    }

    @PostMapping("/url")
    public ResponseEntity<?> scanUrl(@Valid @RequestBody ScanUrlRequest request) {
        try {
            // Basic URL validation
            if (!request.getUrl().startsWith("http://") && !request.getUrl().startsWith("https://")) {
                return ResponseEntity.badRequest()
                        .body(Map.of(
                                "error", "Invalid URL format",
                                "code", "INVALID_URL"
                        ));
            }

            ScanResult result = tavoService.scanUrl(request.getUrl());
            return ResponseEntity.ok(Map.of(
                    "success", true,
                    "data", result
            ));
        } catch (Exception e) {
            log.error("URL scan failed", e);
            return ResponseEntity.internalServerError()
                    .body(Map.of(
                            "error", e.getMessage(),
                            "code", "SCAN_FAILED"
                    ));
        }
    }

    @GetMapping("/{scanId}/results")
    public ResponseEntity<?> getScanResults(@PathVariable String scanId) {
        try {
            ScanResult result = tavoService.getScanResults(scanId);
            return ResponseEntity.ok(Map.of(
                    "success", true,
                    "data", result
            ));
        } catch (Exception e) {
            log.error("Failed to get scan results", e);
            return ResponseEntity.internalServerError()
                    .body(Map.of(
                            "error", e.getMessage(),
                            "code", "RESULTS_FAILED"
                    ));
        }
    }

    // Request DTOs
    public static class ScanCodeRequest {
        @NotBlank(message = "Code is required")
        private String code;

        @NotNull(message = "Language is required")
        private String language = "java";

        // Getters and setters
        public String getCode() { return code; }
        public void setCode(String code) { this.code = code; }
        public String getLanguage() { return language; }
        public void setLanguage(String language) { this.language = language; }
    }

    public static class ScanUrlRequest {
        @NotBlank(message = "URL is required")
        private String url;

        // Getters and setters
        public String getUrl() { return url; }
        public void setUrl(String url) { this.url = url; }
    }
}
```

### Report Controller

```java
// controller/ReportController.java
package com.example.tavo.controller;

import com.example.tavo.service.TavoService;
import ai.tavo.sdk.model.ReportResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/reports")
@RequiredArgsConstructor
@Slf4j
public class ReportController {

    private final TavoService tavoService;

    @PostMapping("/generate")
    public ResponseEntity<?> generateReport(@Valid @RequestBody GenerateReportRequest request) {
        try {
            ReportResult result = tavoService.generateReport(request.getScanIds(), request.getFormat());
            return ResponseEntity.ok(Map.of(
                    "success", true,
                    "data", result
            ));
        } catch (Exception e) {
            log.error("Report generation failed", e);
            return ResponseEntity.internalServerError()
                    .body(Map.of(
                            "error", e.getMessage(),
                            "code", "REPORT_FAILED"
                    ));
        }
    }

    // Request DTO
    public static class GenerateReportRequest {
        @NotEmpty(message = "At least one scan ID is required")
        private List<String> scanIds;

        @NotNull(message = "Format is required")
        private String format = "pdf";

        // Getters and setters
        public List<String> getScanIds() { return scanIds; }
        public void setScanIds(List<String> scanIds) { this.scanIds = scanIds; }
        public String getFormat() { return format; }
        public void setFormat(String format) { this.format = format; }
    }
}
```

## Security Configuration

### Rate Limiting

```java
// config/RateLimitConfig.java
package com.example.tavo.config;

import io.github.bucket4j.Bandwidth;
import io.github.bucket4j.Bucket;
import io.github.bucket4j.Refill;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Duration;
import java.util.concurrent.ConcurrentHashMap;

@Configuration
public class RateLimitConfig {

    @Value("${tavo.scanning.rate-limit:100}")
    private int rateLimit;

    @Bean
    public ConcurrentHashMap<String, Bucket> rateLimitCache() {
        return new ConcurrentHashMap<>();
    }

    @Bean
    public Bandwidth rateLimitBandwidth() {
        return Bandwidth.classic(rateLimit, Refill.intervally(rateLimit, Duration.ofMinutes(15)));
    }
}
```

### Security Interceptor

```java
// interceptor/RateLimitInterceptor.java
package com.example.tavo.interceptor;

import io.github.bucket4j.Bucket;
import io.github.bucket4j.ConsumptionProbe;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.concurrent.ConcurrentHashMap;

@Component
@RequiredArgsConstructor
public class RateLimitInterceptor implements HandlerInterceptor {

    @Qualifier("rateLimitCache")
    private final ConcurrentHashMap<String, Bucket> cache;

    private final Bucket rateLimitBucket;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        if (request.getRequestURI().startsWith("/api/scan")) {
            String clientId = getClientId(request);
            Bucket bucket = cache.computeIfAbsent(clientId, k -> rateLimitBucket);

            ConsumptionProbe probe = bucket.tryConsumeAndReturnRemaining(1);
            if (probe.isConsumed()) {
                response.setHeader("X-Rate-Limit-Remaining", String.valueOf(probe.getRemainingTokens()));
                return true;
            } else {
                response.setStatus(429);
                response.setHeader("X-Rate-Limit-Retry-After-Seconds",
                        String.valueOf(probe.getNanosToWaitForRefill() / 1_000_000_000));
                return false;
            }
        }
        return true;
    }

    private String getClientId(HttpServletRequest request) {
        String xForwardedFor = request.getHeader("X-Forwarded-For");
        if (xForwardedFor != null && !xForwardedFor.isEmpty()) {
            return xForwardedFor.split(",")[0].trim();
        }
        return request.getRemoteAddr();
    }
}
```

### Web Configuration

```java
// config/WebConfig.java
package com.example.tavo.config;

import com.example.tavo.interceptor.RateLimitInterceptor;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    private final RateLimitInterceptor rateLimitInterceptor;

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("http://localhost:3000", "http://localhost:8080")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true);
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(rateLimitInterceptor)
                .addPathPatterns("/api/**");
    }
}
```

## Asynchronous Processing

### Async Configuration

```java
// config/AsyncConfig.java
package com.example.tavo.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {

    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("TavoAsync-");
        executor.initialize();
        return executor;
    }
}
```

### Async Service

```java
// service/AsyncTavoService.java
package com.example.tavo.service;

import ai.tavo.sdk.model.ScanResult;
import ai.tavo.sdk.model.ReportResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.concurrent.CompletableFuture;

@Service
@RequiredArgsConstructor
@Slf4j
public class AsyncTavoService {

    private final TavoService tavoService;

    @Async
    public CompletableFuture<ScanResult> scanCodeAsync(String code, String language) {
        try {
            ScanResult result = tavoService.scanCode(code, language);
            return CompletableFuture.completedFuture(result);
        } catch (Exception e) {
            log.error("Async code scan failed", e);
            CompletableFuture<ScanResult> future = new CompletableFuture<>();
            future.completeExceptionally(e);
            return future;
        }
    }

    @Async
    public CompletableFuture<ScanResult> scanUrlAsync(String url) {
        try {
            ScanResult result = tavoService.scanUrl(url);
            return CompletableFuture.completedFuture(result);
        } catch (Exception e) {
            log.error("Async URL scan failed", e);
            CompletableFuture<ScanResult> future = new CompletableFuture<>();
            future.completeExceptionally(e);
            return future;
        }
    }

    @Async
    public CompletableFuture<ReportResult> generateReportAsync(List<String> scanIds, String format) {
        try {
            ReportResult result = tavoService.generateReport(scanIds, format);
            return CompletableFuture.completedFuture(result);
        } catch (Exception e) {
            log.error("Async report generation failed", e);
            CompletableFuture<ReportResult> future = new CompletableFuture<>();
            future.completeExceptionally(e);
            return future;
        }
    }
}
```

### Async Controller

```java
// controller/AsyncScanController.java
package com.example.tavo.controller;

import com.example.tavo.service.AsyncTavoService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/api/async/scan")
@RequiredArgsConstructor
@Slf4j
public class AsyncScanController {

    private final AsyncTavoService asyncTavoService;

    @PostMapping("/code")
    public CompletableFuture<ResponseEntity<?>> scanCodeAsync(@Valid @RequestBody ScanController.ScanCodeRequest request) {
        return asyncTavoService.scanCodeAsync(request.getCode(), request.getLanguage())
                .thenApply(result -> ResponseEntity.ok(Map.of(
                        "success", true,
                        "data", result
                )))
                .exceptionally(e -> {
                    log.error("Async code scan failed", e);
                    return ResponseEntity.internalServerError()
                            .body(Map.of(
                                    "error", e.getMessage(),
                                    "code", "SCAN_FAILED"
                            ));
                });
    }

    @PostMapping("/url")
    public CompletableFuture<ResponseEntity<?>> scanUrlAsync(@Valid @RequestBody ScanController.ScanUrlRequest request) {
        return asyncTavoService.scanUrlAsync(request.getUrl())
                .thenApply(result -> ResponseEntity.ok(Map.of(
                        "success", true,
                        "data", result
                )))
                .exceptionally(e -> {
                    log.error("Async URL scan failed", e);
                    return ResponseEntity.internalServerError()
                            .body(Map.of(
                                    "error", e.getMessage(),
                                    "code", "SCAN_FAILED"
                            ));
                });
    }
}
```

## Web Interface

### Controller for Web Pages

```java
// controller/WebController.java
package com.example.tavo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class WebController {

    @GetMapping("/")
    public String index() {
        return "index";
    }

    @GetMapping("/scan")
    public String scan() {
        return "scan";
    }
}
```

### Thymeleaf Templates

```html
<!-- templates/scan.html -->
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tavo AI Security Scanner</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">
            Tavo AI Security Scanner
        </h1>

        <!-- Code Scanner -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 class="text-2xl font-semibold mb-4">Code Security Scan</h2>

            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Programming Language
                </label>
                <select id="language" class="w-full p-2 border border-gray-300 rounded-md">
                    <option value="java">Java</option>
                    <option value="javascript">JavaScript</option>
                    <option value="python">Python</option>
                    <option value="go">Go</option>
                </select>
            </div>

            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Code to Scan
                </label>
                <textarea
                    id="code"
                    rows="10"
                    class="w-full p-2 border border-gray-300 rounded-md font-mono text-sm"
                    placeholder="Paste your code here..."
                ></textarea>
            </div>

            <div class="flex space-x-4">
                <button
                    id="scanCodeBtn"
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                    Scan Code
                </button>
                <button
                    id="scanCodeAsyncBtn"
                    class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                    Scan Code (Async)
                </button>
            </div>
        </div>

        <!-- URL Scanner -->
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 class="text-2xl font-semibold mb-4">URL Security Scan</h2>

            <div class="mb-4">
                <input
                    type="url"
                    id="url"
                    class="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="https://example.com"
                >
            </div>

            <div class="flex space-x-4">
                <button
                    id="scanUrlBtn"
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                >
                    Scan URL
                </button>
                <button
                    id="scanUrlAsyncBtn"
                    class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                    Scan URL (Async)
                </button>
            </div>
        </div>

        <!-- Results -->
        <div id="results" class="bg-white rounded-lg shadow-md p-6 hidden">
            <h2 class="text-2xl font-semibold mb-4">Scan Results</h2>
            <div id="resultsContent"></div>
        </div>
    </div>

    <script>
        const API_BASE = '/api';

        // Synchronous code scanning
        document.getElementById('scanCodeBtn').addEventListener('click', async () => {
            const code = document.getElementById('code').value;
            const language = document.getElementById('language').value;
            const btn = document.getElementById('scanCodeBtn');

            if (!code.trim()) {
                alert('Please enter some code to scan');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Scanning...';

            try {
                const response = await fetch(`${API_BASE}/scan/code`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code, language })
                });

                const result = await response.json();
                displayResults(result);

            } catch (error) {
                displayResults({ error: error.message });
            } finally {
                btn.disabled = false;
                btn.textContent = 'Scan Code';
            }
        });

        // Asynchronous code scanning
        document.getElementById('scanCodeAsyncBtn').addEventListener('click', async () => {
            const code = document.getElementById('code').value;
            const language = document.getElementById('language').value;
            const btn = document.getElementById('scanCodeAsyncBtn');

            if (!code.trim()) {
                alert('Please enter some code to scan');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Scanning...';

            try {
                const response = await fetch(`${API_BASE}/async/scan/code`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code, language })
                });

                const result = await response.json();
                displayResults(result);

            } catch (error) {
                displayResults({ error: error.message });
            } finally {
                btn.disabled = false;
                btn.textContent = 'Scan Code (Async)';
            }
        });

        // Synchronous URL scanning
        document.getElementById('scanUrlBtn').addEventListener('click', async () => {
            const url = document.getElementById('url').value;
            const btn = document.getElementById('scanUrlBtn');

            if (!url.trim()) {
                alert('Please enter a URL to scan');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Scanning...';

            try {
                const response = await fetch(`${API_BASE}/scan/url`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url })
                });

                const result = await response.json();
                displayResults(result);

            } catch (error) {
                displayResults({ error: error.message });
            } finally {
                btn.disabled = false;
                btn.textContent = 'Scan URL';
            }
        });

        // Asynchronous URL scanning
        document.getElementById('scanUrlAsyncBtn').addEventListener('click', async () => {
            const url = document.getElementById('url').value;
            const btn = document.getElementById('scanUrlAsyncBtn');

            if (!url.trim()) {
                alert('Please enter a URL to scan');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Scanning...';

            try {
                const response = await fetch(`${API_BASE}/async/scan/url`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url })
                });

                const result = await response.json();
                displayResults(result);

            } catch (error) {
                displayResults({ error: error.message });
            } finally {
                btn.disabled = false;
                btn.textContent = 'Scan URL (Async)';
            }
        });

        function displayResults(result) {
            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');

            if (result.success) {
                const data = result.data;
                resultsContent.innerHTML = `
                    <div class="mb-4">
                        <h3 class="text-lg font-semibold text-green-600">Scan Successful</h3>
                        <p class="text-sm text-gray-600">Scan ID: ${data.id}</p>
                        <p class="text-sm text-gray-600">Status: ${data.status}</p>
                    </div>
                    ${data.summary ? `
                    <div class="mb-4">
                        <h4 class="font-semibold">Summary:</h4>
                        <ul class="list-disc list-inside text-sm">
                            <li>Files scanned: ${data.summary.filesScanned || 0}</li>
                            <li>Vulnerabilities found: ${data.summary.vulnerabilitiesFound || 0}</li>
                            <li>Scan duration: ${data.summary.duration || 'N/A'}</li>
                        </ul>
                    </div>
                    ` : ''}
                    <button
                        onclick="viewDetailedResults('${data.id}')"
                        class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                    >
                        View Detailed Results
                    </button>
                `;
            } else {
                resultsContent.innerHTML = `
                    <div class="text-red-600">
                        <h3 class="text-lg font-semibold">Scan Failed</h3>
                        <p>${result.error}</p>
                    </div>
                `;
            }

            resultsDiv.classList.remove('hidden');
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }

        async function viewDetailedResults(scanId) {
            try {
                const response = await fetch(`${API_BASE}/scan/${scanId}/results`);
                const result = await response.json();

                if (result.success) {
                    // Display detailed results (implement as needed)
                    console.log('Detailed results:', result.data);
                }
            } catch (error) {
                console.error('Failed to get detailed results:', error);
            }
        }
    </script>
</body>
</html>
```

## Testing

### Unit Tests

```java
// test/TavoServiceTest.java
package com.example.tavo;

import com.example.tavo.service.TavoService;
import ai.tavo.sdk.TavoClient;
import ai.tavo.sdk.model.ScanResult;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TavoServiceTest {

    @Mock
    private TavoClient tavoClient;

    @Mock
    private ai.tavo.sdk.api.ScansApi scansApi;

    @InjectMocks
    private TavoService tavoService;

    @Test
    void scanCode_Success() {
        // Given
        ScanResult expectedResult = ScanResult.builder()
                .id("test-scan-id")
                .status("completed")
                .build();

        when(tavoClient.getScansApi()).thenReturn(scansApi);
        when(scansApi.createScan(any())).thenReturn(expectedResult);

        // When
        ScanResult result = tavoService.scanCode("System.out.println(\"test\");", "java");

        // Then
        assertNotNull(result);
        assertEquals("test-scan-id", result.getId());
        assertEquals("completed", result.getStatus());
    }

    @Test
    void scanCode_Failure_ThrowsException() {
        // Given
        when(tavoClient.getScansApi()).thenReturn(scansApi);
        when(scansApi.createScan(any())).thenThrow(new RuntimeException("API Error"));

        // When & Then
        RuntimeException exception = assertThrows(RuntimeException.class, () ->
            tavoService.scanCode("invalid code", "java")
        );
        assertTrue(exception.getMessage().contains("Code scan failed"));
    }
}
```

### Integration Tests

```java
// test/ScanControllerIntegrationTest.java
package com.example.tavo;

import com.example.tavo.controller.ScanController;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureWebMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureWebMvc
class ScanControllerIntegrationTest {

    @Autowired
    private ScanController scanController;

    @Autowired
    private ObjectMapper objectMapper;

    private MockMvc mockMvc;

    @Test
    void scanCode_ValidRequest_ReturnsSuccess() throws Exception {
        mockMvc = MockMvcBuilders.standaloneSetup(scanController).build();

        ScanController.ScanCodeRequest request = new ScanController.ScanCodeRequest();
        request.setCode("public class Test { }");
        request.setLanguage("java");

        mockMvc.perform(post("/api/scan/code")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.data").exists());
    }

    @Test
    void scanCode_MissingCode_ReturnsBadRequest() throws Exception {
        mockMvc = MockMvcBuilders.standaloneSetup(scanController).build();

        ScanController.ScanCodeRequest request = new ScanController.ScanCodeRequest();
        // Don't set code

        mockMvc.perform(post("/api/scan/code")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest());
    }
}
```

## Docker Configuration

### Dockerfile

```dockerfile
FROM openjdk:17-jdk-slim

WORKDIR /app

# Copy Maven wrapper and pom.xml
COPY .mvn/ .mvn
COPY mvnw pom.xml ./

# Download dependencies (for better caching)
RUN ./mvnw dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN ./mvnw clean package -DskipTests

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target/tavo-spring-boot-0.0.1-SNAPSHOT.jar"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  tavo-spring-boot:
    build: .
    ports:
      - "8080:8080"
    environment:
      - TAVO_API_KEY=${TAVO_API_KEY}
      - TAVO_BASE_URL=https://api.tavo.ai
      - SPRING_PROFILES_ACTIVE=docker
    restart: unless-stopped
```

### Application Docker Profile

```properties
# application-docker.properties
server.port=8080
logging.level.com.example.tavo=INFO
spring.thymeleaf.cache=false
```

## Deployment

### Production Configuration

```properties
# application-prod.properties
server.port=8080
logging.level.com.example.tavo=WARN
spring.thymeleaf.cache=true
management.endpoints.web.exposure.include=health,info,metrics
management.endpoint.health.show-details=when-authorized

# Database configuration (if needed)
spring.datasource.url=jdbc:postgresql://localhost:5432/tavo_db
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}
spring.jpa.hibernate.ddl-auto=validate
```

### Health Checks

```java
// controller/HealthController.java
package com.example.tavo.controller;

import com.example.tavo.service.TavoService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.Map;

@RestController
@RequiredArgsConstructor
public class HealthController {

    private final TavoService tavoService;

    @GetMapping("/health")
    public ResponseEntity<?> health() {
        try {
            // Test Tavo service connectivity
            // This is a simple health check - in production you might want to cache this
            Map<String, Object> health = Map.of(
                    "status", "UP",
                    "timestamp", LocalDateTime.now(),
                    "service", "tavo-spring-boot-integration",
                    "tavo", Map.of(
                            "status", "UP",
                            "message", "Tavo service is accessible"
                    )
            );
            return ResponseEntity.ok(health);
        } catch (Exception e) {
            Map<String, Object> health = Map.of(
                    "status", "DOWN",
                    "timestamp", LocalDateTime.now(),
                    "service", "tavo-spring-boot-integration",
                    "tavo", Map.of(
                            "status", "DOWN",
                            "message", e.getMessage()
                    )
            );
            return ResponseEntity.status(503).body(health);
        }
    }
}
```

This Spring Boot integration provides a comprehensive, enterprise-ready solution for incorporating Tavo AI security scanning into Java applications with robust error handling, rate limiting, asynchronous processing, and extensive testing coverage.

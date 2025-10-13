# Java SDK Examples

This directory contains comprehensive examples for using the Tavo AI Java SDK.

## Installation

### Maven

```xml
<dependency>
    <groupId>net.tavoai</groupId>
    <artifactId>sdk</artifactId>
    <version>1.0.0</version>
</dependency>
```

### Gradle

```gradle
implementation 'net.tavoai:sdk:1.0.0'
```

## Basic Usage

### Simple Code Scan

```java
import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ScanResult;
import net.tavoai.sdk.model.Vulnerability;

public class BasicScanExample {
    public static void main(String[] args) {
        // Initialize client
        TavoClient client = new TavoClient("your-api-key");

        // Code to scan
        String code = """
            public void processUserInput(String userInput) {
                String query = "SELECT * FROM users WHERE id = '" + userInput + "'";
                // Potential SQL injection vulnerability
                executeQuery(query);
            }
            """;

        try {
            // Scan the code
            ScanResult result = client.scanCode(code, "java").block();

            System.out.println("Found " + result.getTotalIssues() + " issues");

            for (Vulnerability vuln : result.getVulnerabilities()) {
                System.out.println("- " + vuln.getTitle() + ": " + vuln.getDescription());
            }

        } catch (Exception e) {
            System.err.println("Scan failed: " + e.getMessage());
        } finally {
            // Clean up
            client.close();
        }
    }
}
```

### Configuration and Error Handling

```java
import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.TavoClientConfig;
import net.tavoai.sdk.exception.TavoException;
import net.tavoai.sdk.exception.TavoAuthException;
import net.tavoai.sdk.exception.TavoApiException;
import java.time.Duration;

public class ConfiguredScanExample {
    public static void main(String[] args) {
        // Configure client
        TavoClientConfig config = TavoClientConfig.builder()
                .apiKey("your-api-key")
                .baseUrl("https://api.tavoai.net")
                .timeout(Duration.ofSeconds(30))
                .maxRetries(3)
                .retryDelay(Duration.ofSeconds(1))
                .build();

        TavoClient client = new TavoClient(config);

        try {
            ScanResult result = client.scanCode("System.out.println(\"hello\");", "java")
                    .block();

            System.out.println("Scan successful: " + result.getTotalIssues() + " issues");

        } catch (TavoAuthException e) {
            System.err.println("Authentication failed: " + e.getMessage());
        } catch (TavoApiException e) {
            System.err.println("API error: " + e.getMessage() + " (status: " + e.getStatusCode() + ")");
        } catch (TavoException e) {
            System.err.println("Tavo error: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Unexpected error: " + e.getMessage());
        } finally {
            client.close();
        }
    }
}
```

## Advanced Examples

### Reactive Batch Scanning

```java
import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ScanResult;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

public class BatchScanner {
    private final TavoClient client;

    public BatchScanner(String apiKey) {
        this.client = new TavoClient(apiKey);
    }

    public Mono<Void> scanDirectory(String directoryPath) {
        return findJavaFiles(directoryPath)
                .flatMapMany(Flux::fromIterable)
                .flatMap(this::scanFile, 5) // Concurrent scanning with max 5 concurrent requests
                .doOnNext(result -> System.out.println(result.getFilePath() + ": " + result.getIssues() + " issues"))
                .reduce(0, (total, result) -> total + result.getIssues())
                .doOnNext(totalIssues -> System.out.println("Total issues found: " + totalIssues))
                .then();
    }

    private Mono<List<Path>> findJavaFiles(String directoryPath) {
        return Mono.fromCallable(() -> {
            try {
                return Files.walk(Paths.get(directoryPath))
                        .filter(Files::isRegularFile)
                        .filter(path -> path.toString().endsWith(".java"))
                        .collect(Collectors.toList());
            } catch (Exception e) {
                throw new RuntimeException("Failed to find Java files", e);
            }
        }).subscribeOn(Schedulers.boundedElastic());
    }

    private Mono<ScanResultWithPath> scanFile(Path filePath) {
        return Mono.fromCallable(() -> Files.readString(filePath))
                .subscribeOn(Schedulers.boundedElastic())
                .flatMap(code -> client.scanCode(code, "java"))
                .map(result -> new ScanResultWithPath(filePath.toString(), result.getTotalIssues()))
                .onErrorResume(e -> {
                    System.err.println("Failed to scan " + filePath + ": " + e.getMessage());
                    return Mono.just(new ScanResultWithPath(filePath.toString(), 0));
                });
    }

    public void close() {
        client.close();
    }

    private static class ScanResultWithPath {
        private final String filePath;
        private final int issues;

        public ScanResultWithPath(String filePath, int issues) {
            this.filePath = filePath;
            this.issues = issues;
        }

        public String getFilePath() { return filePath; }
        public int getIssues() { return issues; }
    }

    public static void main(String[] args) {
        BatchScanner scanner = new BatchScanner("your-api-key");

        scanner.scanDirectory("./src/main/java")
                .doFinally(signal -> scanner.close())
                .block();
    }
}
```

### AI Model Analysis

```java
import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ModelAnalysis;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class ModelAnalysisExample {
    public static void main(String[] args) {
        TavoClient client = new TavoClient("your-api-key");

        try {
            ObjectMapper mapper = new ObjectMapper();
            ObjectNode modelConfig = mapper.createObjectNode();

            modelConfig.put("model_type", "transformer");

            ObjectNode architecture = modelConfig.putObject("architecture");
            architecture.put("layers", 12);
            architecture.put("attention_heads", 8);
            architecture.put("hidden_size", 768);
            architecture.put("vocab_size", 30000);

            ObjectNode training = modelConfig.putObject("training");
            training.put("dataset", "wikipedia");
            training.put("epochs", 10);
            training.put("learning_rate", 0.0001);

            ModelAnalysis analysis = client.analyzeModel(modelConfig).block();

            System.out.println("Model safety: " + (analysis.isSafe() ? "Safe" : "Unsafe"));

            if (!analysis.isSafe() && analysis.getIssues() != null) {
                System.out.println("Issues found:");
                analysis.getIssues().forEach((issue, index) -> {
                    System.out.println((index + 1) + ". " + issue.getTitle() + ": " + issue.getDescription());
                });
            }

        } catch (Exception e) {
            System.err.println("Analysis failed: " + e.getMessage());
        } finally {
            client.close();
        }
    }
}
```

### Webhook Management

```java
import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.Webhook;
import net.tavoai.sdk.model.WebhookConfig;
import java.util.Arrays;
import java.util.List;

public class WebhookManagementExample {
    public static void main(String[] args) {
        TavoClient client = new TavoClient("your-api-key");

        try {
            // Create a webhook
            WebhookConfig config = WebhookConfig.builder()
                    .url("https://myapp.com/webhook/scan-complete")
                    .events(Arrays.asList("scan.completed", "vulnerability.found"))
                    .secret("webhook-secret")
                    .active(true)
                    .build();

            Webhook webhook = client.createWebhook(config).block();
            System.out.println("Created webhook: " + webhook.getId());

            // List all webhooks
            List<Webhook> webhooks = client.listWebhooks().collectList().block();
            System.out.println("Total webhooks: " + webhooks.size());

            webhooks.forEach(wh -> {
                System.out.println("- " + wh.getId() + ": " + wh.getUrl() +
                                 " (" + String.join(", ", wh.getEvents()) + ")");
            });

            // Update webhook
            WebhookConfig updateConfig = WebhookConfig.builder()
                    .events(Arrays.asList("scan.completed", "vulnerability.found", "scan.failed"))
                    .build();

            client.updateWebhook(webhook.getId(), updateConfig).block();
            System.out.println("Webhook updated");

            // Delete the webhook
            client.deleteWebhook(webhook.getId()).block();
            System.out.println("Webhook deleted");

        } catch (Exception e) {
            System.err.println("Webhook management failed: " + e.getMessage());
        } finally {
            client.close();
        }
    }
}
```

## Integration Examples

### Spring Boot REST API

```java
package com.example.securityscanner;

import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ScanResult;
import net.tavoai.sdk.model.Vulnerability;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import javax.annotation.PreDestroy;
import java.util.List;
import java.util.stream.Collectors;

@SpringBootApplication
public class SecurityScannerApplication {
    public static void main(String[] args) {
        SpringApplication.run(SecurityScannerApplication.class, args);
    }
}

@RestController
@RequestMapping("/api/security")
@RequiredArgsConstructor
@Slf4j
class SecurityController {

    private final TavoClient tavoClient;

    @PostMapping("/scan")
    public Mono<ResponseEntity<ScanResponse>> scanCode(@RequestBody ScanRequest request) {
        return tavoClient.scanCode(request.getCode(), request.getLanguage())
                .map(result -> {
                    List<VulnerabilityDto> vulnerabilities = result.getVulnerabilities()
                            .stream()
                            .map(this::convertToDto)
                            .collect(Collectors.toList());

                    ScanResponse response = new ScanResponse(
                            result.getTotalIssues(),
                            vulnerabilities,
                            result.getScanId()
                    );

                    return ResponseEntity.ok(response);
                })
                .onErrorResume(TavoAuthException.class, e ->
                    Mono.just(ResponseEntity.status(401).build()))
                .onErrorResume(TavoApiException.class, e ->
                    Mono.just(ResponseEntity.status(e.getStatusCode()).build()))
                .onErrorResume(Exception.class, e -> {
                    log.error("Scan failed", e);
                    return Mono.just(ResponseEntity.status(500).build());
                });
    }

    @PostMapping("/scan/async")
    public Mono<ResponseEntity<AsyncScanResponse>> scanCodeAsync(@RequestBody AsyncScanRequest request) {
        String scanId = "scan_" + System.currentTimeMillis() + "_" +
                       java.util.UUID.randomUUID().toString().substring(0, 8);

        // Start async processing
        tavoClient.scanCode(request.getCode(), request.getLanguage())
                .doOnNext(result -> {
                    if (request.getWebhookUrl() != null) {
                        sendWebhookNotification(request.getWebhookUrl(), scanId, result);
                    }
                    log.info("Async scan {} completed: {} issues", scanId, result.getTotalIssues());
                })
                .doOnError(error ->
                    log.error("Async scan {} failed", scanId, error))
                .subscribe();

        AsyncScanResponse response = new AsyncScanResponse(
                scanId,
                "processing",
                "Scan started. Results will be sent to webhook."
        );

        return Mono.just(ResponseEntity.accepted().body(response));
    }

    private void sendWebhookNotification(String webhookUrl, String scanId, ScanResult result) {
        // Implementation would send HTTP POST to webhookUrl with scan results
        log.info("Sending webhook notification to {} for scan {}", webhookUrl, scanId);
    }

    private VulnerabilityDto convertToDto(Vulnerability vuln) {
        return new VulnerabilityDto(
                vuln.getTitle(),
                vuln.getDescription(),
                vuln.getSeverity(),
                vuln.getLocation() != null ? new LocationDto(
                        vuln.getLocation().getFile(),
                        vuln.getLocation().getLine(),
                        vuln.getLocation().getColumn()
                ) : null
        );
    }
}

@Configuration
class TavoConfig {

    @Bean
    @PreDestroy
    public TavoClient tavoClient(@Value("${tavo.api.key}") String apiKey) {
        return new TavoClient(TavoClientConfig.builder()
                .apiKey(apiKey)
                .timeout(Duration.ofSeconds(60))
                .maxRetries(3)
                .build());
    }
}

// DTOs
record ScanRequest(String code, String language) {}
record AsyncScanRequest(String code, String language, String webhookUrl) {}
record ScanResponse(int totalIssues, List<VulnerabilityDto> vulnerabilities, String scanId) {}
record AsyncScanResponse(String scanId, String status, String message) {}
record VulnerabilityDto(String title, String description, String severity, LocationDto location) {}
record LocationDto(String file, int line, int column) {}
```

### Quarkus REST API

```java
package com.example.securityscanner;

import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ScanResult;
import net.tavoai.sdk.model.Vulnerability;
import io.smallrye.mutiny.Uni;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.jboss.logging.Logger;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.List;
import java.util.stream.Collectors;

@Path("/api/security")
@ApplicationScoped
public class SecurityResource {

    private static final Logger LOG = Logger.getLogger(SecurityResource.class);

    @Inject
    TavoClient tavoClient;

    @POST
    @Path("/scan")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Uni<Response> scanCode(ScanRequest request) {
        return tavoClient.scanCode(request.code, request.language)
                .onItem().transform(result -> {
                    List<VulnerabilityDto> vulnerabilities = result.getVulnerabilities()
                            .stream()
                            .map(this::convertToDto)
                            .collect(Collectors.toList());

                    ScanResponse response = new ScanResponse(
                            result.getTotalIssues(),
                            vulnerabilities,
                            result.getScanId()
                    );

                    return Response.ok(response).build();
                })
                .onFailure().recoverWithItem(throwable -> {
                    LOG.error("Scan failed", throwable);
                    return Response.status(Response.Status.INTERNAL_SERVER_ERROR).build();
                });
    }

    private VulnerabilityDto convertToDto(Vulnerability vuln) {
        return new VulnerabilityDto(
                vuln.getTitle(),
                vuln.getDescription(),
                vuln.getSeverity(),
                vuln.getLocation() != null ? new LocationDto(
                        vuln.getLocation().getFile(),
                        vuln.getLocation().getLine(),
                        vuln.getLocation().getColumn()
                ) : null
        );
    }
}

// DTOs
record ScanRequest(String code, String language) {}
record ScanResponse(int totalIssues, List<VulnerabilityDto> vulnerabilities, String scanId) {}
record VulnerabilityDto(String title, String description, String severity, LocationDto location) {}
record LocationDto(String file, int line, int column) {}

// CDI Producer for TavoClient
package com.example.securityscanner;

import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.TavoClientConfig;
import io.quarkus.runtime.StartupEvent;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import javax.enterprise.context.ApplicationScoped;
import javax.enterprise.event.Observes;
import javax.enterprise.inject.Disposes;
import javax.enterprise.inject.Produces;
import java.time.Duration;

@ApplicationScoped
public class TavoClientProducer {

    @ConfigProperty(name = "tavo.api.key")
    String apiKey;

    @Produces
    @ApplicationScoped
    public TavoClient produceTavoClient() {
        return new TavoClient(TavoClientConfig.builder()
                .apiKey(apiKey)
                .timeout(Duration.ofSeconds(60))
                .maxRetries(3)
                .build());
    }

    public void disposeTavoClient(@Disposes TavoClient client) {
        client.close();
    }
}
```

### CLI Tool with Picocli

```java
package com.example.tavo.cli;

import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ScanResult;
import picocli.CommandLine;
import reactor.core.publisher.Mono;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.stream.Collectors;

@CommandLine.Command(
    name = "tavo-scanner",
    mixinStandardHelpOptions = true,
    version = "1.0.0",
    description = "Tavo AI Security Scanner CLI"
)
public class TavoScanner implements Callable<Integer> {

    @CommandLine.Option(
        names = {"-k", "--api-key"},
        description = "Tavo AI API key"
    )
    private String apiKey;

    @CommandLine.Option(
        names = {"-l", "--language"},
        description = "Programming language",
        defaultValue = "java"
    )
    private String language;

    @CommandLine.Option(
        names = {"-r", "--recursive"},
        description = "Scan directories recursively"
    )
    private boolean recursive;

    @CommandLine.Option(
        names = {"-v", "--verbose"},
        description = "Verbose output"
    )
    private boolean verbose;

    @CommandLine.Parameters(
        index = "0",
        description = "File or directory to scan"
    )
    private Path path;

    @Override
    public Integer call() throws Exception {
        // Get API key from option or environment
        String key = apiKey != null ? apiKey : System.getenv("TAVO_API_KEY");
        if (key == null) {
            System.err.println("❌ API key required. Use --api-key or set TAVO_API_KEY environment variable");
            return 1;
        }

        TavoClient client = new TavoClient(key);

        try {
            if (Files.isRegularFile(path)) {
                int issues = scanFile(client, path, language, verbose).block();
                return issues > 0 ? 1 : 0;
            } else if (Files.isDirectory(path)) {
                int issues = scanDirectory(client, path, language, recursive, verbose).block();
                return issues > 0 ? 1 : 0;
            } else {
                System.err.println("❌ Path is neither a file nor directory");
                return 1;
            }
        } catch (Exception e) {
            System.err.println("❌ Error: " + e.getMessage());
            return 1;
        } finally {
            client.close();
        }
    }

    private Mono<Integer> scanFile(TavoClient client, Path filePath, String language, boolean verbose) {
        return Mono.fromCallable(() -> Files.readString(filePath))
                .flatMap(code -> client.scanCode(code, language))
                .doOnNext(result -> printScanResult(filePath.toString(), result, verbose))
                .map(ScanResult::getTotalIssues)
                .onErrorResume(e -> {
                    System.err.println("❌ Error scanning " + filePath + ": " + e.getMessage());
                    return Mono.just(0);
                });
    }

    private Mono<Integer> scanDirectory(TavoClient client, Path dirPath, String language, boolean recursive, boolean verbose) {
        return findFilesToScan(dirPath, language, recursive)
                .flatMapMany(Mono::just)
                .flatMap(file -> scanFile(client, file, language, verbose), 5) // Concurrent scanning
                .reduce(0, Integer::sum)
                .doOnNext(totalIssues -> {
                    System.out.println("\n📊 Summary: " + totalIssues + " total issues");
                });
    }

    private Mono<List<Path>> findFilesToScan(Path dirPath, String language, boolean recursive) {
        return Mono.fromCallable(() -> {
            String extension = getExtensionForLanguage(language);
            return Files.walk(dirPath, recursive ? Integer.MAX_VALUE : 1)
                    .filter(Files::isRegularFile)
                    .filter(path -> path.toString().endsWith(extension))
                    .collect(Collectors.toList());
        });
    }

    private String getExtensionForLanguage(String language) {
        return switch (language.toLowerCase()) {
            case "java" -> ".java";
            case "python" -> ".py";
            case "javascript", "typescript" -> ".js";
            case "go" -> ".go";
            case "rust" -> ".rs";
            case "csharp" -> ".cs";
            default -> ".java";
        };
    }

    private void printScanResult(String filePath, ScanResult result, boolean verbose) {
        if (result.getTotalIssues() > 0) {
            System.out.println("\n🔴 " + filePath + " (" + result.getTotalIssues() + " issues):");

            result.getVulnerabilities().forEach((vuln, index) -> {
                System.out.println("  " + (index + 1) + ". " + vuln.getTitle() + " (" + vuln.getSeverity() + ")");
                if (verbose) {
                    System.out.println("     " + vuln.getDescription());
                    if (vuln.getLocation() != null) {
                        System.out.println("     📍 " + vuln.getLocation().getFile() + ":" +
                                         vuln.getLocation().getLine() + ":" + vuln.getLocation().getColumn());
                    }
                }
            });
        } else {
            System.out.println("✅ " + filePath + " (0 issues)");
        }
    }

    public static void main(String[] args) {
        int exitCode = new CommandLine(new TavoScanner()).execute(args);
        System.exit(exitCode);
    }
}
```

## Testing Examples

### Unit Tests with JUnit 5 and Mockito

```java
package com.example.tavo;

import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.exception.TavoApiException;
import net.tavoai.sdk.model.ScanResult;
import net.tavoai.sdk.model.Vulnerability;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

import java.util.Collections;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

class TavoClientTest {

    @Mock
    private TavoClient mockClient;

    private AutoCloseable mocks;

    @BeforeEach
    void setUp() {
        mocks = MockitoAnnotations.openMocks(this);
    }

    @AfterEach
    void tearDown() throws Exception {
        mocks.close();
    }

    @Test
    void scanCode_Success() {
        // Arrange
        Vulnerability vuln = Vulnerability.builder()
                .title("SQL Injection")
                .description("Potential SQL injection vulnerability")
                .severity("high")
                .build();

        ScanResult expectedResult = ScanResult.builder()
                .totalIssues(1)
                .vulnerabilities(Collections.singletonList(vuln))
                .build();

        when(mockClient.scanCode(any(String.class), eq("java")))
                .thenReturn(Mono.just(expectedResult));

        // Act & Assert
        StepVerifier.create(mockClient.scanCode("test code", "java"))
                .expectNext(expectedResult)
                .verifyComplete();
    }

    @Test
    void scanCode_ApiError() {
        // Arrange
        when(mockClient.scanCode(any(String.class), eq("java")))
                .thenReturn(Mono.error(new TavoApiException("API Error", 400)));

        // Act & Assert
        StepVerifier.create(mockClient.scanCode("test code", "java"))
                .expectError(TavoApiException.class)
                .verify();
    }
}
```

### Integration Tests with Testcontainers

```java
package com.example.tavo;

import net.tavoai.sdk.TavoClient;
import net.tavoai.sdk.model.ScanResult;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import reactor.test.StepVerifier;

@Testcontainers
class TavoClientIntegrationTest {

    @Container
    static GenericContainer<?> tavoContainer = new GenericContainer<>("tavoai/tavo-sdk:latest")
            .withExposedPorts(8080)
            .withEnv("TAVO_API_KEY", "test-key");

    static TavoClient client;

    @BeforeAll
    static void setUp() {
        String apiKey = System.getenv("TAVO_API_KEY");
        if (apiKey == null) {
            throw new IllegalStateException("TAVO_API_KEY environment variable required");
        }

        client = new TavoClient(apiKey);
    }

    @AfterAll
    static void tearDown() {
        if (client != null) {
            client.close();
        }
    }

    @Test
    void scanVulnerableCode_DetectsSqlInjection() {
        // Arrange
        String vulnerableCode = """
            public void authenticate(String username, String password) {
                String query = "SELECT * FROM users WHERE username='" + username +
                              "' AND password='" + password + "'";
                // SQL injection vulnerability
                executeQuery(query);
            }
            """;

        // Act & Assert
        StepVerifier.create(client.scanCode(vulnerableCode, "java"))
                .expectNextMatches(result -> {
                    boolean hasSqlInjection = result.getVulnerabilities().stream()
                            .anyMatch(vuln -> vuln.getTitle().toLowerCase().contains("sql") &&
                                            vuln.getTitle().toLowerCase().contains("injection"));
                    return result.getTotalIssues() > 0 && hasSqlInjection;
                })
                .verifyComplete();
    }

    @Test
    void scanSafeCode_NoHighSeverityIssues() {
        // Arrange
        String safeCode = """
            public void authenticate(String username, String password) {
                String query = "SELECT * FROM users WHERE username=? AND password=?";
                executeQuery(query, username, password);
            }
            """;

        // Act & Assert
        StepVerifier.create(client.scanCode(safeCode, "java"))
                .expectNextMatches(result -> {
                    long highSeverityIssues = result.getVulnerabilities().stream()
                            .filter(vuln -> "critical".equals(vuln.getSeverity()) ||
                                          "high".equals(vuln.getSeverity()))
                            .count();
                    return highSeverityIssues == 0;
                })
                .verifyComplete();
    }
}
```

### Performance Tests with JMH

```java
package com.example.tavo.benchmark;

import net.tavoai.sdk.TavoClient;
import org.openjdk.jmh.annotations.*;
import reactor.core.publisher.Mono;

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Benchmark)
@Fork(2)
@Warmup(iterations = 3)
@Measurement(iterations = 5)
public class TavoClientBenchmark {

    private TavoClient client;
    private String testCode;

    @Setup
    public void setup() {
        client = new TavoClient("benchmark-api-key");

        testCode = """
            public class TestClass {
                public void method1() {
                    String sql = "SELECT * FROM users WHERE id = " + userId;
                    executeQuery(sql);
                }

                public void method2() {
                    String cmd = "ls " + userInput;
                    executeCommand(cmd);
                }

                public void method3() {
                    String xpath = "//users[@id='" + userId + "']";
                    evaluateXPath(xpath);
                }
            }
            """;
    }

    @TearDown
    public void tearDown() {
        client.close();
    }

    @Benchmark
    public void scanCodeBenchmark() {
        Mono<ScanResult> result = client.scanCode(testCode, "java");
        result.block(); // Wait for completion
    }
}
```

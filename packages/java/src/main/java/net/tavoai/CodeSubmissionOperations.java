package net.tavoai;

import okhttp3.*;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.file.Files;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;

/**
 * Code submission operations for CLI tools and scanners.
 */
public class CodeSubmissionOperations {
    private static final String CODE_ENDPOINT = "/code";
    private static final MediaType JSON = MediaType.get("application/json; charset=utf-8");

    private final TavoClient client;
    private final Gson gson;
    private final Type mapType;

    /**
     * Constructor for CodeSubmissionOperations.
     * @param client the TavoClient instance
     */
    public CodeSubmissionOperations(TavoClient client) {
        this.client = client;
        this.gson = new Gson();
        this.mapType = new TypeToken<Map<String, Object>>(){}.getType();
    }

    /**
     * Helper method to create a new map.
     * @return a new HashMap
     */
    private Map<String, Object> createMap() {
        return new java.util.HashMap<>();
    }

    /**
     * Submit code files directly for scanning.
     * @param files list of files to submit
     * @param filenames list of corresponding filenames
     * @param repositoryName optional repository name
     * @param branch optional branch
     * @param commitSha optional commit SHA
     * @param scanConfig optional scan configuration
     * @return submission response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> submitCode(List<File> files, List<String> filenames, String repositoryName, String branch, String commitSha, Map<String, Object> scanConfig) throws TavoException {
        try {
            MultipartBody.Builder multipartBuilder = new MultipartBody.Builder()
                    .setType(MultipartBody.FORM);

            // Add files
            for (int i = 0; i < files.size(); i++) {
                File file = files.get(i);
                String filename = i < filenames.size() ? filenames.get(i) : file.getName();
                String mimeType = Files.probeContentType(file.toPath());
                if (mimeType == null) mimeType = "application/octet-stream";

                RequestBody fileBody = RequestBody.create(file, MediaType.parse(mimeType));
                multipartBuilder.addFormDataPart("files", filename, fileBody);
            }

            // Add optional parameters
            if (repositoryName != null) multipartBuilder.addFormDataPart("repository_name", repositoryName);
            if (branch != null) multipartBuilder.addFormDataPart("branch", branch);
            if (commitSha != null) multipartBuilder.addFormDataPart("commit_sha", commitSha);
            if (scanConfig != null) multipartBuilder.addFormDataPart("scan_config", gson.toJson(scanConfig));

            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/code/submit/code")
                    .post(multipartBuilder.build())
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to submit code for scanning", e);
        }
    }

    /**
     * Submit repository snapshot for scanning.
     * @param repositoryUrl repository URL or identifier
     * @param snapshotData repository snapshot data
     * @param branch optional branch
     * @param commitSha optional commit SHA
     * @param scanConfig optional scan configuration
     * @return submission response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> submitRepository(String repositoryUrl, Map<String, Object> snapshotData, String branch, String commitSha, Map<String, Object> scanConfig) throws TavoException {
        try {
            Map<String, Object> requestBody = createMap();
            requestBody.put("repository_url", repositoryUrl);
            requestBody.put("snapshot_data", snapshotData);
            if (branch != null) requestBody.put("branch", branch);
            if (commitSha != null) requestBody.put("commit_sha", commitSha);
            if (scanConfig != null) requestBody.put("scan_config", scanConfig);

            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/code/submit/repository")
                    .post(RequestBody.create(gson.toJson(requestBody), JSON))
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to submit repository snapshot", e);
        }
    }

    /**
     * Submit code snippet for targeted analysis.
     * @param codeContent the code content to analyze
     * @param language programming language
     * @param analysisType optional analysis type
     * @param rules optional specific rules to apply
     * @param plugins optional plugins to use
     * @param context optional additional context
     * @return analysis response
     * @throws TavoException if the request fails
     */
    public Map<String, Object> submitAnalysis(String codeContent, String language, String analysisType, List<String> rules, List<String> plugins, Map<String, Object> context) throws TavoException {
        try {
            Map<String, Object> requestBody = createMap();
            requestBody.put("code_content", codeContent);
            requestBody.put("language", language);
            if (analysisType != null) requestBody.put("analysis_type", analysisType);
            if (rules != null) requestBody.put("rules", rules);
            if (plugins != null) requestBody.put("plugins", plugins);
            if (context != null) requestBody.put("context", context);

            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/code/submit/analysis")
                    .post(RequestBody.create(gson.toJson(requestBody), JSON))
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to submit code analysis request", e);
        }
    }

    /**
     * Get scan status (CLI-optimized).
     * @param scanId the scan ID
     * @return scan status
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getScanStatus(String scanId) throws TavoException {
        try {
            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/code/scans/" + scanId + "/status")
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to get scan status", e);
        }
    }

    /**
     * Get scan results summary (CLI-optimized).
     * @param scanId the scan ID
     * @return scan results summary
     * @throws TavoException if the request fails
     */
    public Map<String, Object> getScanResults(String scanId) throws TavoException {
        try {
            Request request = new Request.Builder()
                    .url(client.getBaseUrl() + "/code/scans/" + scanId + "/results/summary")
                    .get()
                    .build();

            return executeRequest(request, mapType);
        } catch (IOException e) {
            throw new TavoException("Failed to get scan results summary", e);
        }
    }

    // ===========================================
    // Async Operations with CompletableFuture
    // ===========================================

    /**
     * Submit code asynchronously.
     * @param files list of files to submit
     * @param filenames list of filenames
     * @param repositoryName optional repository name
     * @param branch optional branch
     * @param commitSha optional commit SHA
     * @param scanConfig optional scan configuration
     * @return CompletableFuture with submission response
     */
    public CompletableFuture<Map<String, Object>> submitCodeAsync(List<File> files, List<String> filenames, String repositoryName, String branch, String commitSha, Map<String, Object> scanConfig) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return submitCode(files, filenames, repositoryName, branch, commitSha, scanConfig);
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Submit repository asynchronously.
     * @param repositoryURL repository URL or identifier
     * @param snapshotData repository snapshot data
     * @param branch optional branch
     * @param commitSha optional commit SHA
     * @param scanConfig optional scan configuration
     * @return CompletableFuture with submission response
     */
    public CompletableFuture<Map<String, Object>> submitRepositoryAsync(String repositoryURL, Map<String, Object> snapshotData, String branch, String commitSha, Map<String, Object> scanConfig) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return submitRepository(repositoryURL, snapshotData, branch, commitSha, scanConfig);
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Submit analysis asynchronously.
     * @param codeContent the code content to analyze
     * @param language programming language
     * @param analysisType optional analysis type
     * @param rules optional specific rules to apply
     * @param plugins optional plugins to use
     * @param context optional additional context
     * @return CompletableFuture with analysis response
     */
    public CompletableFuture<Map<String, Object>> submitAnalysisAsync(String codeContent, String language, String analysisType, List<String> rules, List<String> plugins, Map<String, Object> context) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return submitAnalysis(codeContent, language, analysisType, rules, plugins, context);
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Get scan status asynchronously (CLI-optimized).
     * @param scanId the scan ID
     * @return CompletableFuture with scan status
     */
    public CompletableFuture<Map<String, Object>> getScanStatusAsync(String scanId) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return getScanStatus(scanId);
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }

    /**
     * Get scan results asynchronously (CLI-optimized).
     * @param scanId the scan ID
     * @return CompletableFuture with scan results summary
     */
    public CompletableFuture<Map<String, Object>> getScanResultsAsync(String scanId) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return getScanResults(scanId);
            } catch (TavoException e) {
                throw new CompletionException(e);
            }
        });
    }
}

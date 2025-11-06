package net.tavoai.sdk;

import okhttp3.*;
import com.google.gson.Gson;
import java.util.concurrent.CompletableFuture;
import java.util.Map;
import java.util.HashMap;

/**
 * Client for code_submission endpoints
 */
public class CodeSubmissionClient {
    private final OkHttpClient httpClient;
    private final String baseUrl;
    private final Gson gson = new Gson();

    public CodeSubmissionClient(OkHttpClient httpClient, String baseUrl) {
        this.httpClient = httpClient;
        this.baseUrl = baseUrl;
    }

{methods_str}
}}

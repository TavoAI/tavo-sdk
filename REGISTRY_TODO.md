# SDK - Universal Security Tool Registry Support

**Project**: TavoAI SDK (Python & JavaScript)  
**Initiative**: Universal Security Tool Registry  
**Status**: 📋 Planning Phase  
**Owner**: SDK Team  

---

## Overview

This document details the implementation tasks for adding Registry support to both Python, Java, and JavaScript SDKs at a minimum. The SDKs will provide programmatic access to:

1. Registry marketplace browsing and search
2. Bundle download and installation
3. Rule execution (local and cloud)
4. Rating and review management
5. Usage tracking and cost monitoring

**Reference**: See `../architecting/REGISTRY_PLAN.md` for complete architecture.

---

## Python SDK Implementation

### Phase 1: Registry Client Module (Week 10 - 1 week)

#### Task 1.1: Registry Client Class
**File**: `python/tavoai/registry_client.py`

Create main registry client class:

```python
from typing import List, Optional, Dict, Any
from .models import (
    ArtifactBundle,
    BundleDetail,
    BundleInstallation,
    ArtifactExecution,
    BundleRating,
    BundleReview,
    MarketplaceFilters,
    ExecutionRequest,
)

class RegistryClient:
    """Client for TavoAI Universal Security Tool Registry"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.tavoai.com"):
        self.api_key = api_key
        self.base_url = base_url
        self._session = self._create_session()
    
    # Marketplace
    def browse_marketplace(
        self,
        artifact_type: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        pricing_tier: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> Dict[str, Any]:
        """Browse marketplace with filters"""
        pass
    
    def get_bundle(self, bundle_id: str) -> BundleDetail:
        """Get bundle details"""
        pass
    
    def get_categories(self) -> List[str]:
        """Get available categories"""
        pass
    
    # Bundle management
    def create_bundle(self, bundle_data: Dict[str, Any]) -> ArtifactBundle:
        """Create a new bundle"""
        pass
    
    def update_bundle(
        self, bundle_id: str, bundle_data: Dict[str, Any]
    ) -> ArtifactBundle:
        """Update existing bundle"""
        pass
    
    def delete_bundle(self, bundle_id: str) -> None:
        """Delete bundle"""
        pass
    
    def publish_bundle(self, bundle_id: str) -> ArtifactBundle:
        """Publish bundle to marketplace"""
        pass
    
    # Installation & downloads
    def download_bundle(self, bundle_id: str, output_path: str) -> str:
        """Download bundle as .tavoai-bundle file"""
        pass
    
    def install_bundle(self, bundle_id: str) -> BundleInstallation:
        """Install bundle to user's account"""
        pass
    
    def get_my_bundles(self) -> List[ArtifactBundle]:
        """Get user's installed bundles"""
        pass
    
    # Execution
    def execute_code_rule(
        self,
        rule_id: str,
        code: str,
        language: str,
        file_path: Optional[str] = None,
        execution_mode: str = "cloud",
    ) -> ArtifactExecution:
        """Execute code analysis rule"""
        pass
    
    def get_execution(self, execution_id: str) -> ArtifactExecution:
        """Get execution details"""
        pass
    
    def get_my_executions(
        self,
        page: int = 1,
        per_page: int = 20,
        artifact_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get user's execution history"""
        pass
    
    # Ratings & reviews
    def rate_bundle(self, bundle_id: str, rating: int) -> BundleRating:
        """Rate a bundle (1-5 stars)"""
        pass
    
    def review_bundle(
        self, bundle_id: str, review_text: str, rating: int
    ) -> BundleReview:
        """Review a bundle"""
        pass
    
    def get_reviews(
        self, bundle_id: str, page: int = 1, per_page: int = 20
    ) -> Dict[str, Any]:
        """Get bundle reviews"""
        pass
```

**Dependencies**:
- `requests` or `httpx` for HTTP client
- Existing SDK authentication

**Testing**:
- Unit tests with mocked API responses
- Integration tests with real API
- Error handling tests (401, 404, 500)

**Acceptance Criteria**:
- [ ] All methods implemented
- [ ] Proper error handling
- [ ] Type hints complete
- [ ] Docstrings for all public methods
- [ ] Works with API key authentication

---

#### Task 1.2: Data Models
**File**: `python/tavoai/models/registry.py`

Create Pydantic models for registry objects:

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ArtifactType(str, Enum):
    CODE_RULE = "code_rule"
    PROXY_RULE = "proxy_rule"
    ZAP_ATTACK = "zap_attack"
    POLICY = "policy"

class PricingTier(str, Enum):
    FREE = "free"
    PAID = "paid"
    ENTERPRISE = "enterprise"

class ArtifactBundle(BaseModel):
    id: str
    name: str
    description: str
    version: str
    artifact_type: ArtifactType
    category: str
    pricing_tier: PricingTier
    organization_id: str
    is_official: bool
    rating: float
    download_count: int
    created_at: datetime

class BundleDetail(ArtifactBundle):
    artifacts: List[Dict[str, Any]]
    reviews_count: int
    changelog: Optional[str]
    readme: Optional[str]

class ArtifactExecution(BaseModel):
    id: str
    artifact_id: str
    artifact_type: ArtifactType
    status: str
    execution_mode: str
    tokens_used: Optional[int]
    cost_usd: Optional[float]
    result: Dict[str, Any]
    created_at: datetime

class BundleRating(BaseModel):
    id: str
    bundle_id: str
    user_id: str
    rating: int
    created_at: datetime

class BundleReview(BaseModel):
    id: str
    bundle_id: str
    user_id: str
    rating: int
    review_text: str
    created_at: datetime
```

**Dependencies**:
- Pydantic 2.0+

**Testing**:
- Model validation tests
- Serialization/deserialization tests

**Acceptance Criteria**:
- [ ] All models defined
- [ ] Validation works
- [ ] JSON serialization works

---

#### Task 1.3: Local Bundle Manager
**File**: `python/tavoai/local_bundle_manager.py`

Create local bundle management:

```python
import os
import zipfile
import json
from pathlib import Path
from typing import Optional

class LocalBundleManager:
    """Manage locally downloaded bundles"""
    
    def __init__(self, bundles_dir: Optional[str] = None):
        self.bundles_dir = bundles_dir or self._get_default_bundles_dir()
        os.makedirs(self.bundles_dir, exist_ok=True)
    
    def _get_default_bundles_dir(self) -> str:
        """Get default bundles directory (~/.tavoai/bundles)"""
        return os.path.join(os.path.expanduser("~"), ".tavoai", "bundles")
    
    def install_from_file(self, bundle_path: str) -> Dict[str, Any]:
        """Install bundle from .tavoai-bundle file"""
        # Extract ZIP
        # Parse manifest.json
        # Install artifacts
        # Return installation info
        pass
    
    def list_installed(self) -> List[Dict[str, Any]]:
        """List installed bundles"""
        pass
    
    def get_bundle(self, bundle_id: str) -> Optional[Dict[str, Any]]:
        """Get installed bundle"""
        pass
    
    def uninstall(self, bundle_id: str) -> None:
        """Uninstall bundle"""
        pass
    
    def check_updates(self) -> List[Dict[str, Any]]:
        """Check for bundle updates"""
        pass
```

**Dependencies**:
- Python standard library (zipfile, json, pathlib)

**Testing**:
- Test bundle installation
- Test bundle listing
- Test uninstallation
- Test update checking

**Acceptance Criteria**:
- [ ] Can install from ZIP file
- [ ] Bundles stored in user directory
- [ ] Can list and manage bundles
- [ ] Update checking works

---

#### Task 1.4: Usage Tracking Helper
**File**: `python/tavoai/usage_tracker.py`

Create usage tracking helper:

```python
class UsageTracker:
    """Track registry usage for cost monitoring"""
    
    def __init__(self, registry_client: RegistryClient):
        self.client = registry_client
    
    def get_current_usage(self, period: str = "month") -> Dict[str, Any]:
        """Get current usage statistics"""
        # Query executions
        # Calculate totals
        return {
            "executions": 150,
            "tokens_used": 50000,
            "cost_usd": 1.50,
            "budget_remaining": 8.50,
        }
    
    def get_cost_breakdown(self) -> Dict[str, Any]:
        """Get cost breakdown by model"""
        pass
    
    def set_budget_alert(self, threshold_usd: float) -> None:
        """Set budget alert threshold"""
        pass
```

**Dependencies**:
- Task 1.1

**Testing**:
- Test usage calculation
- Test cost breakdown
- Test budget alerts

**Acceptance Criteria**:
- [ ] Usage tracking accurate
- [ ] Cost calculations correct
- [ ] Budget alerts configurable

---

### Python SDK Testing

**Location**: `python/tests/test_registry_client.py`

Required tests:
```python
def test_browse_marketplace():
    # Test marketplace browsing with filters
    pass

def test_get_bundle():
    # Test bundle retrieval
    pass

def test_execute_code_rule():
    # Test rule execution
    pass

def test_rate_bundle():
    # Test bundle rating
    pass

def test_local_bundle_install():
    # Test local bundle installation
    pass

def test_usage_tracking():
    # Test usage tracking
    pass
```

**Coverage Target**: 80%

---

## JavaScript/TypeScript SDK Implementation

### Phase 1: Registry Client Module (Week 10 - 1 week)

#### Task 2.1: Registry Client Class
**File**: `javascript/src/registryClient.ts`

Create TypeScript registry client:

```typescript
import { AxiosInstance } from 'axios';

export interface MarketplaceFilters {
  artifactType?: ArtifactType;
  category?: string;
  tags?: string[];
  pricingTier?: PricingTier;
  search?: string;
  page?: number;
  perPage?: number;
}

export interface ExecutionRequest {
  ruleId: string;
  code: string;
  language: string;
  filePath?: string;
  executionMode?: 'cloud' | 'local';
}

export class RegistryClient {
  private client: AxiosInstance;
  
  constructor(apiKey: string, baseUrl = 'https://api.tavoai.com') {
    this.client = this.createClient(apiKey, baseUrl);
  }
  
  // Marketplace
  async browseMarketplace(filters: MarketplaceFilters): Promise<PaginatedResponse<ArtifactBundle>> {
    const response = await this.client.get('/api/v1/registry/marketplace', {
      params: filters,
    });
    return response.data;
  }
  
  async getBundle(bundleId: string): Promise<BundleDetail> {
    const response = await this.client.get(`/api/v1/registry/bundles/${bundleId}`);
    return response.data;
  }
  
  async getCategories(): Promise<string[]> {
    const response = await this.client.get('/api/v1/registry/categories');
    return response.data;
  }
  
  // Bundle management
  async createBundle(bundleData: BundleCreate): Promise<ArtifactBundle> {
    const response = await this.client.post('/api/v1/registry/bundles', bundleData);
    return response.data;
  }
  
  async updateBundle(bundleId: string, bundleData: BundleUpdate): Promise<ArtifactBundle> {
    const response = await this.client.put(
      `/api/v1/registry/bundles/${bundleId}`,
      bundleData
    );
    return response.data;
  }
  
  async deleteBundle(bundleId: string): Promise<void> {
    await this.client.delete(`/api/v1/registry/bundles/${bundleId}`);
  }
  
  async publishBundle(bundleId: string): Promise<ArtifactBundle> {
    const response = await this.client.post(
      `/api/v1/registry/bundles/${bundleId}/publish`
    );
    return response.data;
  }
  
  // Installation & downloads
  async downloadBundle(bundleId: string): Promise<Blob> {
    const response = await this.client.get(
      `/api/v1/registry/bundles/${bundleId}/download`,
      { responseType: 'blob' }
    );
    return response.data;
  }
  
  async installBundle(bundleId: string): Promise<BundleInstallation> {
    const response = await this.client.post(
      `/api/v1/registry/bundles/${bundleId}/install`
    );
    return response.data;
  }
  
  async getMyBundles(): Promise<ArtifactBundle[]> {
    const response = await this.client.get('/api/v1/registry/my-bundles');
    return response.data;
  }
  
  // Execution
  async executeCodeRule(request: ExecutionRequest): Promise<ArtifactExecution> {
    const response = await this.client.post(
      '/api/v1/registry/execute/code-rule',
      request
    );
    return response.data;
  }
  
  async getExecution(executionId: string): Promise<ArtifactExecution> {
    const response = await this.client.get(
      `/api/v1/registry/executions/${executionId}`
    );
    return response.data;
  }
  
  async getMyExecutions(filters?: {
    page?: number;
    perPage?: number;
    artifactType?: ArtifactType;
  }): Promise<PaginatedResponse<ArtifactExecution>> {
    const response = await this.client.get('/api/v1/registry/my-executions', {
      params: filters,
    });
    return response.data;
  }
  
  // Ratings & reviews
  async rateBundle(bundleId: string, rating: number): Promise<BundleRating> {
    const response = await this.client.post(
      `/api/v1/registry/bundles/${bundleId}/rate`,
      { rating }
    );
    return response.data;
  }
  
  async reviewBundle(
    bundleId: string,
    reviewText: string,
    rating: number
  ): Promise<BundleReview> {
    const response = await this.client.post(
      `/api/v1/registry/bundles/${bundleId}/review`,
      { review_text: reviewText, rating }
    );
    return response.data;
  }
  
  async getReviews(
    bundleId: string,
    page = 1,
    perPage = 20
  ): Promise<PaginatedResponse<BundleReview>> {
    const response = await this.client.get(
      `/api/v1/registry/bundles/${bundleId}/reviews`,
      { params: { page, per_page: perPage } }
    );
    return response.data;
  }
}
```

**Dependencies**:
- `axios` for HTTP client
- Existing SDK authentication

**Testing**:
- Jest unit tests with mocked responses
- Integration tests with real API

**Acceptance Criteria**:
- [ ] All methods implemented
- [ ] TypeScript types complete
- [ ] Error handling
- [ ] JSDoc comments

---

#### Task 2.2: TypeScript Type Definitions
**File**: `javascript/src/types/registry.ts`

Create TypeScript types:

```typescript
export enum ArtifactType {
  CODE_RULE = 'code_rule',
  PROXY_RULE = 'proxy_rule',
  ZAP_ATTACK = 'zap_attack',
  POLICY = 'policy',
}

export enum PricingTier {
  FREE = 'free',
  PAID = 'paid',
  ENTERPRISE = 'enterprise',
}

export interface ArtifactBundle {
  id: string;
  name: string;
  description: string;
  version: string;
  artifactType: ArtifactType;
  category: string;
  pricingTier: PricingTier;
  organizationId: string;
  isOfficial: boolean;
  rating: number;
  downloadCount: number;
  createdAt: string;
}

export interface BundleDetail extends ArtifactBundle {
  artifacts: any[];
  reviewsCount: number;
  changelog?: string;
  readme?: string;
}

export interface ArtifactExecution {
  id: string;
  artifactId: string;
  artifactType: ArtifactType;
  status: string;
  executionMode: 'cloud' | 'local';
  tokensUsed?: number;
  costUsd?: number;
  result: Record<string, any>;
  createdAt: string;
}

export interface BundleRating {
  id: string;
  bundleId: string;
  userId: string;
  rating: number;
  createdAt: string;
}

export interface BundleReview {
  id: string;
  bundleId: string;
  userId: string;
  rating: number;
  reviewText: string;
  createdAt: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  perPage: number;
  pages: number;
}
```

**Dependencies**:
- TypeScript 5.0+

**Testing**:
- Type checking tests
- JSON serialization tests

**Acceptance Criteria**:
- [ ] All types defined
- [ ] Types match API responses
- [ ] No `any` types where possible

---

#### Task 2.3: Local Bundle Manager (Node.js)
**File**: `javascript/src/localBundleManager.ts`

Create local bundle management for Node.js:

```typescript
import fs from 'fs';
import path from 'path';
import AdmZip from 'adm-zip';
import os from 'os';

export class LocalBundleManager {
  private bundlesDir: string;
  
  constructor(bundlesDir?: string) {
    this.bundlesDir = bundlesDir || this.getDefaultBundlesDir();
    fs.mkdirSync(this.bundlesDir, { recursive: true });
  }
  
  private getDefaultBundlesDir(): string {
    return path.join(os.homedir(), '.tavoai', 'bundles');
  }
  
  async installFromFile(bundlePath: string): Promise<any> {
    // Extract ZIP
    // Parse manifest.json
    // Install artifacts
    const zip = new AdmZip(bundlePath);
    // ...
  }
  
  listInstalled(): any[] {
    // List installed bundles
    return [];
  }
  
  getBundle(bundleId: string): any | null {
    // Get installed bundle
    return null;
  }
  
  uninstall(bundleId: string): void {
    // Uninstall bundle
  }
  
  checkUpdates(): any[] {
    // Check for updates
    return [];
  }
}
```

**Dependencies**:
- `adm-zip` for ZIP handling
- Node.js `fs` and `path`

**Testing**:
- Test bundle installation
- Test bundle listing
- Test uninstallation

**Acceptance Criteria**:
- [ ] Works in Node.js environment
- [ ] Bundles stored locally
- [ ] Can manage bundles

---

### JavaScript SDK Testing

**Location**: `javascript/tests/registryClient.test.ts`

Required tests:
```typescript
describe('RegistryClient', () => {
  test('browseMarketplace', async () => {
    // Test marketplace browsing
  });
  
  test('getBundle', async () => {
    // Test bundle retrieval
  });
  
  test('executeCodeRule', async () => {
    // Test rule execution
  });
  
  test('rateBundle', async () => {
    // Test bundle rating
  });
  
  test('localBundleInstall', async () => {
    // Test local bundle installation
  });
});
```

**Coverage Target**: 80%

---

## Documentation

### Python SDK Documentation
**File**: `python/docs/registry.md`

Create comprehensive documentation:

```markdown
# Registry Client

## Installation

```bash
pip install tavoai-sdk
```

## Quick Start

```python
from tavoai import RegistryClient

# Initialize client
client = RegistryClient(api_key="tavo_live_...")

# Browse marketplace
bundles = client.browse_marketplace(
    category="security",
    pricing_tier="free"
)

# Get bundle details
bundle = client.get_bundle("bundle-id")

# Execute code rule
result = client.execute_code_rule(
    rule_id="rule-id",
    code="user_input = request.get('data'); llm.prompt(user_input)",
    language="python"
)
```

## API Reference
...
```

**Acceptance Criteria**:
- [ ] All methods documented
- [ ] Code examples provided
- [ ] Common use cases covered

---

### JavaScript SDK Documentation
**File**: `javascript/docs/registry.md`

Similar documentation for JavaScript SDK.

---

## Success Criteria

### Python SDK
- [ ] All registry methods implemented
- [ ] Type hints complete
- [ ] 80%+ test coverage
- [ ] Documentation complete
- [ ] Published to PyPI

### JavaScript SDK
- [ ] All registry methods implemented
- [ ] TypeScript types complete
- [ ] 80%+ test coverage
- [ ] Documentation complete
- [ ] Published to NPM

### Integration
- [ ] Works with existing authentication
- [ ] Works with dashboard API client
- [ ] Works with CLI
- [ ] Works with VSCode extension

---

## Notes

- Maintain backward compatibility with existing SDK methods
- Follow existing code style and patterns
- Update main SDK documentation to include registry features
- Coordinate with API server team for endpoint availability
- Coordinate with CLI team for SDK integration

---

**Last Updated**: October 25, 2025  
**Next Review**: After Phase 1 completion


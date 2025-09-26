---
sidebar_position: 7
---

# Angular Integration

Integrate Tavo AI security scanning into your Angular applications.

## Installation

```bash
npm install tavo-ai axios
```

## Basic Setup

### Environment Configuration

```typescript
// src/environments/environment.ts
export const environment = {
  production: false,
  tavo: {
    apiKey: 'your-api-key-here',
    baseUrl: 'https://api.tavo.ai',
    timeout: 30000,
  },
};
```

```typescript
// src/environments/environment.prod.ts
export const environment = {
  production: true,
  tavo: {
    apiKey: process.env['TAVO_API_KEY'] || 'your-production-api-key',
    baseUrl: 'https://api.tavo.ai',
    timeout: 30000,
  },
};
```

### Tavo Service

```typescript
// src/app/services/tavo.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface ScanRequest {
  name: string;
  target: string;
  scan_type: 'code' | 'web';
  language?: string;
}

export interface ScanResult {
  id: string;
  status: string;
  summary?: {
    files_scanned: number;
    vulnerabilities_found: number;
    duration: string;
  };
}

export interface ReportRequest {
  type: string;
  format: string;
  scan_ids: string[];
}

@Injectable({
  providedIn: 'root',
})
export class TavoService {
  private readonly baseUrl = environment.tavo.baseUrl;
  private readonly apiKey = environment.tavo.apiKey;

  constructor(private http: HttpClient) {}

  scanCode(code: string, language: string = 'typescript'): Observable<ScanResult> {
    const request: ScanRequest = {
      name: `Code Scan - ${language}`,
      target: code,
      scan_type: 'code',
      language: language,
    };

    return this.http
      .post<ScanResult>(`${this.baseUrl}/scans`, request, {
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
      })
      .pipe(
        map((result) => result),
        catchError(this.handleError)
      );
  }

  scanUrl(url: string): Observable<ScanResult> {
    const request: ScanRequest = {
      name: `URL Scan - ${url}`,
      target: url,
      scan_type: 'web',
    };

    return this.http
      .post<ScanResult>(`${this.baseUrl}/scans`, request, {
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
      })
      .pipe(
        map((result) => result),
        catchError(this.handleError)
      );
  }

  getScanResults(scanId: string): Observable<ScanResult> {
    return this.http
      .get<ScanResult>(`${this.baseUrl}/scans/${scanId}/results`, {
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
        },
      })
      .pipe(
        map((result) => result),
        catchError(this.handleError)
      );
  }

  generateReport(scanIds: string[], format: string = 'pdf'): Observable<any> {
    const request: ReportRequest = {
      type: 'compliance',
      format: format,
      scan_ids: scanIds,
    };

    return this.http
      .post(`${this.baseUrl}/reports`, request, {
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
        },
      })
      .pipe(
        map((result) => result),
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred';

    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Client error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = `Server error: ${error.status} - ${error.message}`;
      if (error.error?.message) {
        errorMessage += ` - ${error.error.message}`;
      }
    }

    console.error('TavoService error:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
```

## Angular Components

### Code Scanner Component

```typescript
// src/app/components/code-scanner/code-scanner.component.ts
import { Component } from '@angular/core';
import { TavoService, ScanResult } from '../../services/tavo.service';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-code-scanner',
  templateUrl: './code-scanner.component.html',
  styleUrls: ['./code-scanner.component.css'],
})
export class CodeScannerComponent {
  code = '';
  language = 'typescript';
  loading = false;
  error: string | null = null;
  scanResult: ScanResult | null = null;

  constructor(private tavoService: TavoService) {}

  onScan(): void {
    if (!this.code.trim()) {
      alert('Please enter some code to scan');
      return;
    }

    this.loading = true;
    this.error = null;
    this.scanResult = null;

    this.tavoService
      .scanCode(this.code, this.language)
      .pipe(finalize(() => (this.loading = false)))
      .subscribe({
        next: (result) => {
          this.scanResult = result;
        },
        error: (error) => {
          this.error = error.message;
        },
      });
  }

  onViewDetails(scanId: string): void {
    this.tavoService.getScanResults(scanId).subscribe({
      next: (result) => {
        this.scanResult = result;
      },
      error: (error) => {
        this.error = `Failed to get detailed results: ${error.message}`;
      },
    });
  }
}
```

```html
<!-- src/app/components/code-scanner/code-scanner.component.html -->
<div class="bg-white rounded-lg shadow-md p-6">
  <h2 class="text-2xl font-semibold mb-4">Code Security Scan</h2>

  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-2">
      Programming Language
    </label>
    <select
      [(ngModel)]="language"
      class="w-full p-2 border border-gray-300 rounded-md"
    >
      <option value="typescript">TypeScript</option>
      <option value="javascript">JavaScript</option>
      <option value="python">Python</option>
      <option value="java">Java</option>
      <option value="go">Go</option>
    </select>
  </div>

  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-2">
      Code to Scan
    </label>
    <textarea
      [(ngModel)]="code"
      rows="10"
      class="w-full p-2 border border-gray-300 rounded-md font-mono text-sm"
      placeholder="Paste your code here..."
    ></textarea>
  </div>

  <button
    (click)="onScan()"
    [disabled]="loading || !code.trim()"
    class="bg-blue-500 hover:bg-blue-700 disabled:bg-blue-300 text-white font-bold py-2 px-4 rounded"
  >
    {{ loading ? 'Scanning...' : 'Scan Code' }}
  </button>

  <div *ngIf="error" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
    Error: {{ error }}
  </div>

  <app-scan-result-display
    *ngIf="scanResult"
    [result]="scanResult"
    (viewDetails)="onViewDetails($event)"
  ></app-scan-result-display>
</div>
```

```css
/* src/app/components/code-scanner/code-scanner.component.css */
:host {
  display: block;
}
```

### URL Scanner Component

```typescript
// src/app/components/url-scanner/url-scanner.component.ts
import { Component } from '@angular/core';
import { TavoService, ScanResult } from '../../services/tavo.service';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-url-scanner',
  templateUrl: './url-scanner.component.html',
  styleUrls: ['./url-scanner.component.css'],
})
export class UrlScannerComponent {
  url = '';
  loading = false;
  error: string | null = null;
  scanResult: ScanResult | null = null;

  constructor(private tavoService: TavoService) {}

  get isValidUrl(): boolean {
    try {
      new URL(this.url);
      return true;
    } catch {
      return false;
    }
  }

  onScan(): void {
    if (!this.url.trim()) {
      alert('Please enter a URL to scan');
      return;
    }

    if (!this.isValidUrl) {
      alert('Please enter a valid URL');
      return;
    }

    this.loading = true;
    this.error = null;
    this.scanResult = null;

    this.tavoService
      .scanUrl(this.url)
      .pipe(finalize(() => (this.loading = false)))
      .subscribe({
        next: (result) => {
          this.scanResult = result;
        },
        error: (error) => {
          this.error = error.message;
        },
      });
  }

  onViewDetails(scanId: string): void {
    this.tavoService.getScanResults(scanId).subscribe({
      next: (result) => {
        this.scanResult = result;
      },
      error: (error) => {
        this.error = `Failed to get detailed results: ${error.message}`;
      },
    });
  }
}
```

```html
<!-- src/app/components/url-scanner/url-scanner.component.html -->
<div class="bg-white rounded-lg shadow-md p-6">
  <h2 class="text-2xl font-semibold mb-4">URL Security Scan</h2>

  <div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 mb-2">
      URL to Scan
    </label>
    <input
      type="url"
      [(ngModel)]="url"
      class="w-full p-2 border border-gray-300 rounded-md"
      placeholder="https://example.com"
    >
    <p *ngIf="url && !isValidUrl" class="text-red-500 text-sm mt-1">
      Please enter a valid URL
    </p>
  </div>

  <button
    (click)="onScan()"
    [disabled]="loading || !isValidUrl"
    class="bg-blue-500 hover:bg-blue-700 disabled:bg-blue-300 text-white font-bold py-2 px-4 rounded"
  >
    {{ loading ? 'Scanning...' : 'Scan URL' }}
  </button>

  <div *ngIf="error" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
    Error: {{ error }}
  </div>

  <app-scan-result-display
    *ngIf="scanResult"
    [result]="scanResult"
    (viewDetails)="onViewDetails($event)"
  ></app-scan-result-display>
</div>
```

### Scan Result Display Component

```typescript
// src/app/components/scan-result-display/scan-result-display.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ScanResult } from '../../services/tavo.service';

@Component({
  selector: 'app-scan-result-display',
  templateUrl: './scan-result-display.component.html',
  styleUrls: ['./scan-result-display.component.css'],
})
export class ScanResultDisplayComponent {
  @Input() result!: ScanResult;
  @Output() viewDetails = new EventEmitter<string>();

  onViewDetailsClick(): void {
    this.viewDetails.emit(this.result.id);
  }
}
```

```html
<!-- src/app/components/scan-result-display/scan-result-display.component.html -->
<div class="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
  <h3 class="text-lg font-semibold text-green-800 mb-2">Scan Successful</h3>

  <div class="grid grid-cols-2 gap-4 mb-4">
    <div>
      <span class="font-medium">Scan ID:</span> {{ result.id }}
    </div>
    <div>
      <span class="font-medium">Status:</span>
      <span
        class="ml-2 px-2 py-1 rounded text-sm"
        [ngClass]="{
          'bg-green-100 text-green-800': result.status === 'completed',
          'bg-yellow-100 text-yellow-800': result.status === 'running',
          'bg-red-100 text-red-800': result.status === 'failed'
        }"
      >
        {{ result.status }}
      </span>
    </div>
  </div>

  <div *ngIf="result.summary" class="mb-4">
    <h4 class="font-semibold mb-2">Summary:</h4>
    <ul class="list-disc list-inside text-sm space-y-1">
      <li>Files scanned: {{ result.summary.files_scanned || 0 }}</li>
      <li>Vulnerabilities found: {{ result.summary.vulnerabilities_found || 0 }}</li>
      <li>Scan duration: {{ result.summary.duration || 'N/A' }}</li>
    </ul>
  </div>

  <button
    (click)="onViewDetailsClick()"
    class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
  >
    View Detailed Results
  </button>
</div>
```

## NgRx State Management

### Actions

```typescript
// src/app/store/tavo.actions.ts
import { createAction, props } from '@ngrx/store';
import { ScanResult } from '../services/tavo.service';

export const scanCode = createAction(
  '[Tavo] Scan Code',
  props<{ code: string; language: string }>()
);

export const scanCodeSuccess = createAction(
  '[Tavo] Scan Code Success',
  props<{ result: ScanResult }>()
);

export const scanCodeFailure = createAction(
  '[Tavo] Scan Code Failure',
  props<{ error: string }>()
);

export const scanUrl = createAction(
  '[Tavo] Scan URL',
  props<{ url: string }>()
);

export const scanUrlSuccess = createAction(
  '[Tavo] Scan URL Success',
  props<{ result: ScanResult }>()
);

export const scanUrlFailure = createAction(
  '[Tavo] Scan URL Failure',
  props<{ error: string }>()
);

export const clearError = createAction('[Tavo] Clear Error');
```

### Reducer

```typescript
// src/app/store/tavo.reducer.ts
import { createReducer, on } from '@ngrx/store';
import * as TavoActions from './tavo.actions';
import { ScanResult } from '../services/tavo.service';

export interface TavoState {
  scans: ScanResult[];
  currentScan: ScanResult | null;
  loading: boolean;
  error: string | null;
}

export const initialState: TavoState = {
  scans: [],
  currentScan: null,
  loading: false,
  error: null,
};

export const tavoReducer = createReducer(
  initialState,

  on(TavoActions.scanCode, (state) => ({
    ...state,
    loading: true,
    error: null,
  })),

  on(TavoActions.scanCodeSuccess, (state, { result }) => ({
    ...state,
    loading: false,
    scans: [...state.scans, result],
    currentScan: result,
  })),

  on(TavoActions.scanCodeFailure, (state, { error }) => ({
    ...state,
    loading: false,
    error,
  })),

  on(TavoActions.scanUrl, (state) => ({
    ...state,
    loading: true,
    error: null,
  })),

  on(TavoActions.scanUrlSuccess, (state, { result }) => ({
    ...state,
    loading: false,
    scans: [...state.scans, result],
    currentScan: result,
  })),

  on(TavoActions.scanUrlFailure, (state, { error }) => ({
    ...state,
    loading: false,
    error,
  })),

  on(TavoActions.clearError, (state) => ({
    ...state,
    error: null,
  }))
);
```

### Effects

```typescript
// src/app/store/tavo.effects.ts
import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of } from 'rxjs';
import { map, mergeMap, catchError } from 'rxjs/operators';
import { TavoService } from '../services/tavo.service';
import * as TavoActions from './tavo.actions';

@Injectable()
export class TavoEffects {
  scanCode$ = createEffect(() =>
    this.actions$.pipe(
      ofType(TavoActions.scanCode),
      mergeMap((action) =>
        this.tavoService.scanCode(action.code, action.language).pipe(
          map((result) => TavoActions.scanCodeSuccess({ result })),
          catchError((error) =>
            of(TavoActions.scanCodeFailure({ error: error.message }))
          )
        )
      )
    )
  );

  scanUrl$ = createEffect(() =>
    this.actions$.pipe(
      ofType(TavoActions.scanUrl),
      mergeMap((action) =>
        this.tavoService.scanUrl(action.url).pipe(
          map((result) => TavoActions.scanUrlSuccess({ result })),
          catchError((error) =>
            of(TavoActions.scanUrlFailure({ error: error.message }))
          )
        )
      )
    )
  );

  constructor(private actions$: Actions, private tavoService: TavoService) {}
}
```

## Main Application

### App Component

```typescript
// src/app/app.component.ts
import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { Store } from '@ngrx/store';
import { TavoState } from './store/tavo.reducer';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'Tavo AI Security Scanner';

  scans$: Observable<any[]>;
  loading$: Observable<boolean>;
  error$: Observable<string | null>;

  constructor(private store: Store<{ tavo: TavoState }>) {
    this.scans$ = this.store.select((state) => state.tavo.scans);
    this.loading$ = this.store.select((state) => state.tavo.loading);
    this.error$ = this.store.select((state) => state.tavo.error);
  }
}
```

```html
<!-- src/app/app.component.html -->
<div class="min-h-screen bg-gray-100">
  <header class="bg-blue-600 text-white p-4">
    <div class="container mx-auto">
      <h1 class="text-3xl font-bold">{{ title }}</h1>
      <p class="text-blue-100">Advanced security scanning powered by AI</p>
    </div>
  </header>

  <main class="container mx-auto px-4 py-8">
    <div class="grid md:grid-cols-2 gap-8 mb-8">
      <app-code-scanner></app-code-scanner>
      <app-url-scanner></app-url-scanner>
    </div>

    <app-scan-history></app-scan-history>
  </main>
</div>
```

### Scan History Component

```typescript
// src/app/components/scan-history/scan-history.component.ts
import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { Store } from '@ngrx/store';
import { ScanResult } from '../../services/tavo.service';
import { TavoState } from '../../store/tavo.reducer';

@Component({
  selector: 'app-scan-history',
  templateUrl: './scan-history.component.html',
  styleUrls: ['./scan-history.component.css'],
})
export class ScanHistoryComponent {
  scans$: Observable<ScanResult[]>;
  loading$: Observable<boolean>;

  constructor(private store: Store<{ tavo: TavoState }>) {
    this.scans$ = this.store.select((state) => state.tavo.scans);
    this.loading$ = this.store.select((state) => state.tavo.loading);
  }
}
```

```html
<!-- src/app/components/scan-history/scan-history.component.html -->
<div class="bg-white rounded-lg shadow-md p-6">
  <h2 class="text-2xl font-semibold mb-4">Scan History</h2>

  <div *ngIf="(scans$ | async)?.length === 0 && !(loading$ | async)" class="text-gray-500">
    No scans performed yet.
  </div>

  <div class="space-y-4">
    <div
      *ngFor="let scan of scans$ | async"
      class="border border-gray-200 rounded p-4"
    >
      <div class="flex justify-between items-start mb-2">
        <div>
          <h3 class="font-semibold">{{ scan.name }}</h3>
          <p class="text-sm text-gray-600">ID: {{ scan.id }}</p>
        </div>
        <span
          class="px-2 py-1 rounded text-sm"
          [ngClass]="{
            'bg-green-100 text-green-800': scan.status === 'completed',
            'bg-yellow-100 text-yellow-800': scan.status === 'running',
            'bg-red-100 text-red-800': scan.status === 'failed'
          }"
        >
          {{ scan.status }}
        </span>
      </div>

      <div *ngIf="scan.summary" class="text-sm text-gray-600">
        <span>Files: {{ scan.summary.files_scanned || 0 }}</span>
        <span class="ml-4">Vulnerabilities: {{ scan.summary.vulnerabilities_found || 0 }}</span>
      </div>
    </div>
  </div>
</div>
```

## Guards and Interceptors

### Auth Interceptor

```typescript
// src/app/interceptors/auth.interceptor.ts
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Only add auth header for Tavo API requests
    if (req.url.includes(environment.tavo.baseUrl)) {
      const authReq = req.clone({
        setHeaders: {
          Authorization: `Bearer ${environment.tavo.apiKey}`,
        },
      });
      return next.handle(authReq);
    }

    return next.handle(req);
  }
}
```

### Error Interceptor

```typescript
// src/app/interceptors/error.interceptor.ts
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Store } from '@ngrx/store';
import { TavoState } from '../store/tavo.reducer';
import * as TavoActions from '../store/tavo.actions';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private store: Store<{ tavo: TavoState }>) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        let errorMessage = 'An unknown error occurred';

        if (error.error instanceof ErrorEvent) {
          errorMessage = `Client error: ${error.error.message}`;
        } else {
          errorMessage = `Server error: ${error.status} - ${error.message}`;
        }

        // Dispatch error action for Tavo API requests
        if (req.url.includes('tavo.ai')) {
          this.store.dispatch(TavoActions.scanCodeFailure({ error: errorMessage }));
        }

        return throwError(() => error);
      })
    );
  }
}
```

## Testing

### Service Tests

```typescript
// src/app/services/tavo.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TavoService } from './tavo.service';
import { environment } from '../../environments/environment';

describe('TavoService', () => {
  let service: TavoService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [TavoService],
    });

    service = TestBed.inject(TavoService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should scan code successfully', () => {
    const mockResponse = { id: 'test-id', status: 'completed' };

    service.scanCode('console.log("test");', 'javascript').subscribe((result) => {
      expect(result).toEqual(mockResponse);
    });

    const req = httpMock.expectOne(`${environment.tavo.baseUrl}/scans`);
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });

  it('should handle scan code error', () => {
    service.scanCode('invalid code', 'javascript').subscribe({
      next: () => fail('Should have failed'),
      error: (error) => {
        expect(error.message).toContain('Server error');
      },
    });

    const req = httpMock.expectOne(`${environment.tavo.baseUrl}/scans`);
    req.flush('Server error', { status: 500, statusText: 'Server Error' });
  });
});
```

### Component Tests

```typescript
// src/app/components/code-scanner/code-scanner.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { Store } from '@ngrx/store';
import { provideMockStore, MockStore } from '@ngrx/store/testing';
import { CodeScannerComponent } from './code-scanner.component';
import { TavoState } from '../../store/tavo.reducer';

describe('CodeScannerComponent', () => {
  let component: CodeScannerComponent;
  let fixture: ComponentFixture<CodeScannerComponent>;
  let store: MockStore<{ tavo: TavoState }>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CodeScannerComponent],
      imports: [FormsModule],
      providers: [provideMockStore({ initialState: { tavo: { scans: [], currentScan: null, loading: false, error: null } } })],
    }).compileComponents();

    fixture = TestBed.createComponent(CodeScannerComponent);
    component = fixture.componentInstance;
    store = TestBed.inject(MockStore);
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show validation error for empty code', () => {
    spyOn(window, 'alert');
    component.onScan();
    expect(window.alert).toHaveBeenCalledWith('Please enter some code to scan');
  });
});
```

## Docker Configuration

### Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build --prod

# Use nginx to serve the built application
FROM nginx:alpine

COPY --from=0 /app/dist/tavo-angular /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  tavo-angular:
    build: .
    ports:
      - "80:80"
    environment:
      - TAVO_API_KEY=${TAVO_API_KEY}
    restart: unless-stopped
```

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass https://api.tavo.ai;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    }
}
```

## Deployment

### Production Build

```json
// package.json (scripts section)
{
  "scripts": {
    "build": "ng build",
    "build:prod": "ng build --configuration production",
    "test": "ng test",
    "lint": "ng lint"
  }
}
```

### Environment Variables for Production

```bash
# Production environment
TAVO_API_KEY=your-production-api-key
```

This Angular integration provides a robust, type-safe interface for Tavo AI security scanning with NgRx state management, comprehensive testing, and production deployment configurations.

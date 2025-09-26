---
sidebar_position: 6
---

# Vue.js Integration

Integrate Tavo AI security scanning into your Vue.js applications.

## Installation

```bash
npm install tavo-ai axios vue-router vuex
```

## Basic Setup

### Environment Configuration

```javascript
// .env
VUE_APP_TAVO_API_KEY=your-api-key-here
VUE_APP_TAVO_BASE_URL=https://api.tavo.ai
VUE_APP_TAVO_TIMEOUT=30000
```

### Tavo Service

```javascript
// services/tavoService.js
import axios from 'axios';

class TavoService {
    constructor() {
        this.client = axios.create({
            baseURL: process.env.VUE_APP_TAVO_BASE_URL || 'https://api.tavo.ai',
            timeout: parseInt(process.env.VUE_APP_TAVO_TIMEOUT) || 30000,
            headers: {
                'Authorization': `Bearer ${process.env.VUE_APP_TAVO_API_KEY}`,
                'Content-Type': 'application/json',
            },
        });
    }

    async scanCode(code, language = 'javascript') {
        try {
            const response = await this.client.post('/scans', {
                name: `Code Scan - ${language}`,
                target: code,
                scan_type: 'code',
                language: language,
            });
            return response.data;
        } catch (error) {
            throw new Error(`Code scan failed: ${error.response?.data?.message || error.message}`);
        }
    }

    async scanUrl(url) {
        try {
            const response = await this.client.post('/scans', {
                name: `URL Scan - ${url}`,
                target: url,
                scan_type: 'web',
            });
            return response.data;
        } catch (error) {
            throw new Error(`URL scan failed: ${error.response?.data?.message || error.message}`);
        }
    }

    async getScanResults(scanId) {
        try {
            const response = await this.client.get(`/scans/${scanId}/results`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get scan results: ${error.response?.data?.message || error.message}`);
        }
    }

    async generateReport(scanIds, format = 'pdf') {
        try {
            const response = await this.client.post('/reports', {
                type: 'compliance',
                format: format,
                scan_ids: scanIds,
            });
            return response.data;
        } catch (error) {
            throw new Error(`Report generation failed: ${error.response?.data?.message || error.message}`);
        }
    }
}

export default new TavoService();
```

## Vuex Store

### Store Configuration

```javascript
// store/index.js
import Vue from 'vue';
import Vuex from 'vuex';
import tavoService from '../services/tavoService';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        scans: [],
        currentScan: null,
        loading: false,
        error: null,
    },

    mutations: {
        SET_LOADING(state, loading) {
            state.loading = loading;
        },

        SET_ERROR(state, error) {
            state.error = error;
        },

        CLEAR_ERROR(state) {
            state.error = null;
        },

        ADD_SCAN(state, scan) {
            state.scans.push(scan);
            state.currentScan = scan;
        },

        SET_CURRENT_SCAN(state, scan) {
            state.currentScan = scan;
        },
    },

    actions: {
        async scanCode({ commit }, { code, language = 'javascript' }) {
            commit('SET_LOADING', true);
            commit('CLEAR_ERROR');

            try {
                const result = await tavoService.scanCode(code, language);
                commit('ADD_SCAN', result);
                return result;
            } catch (error) {
                commit('SET_ERROR', error.message);
                throw error;
            } finally {
                commit('SET_LOADING', false);
            }
        },

        async scanUrl({ commit }, url) {
            commit('SET_LOADING', true);
            commit('CLEAR_ERROR');

            try {
                const result = await tavoService.scanUrl(url);
                commit('ADD_SCAN', result);
                return result;
            } catch (error) {
                commit('SET_ERROR', error.message);
                throw error;
            } finally {
                commit('SET_LOADING', false);
            }
        },

        async getScanResults({ commit }, scanId) {
            commit('SET_LOADING', true);
            commit('CLEAR_ERROR');

            try {
                const result = await tavoService.getScanResults(scanId);
                commit('SET_CURRENT_SCAN', result);
                return result;
            } catch (error) {
                commit('SET_ERROR', error.message);
                throw error;
            } finally {
                commit('SET_LOADING', false);
            }
        },

        async generateReport({ commit }, { scanIds, format = 'pdf' }) {
            commit('SET_LOADING', true);
            commit('CLEAR_ERROR');

            try {
                const result = await tavoService.generateReport(scanIds, format);
                return result;
            } catch (error) {
                commit('SET_ERROR', error.message);
                throw error;
            } finally {
                commit('SET_LOADING', false);
            }
        },

        clearError({ commit }) {
            commit('CLEAR_ERROR');
        },
    },

    getters: {
        scanHistory: (state) => state.scans,
        currentScan: (state) => state.currentScan,
        isLoading: (state) => state.loading,
        error: (state) => state.error,
    },
});
```

## Vue Components

### Code Scanner Component

```vue
<!-- components/CodeScanner.vue -->
<template>
    <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-2xl font-semibold mb-4">Code Security Scan</h2>

        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Programming Language
            </label>
            <select
                v-model="language"
                class="w-full p-2 border border-gray-300 rounded-md"
            >
                <option value="javascript">JavaScript</option>
                <option value="typescript">TypeScript</option>
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
                v-model="code"
                rows="10"
                class="w-full p-2 border border-gray-300 rounded-md font-mono text-sm"
                placeholder="Paste your code here..."
            ></textarea>
        </div>

        <button
            @click="handleScan"
            :disabled="loading || !code.trim()"
            class="bg-blue-500 hover:bg-blue-700 disabled:bg-blue-300 text-white font-bold py-2 px-4 rounded"
        >
            {{ loading ? 'Scanning...' : 'Scan Code' }}
        </button>

        <div v-if="error" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            Error: {{ error }}
        </div>

        <ScanResultDisplay
            v-if="scanResult"
            :result="scanResult"
            @view-details="handleViewDetails"
        />
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import ScanResultDisplay from './ScanResultDisplay.vue';

export default {
    name: 'CodeScanner',
    components: {
        ScanResultDisplay,
    },
    data() {
        return {
            code: '',
            language: 'javascript',
            scanResult: null,
            detailedResults: null,
        };
    },
    computed: {
        ...mapGetters(['loading', 'error']),
    },
    methods: {
        ...mapActions(['scanCode', 'getScanResults']),

        async handleScan() {
            if (!this.code.trim()) {
                alert('Please enter some code to scan');
                return;
            }

            try {
                this.scanResult = await this.scanCode({
                    code: this.code,
                    language: this.language,
                });
            } catch (error) {
                console.error('Scan failed:', error);
            }
        },

        async handleViewDetails(scanId) {
            try {
                this.detailedResults = await this.getScanResults(scanId);
            } catch (error) {
                console.error('Failed to get detailed results:', error);
            }
        },
    },
};
</script>
```

### URL Scanner Component

```vue
<!-- components/UrlScanner.vue -->
<template>
    <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-2xl font-semibold mb-4">URL Security Scan</h2>

        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
                URL to Scan
            </label>
            <input
                v-model="url"
                type="url"
                class="w-full p-2 border border-gray-300 rounded-md"
                placeholder="https://example.com"
                @input="validateUrl"
            >
            <p v-if="url && !isValidUrl" class="text-red-500 text-sm mt-1">
                Please enter a valid URL
            </p>
        </div>

        <button
            @click="handleScan"
            :disabled="loading || !isValidUrl"
            class="bg-blue-500 hover:bg-blue-700 disabled:bg-blue-300 text-white font-bold py-2 px-4 rounded"
        >
            {{ loading ? 'Scanning...' : 'Scan URL' }}
        </button>

        <div v-if="error" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            Error: {{ error }}
        </div>

        <ScanResultDisplay
            v-if="scanResult"
            :result="scanResult"
            @view-details="handleViewDetails"
        />
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import ScanResultDisplay from './ScanResultDisplay.vue';

export default {
    name: 'UrlScanner',
    components: {
        ScanResultDisplay,
    },
    data() {
        return {
            url: '',
            isValidUrl: false,
            scanResult: null,
        };
    },
    computed: {
        ...mapGetters(['loading', 'error']),
    },
    methods: {
        ...mapActions(['scanUrl', 'getScanResults']),

        validateUrl() {
            try {
                new URL(this.url);
                this.isValidUrl = true;
            } catch {
                this.isValidUrl = false;
            }
        },

        async handleScan() {
            if (!this.url.trim()) {
                alert('Please enter a URL to scan');
                return;
            }

            try {
                this.scanResult = await this.scanUrl(this.url);
            } catch (error) {
                console.error('Scan failed:', error);
            }
        },

        async handleViewDetails(scanId) {
            try {
                await this.getScanResults(scanId);
            } catch (error) {
                console.error('Failed to get detailed results:', error);
            }
        },
    },
    watch: {
        url() {
            this.validateUrl();
        },
    },
};
</script>
```

### Scan Result Display Component

```vue
<!-- components/ScanResultDisplay.vue -->
<template>
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
                    :class="{
                        'bg-green-100 text-green-800': result.status === 'completed',
                        'bg-yellow-100 text-yellow-800': result.status === 'running',
                        'bg-red-100 text-red-800': result.status === 'failed'
                    }"
                >
                    {{ result.status }}
                </span>
            </div>
        </div>

        <div v-if="result.summary" class="mb-4">
            <h4 class="font-semibold mb-2">Summary:</h4>
            <ul class="list-disc list-inside text-sm space-y-1">
                <li>Files scanned: {{ result.summary.files_scanned || 0 }}</li>
                <li>Vulnerabilities found: {{ result.summary.vulnerabilities_found || 0 }}</li>
                <li>Scan duration: {{ result.summary.duration || 'N/A' }}</li>
            </ul>
        </div>

        <button
            @click="$emit('view-details', result.id)"
            :disabled="loading"
            class="bg-green-500 hover:bg-green-700 disabled:bg-green-300 text-white font-bold py-2 px-4 rounded"
        >
            {{ loading ? 'Loading...' : 'View Detailed Results' }}
        </button>

        <div v-if="detailedResults" class="mt-4 p-4 bg-white border border-gray-200 rounded">
            <h4 class="font-semibold mb-2">Detailed Results</h4>
            <pre class="text-sm overflow-x-auto">{{ JSON.stringify(detailedResults, null, 2) }}</pre>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'ScanResultDisplay',
    props: {
        result: {
            type: Object,
            required: true,
        },
    },
    computed: {
        ...mapGetters(['loading']),
        detailedResults() {
            return this.$store.state.currentScan;
        },
    },
};
</script>
```

### Scan History Component

```vue
<!-- components/ScanHistory.vue -->
<template>
    <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-2xl font-semibold mb-4">Scan History</h2>

        <div v-if="scans.length === 0 && !loading" class="text-gray-500">
            No scans performed yet.
        </div>

        <div v-else class="space-y-4">
            <div
                v-for="(scan, index) in scans"
                :key="scan.id || index"
                class="border border-gray-200 rounded p-4"
            >
                <div class="flex justify-between items-start mb-2">
                    <div>
                        <h3 class="font-semibold">{{ scan.name }}</h3>
                        <p class="text-sm text-gray-600">ID: {{ scan.id }}</p>
                    </div>
                    <span
                        class="px-2 py-1 rounded text-sm"
                        :class="{
                            'bg-green-100 text-green-800': scan.status === 'completed',
                            'bg-yellow-100 text-yellow-800': scan.status === 'running',
                            'bg-red-100 text-red-800': scan.status === 'failed'
                        }"
                    >
                        {{ scan.status }}
                    </span>
                </div>

                <div v-if="scan.summary" class="text-sm text-gray-600">
                    <span>Files: {{ scan.summary.files_scanned || 0 }}</span>
                    <span class="ml-4">Vulnerabilities: {{ scan.summary.vulnerabilities_found || 0 }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    name: 'ScanHistory',
    computed: {
        ...mapGetters(['scanHistory', 'loading']),
        scans() {
            return this.scanHistory;
        },
    },
};
</script>
```

## Vue Router Configuration

### Router Setup

```javascript
// router/index.js
import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Scanner from '../views/Scanner.vue';
import History from '../views/History.vue';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/scanner',
        name: 'Scanner',
        component: Scanner,
    },
    {
        path: '/history',
        name: 'History',
        component: History,
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

export default router;
```

## Main Application

### App.vue

```vue
<!-- App.vue -->
<template>
    <div id="app" class="min-h-screen bg-gray-100">
        <header class="bg-blue-600 text-white p-4">
            <div class="container mx-auto">
                <nav class="flex justify-between items-center">
                    <router-link to="/" class="text-2xl font-bold">
                        Tavo AI Security Scanner
                    </router-link>
                    <ul class="flex space-x-6">
                        <li>
                            <router-link to="/" class="hover:text-blue-200">Home</router-link>
                        </li>
                        <li>
                            <router-link to="/scanner" class="hover:text-blue-200">Scanner</router-link>
                        </li>
                        <li>
                            <router-link to="/history" class="hover:text-blue-200">History</router-link>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>

        <main class="container mx-auto px-4 py-8">
            <router-view />
        </main>
    </div>
</template>

<script>
export default {
    name: 'App',
};
</script>

<style>
/* Global styles */
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
</style>
```

### Views

```vue
<!-- views/Scanner.vue -->
<template>
    <div>
        <h1 class="text-3xl font-bold mb-8">Security Scanner</h1>

        <div class="grid md:grid-cols-2 gap-8">
            <CodeScanner />
            <UrlScanner />
        </div>
    </div>
</template>

<script>
import CodeScanner from '../components/CodeScanner.vue';
import UrlScanner from '../components/UrlScanner.vue';

export default {
    name: 'Scanner',
    components: {
        CodeScanner,
        UrlScanner,
    },
};
</script>
```

```vue
<!-- views/History.vue -->
<template>
    <div>
        <h1 class="text-3xl font-bold mb-8">Scan History</h1>
        <ScanHistory />
    </div>
</template>

<script>
import ScanHistory from '../components/ScanHistory.vue';

export default {
    name: 'History',
    components: {
        ScanHistory,
    },
};
</script>
```

## Mixins

### Tavo Mixin

```javascript
// mixins/tavoMixin.js
import { mapActions, mapGetters } from 'vuex';

export const tavoMixin = {
    computed: {
        ...mapGetters(['loading', 'error', 'currentScan']),
    },

    methods: {
        ...mapActions(['clearError']),

        handleScanError(error) {
            console.error('Scan error:', error);
            this.$emit('scan-error', error);
        },

        handleScanSuccess(result) {
            console.log('Scan successful:', result);
            this.$emit('scan-success', result);
        },
    },
};
```

## Plugins

### Tavo Plugin

```javascript
// plugins/tavo.js
import tavoService from '../services/tavoService';

export default {
    install(Vue) {
        Vue.prototype.$tavo = tavoService;

        // Global mixin for error handling
        Vue.mixin({
            methods: {
                $handleTavoError(error) {
                    console.error('Tavo error:', error);
                    this.$store.dispatch('clearError');
                    // You can add global error handling logic here
                },
            },
        });
    },
};
```

### Vue Configuration

```javascript
// main.js
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import tavoPlugin from './plugins/tavo';

Vue.config.productionTip = false;

Vue.use(tavoPlugin);

new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount('#app');
```

## Testing

### Component Tests

```javascript
// tests/unit/CodeScanner.spec.js
import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import CodeScanner from '@/components/CodeScanner.vue';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('CodeScanner.vue', () => {
    let store;
    let actions;

    beforeEach(() => {
        actions = {
            scanCode: jest.fn(),
        };

        store = new Vuex.Store({
            actions,
        });
    });

    it('renders correctly', () => {
        const wrapper = shallowMount(CodeScanner, { store, localVue });
        expect(wrapper.find('h2').text()).toBe('Code Security Scan');
    });

    it('calls scanCode action when scan button is clicked', async () => {
        const wrapper = shallowMount(CodeScanner, { store, localVue });

        wrapper.setData({ code: 'console.log("test");', language: 'javascript' });
        await wrapper.vm.$nextTick();

        const button = wrapper.find('button');
        await button.trigger('click');

        expect(actions.scanCode).toHaveBeenCalledWith(
            expect.any(Object),
            { code: 'console.log("test");', language: 'javascript' }
        );
    });

    it('shows validation error for empty code', async () => {
        const wrapper = shallowMount(CodeScanner, { store, localVue });
        const alertMock = jest.spyOn(window, 'alert').mockImplementation(() => {});

        const button = wrapper.find('button');
        await button.trigger('click');

        expect(alertMock).toHaveBeenCalledWith('Please enter some code to scan');
        alertMock.mockRestore();
    });
});
```

### Store Tests

```javascript
// tests/unit/store.spec.js
import store from '@/store';

describe('Vuex Store', () => {
    it('has correct initial state', () => {
        expect(store.state.scans).toEqual([]);
        expect(store.state.currentScan).toBeNull();
        expect(store.state.loading).toBe(false);
        expect(store.state.error).toBeNull();
    });

    it('mutations work correctly', () => {
        store.commit('SET_LOADING', true);
        expect(store.state.loading).toBe(true);

        store.commit('SET_ERROR', 'Test error');
        expect(store.state.error).toBe('Test error');

        store.commit('CLEAR_ERROR');
        expect(store.state.error).toBeNull();

        const scan = { id: 'test-id', status: 'completed' };
        store.commit('ADD_SCAN', scan);
        expect(store.state.scans).toContain(scan);
        expect(store.state.currentScan).toEqual(scan);
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
RUN npm run build

# Expose port
EXPOSE 8080

# Start the application
CMD ["npm", "run", "serve"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  tavo-vue:
    build: .
    ports:
      - "8080:8080"
    environment:
      - VUE_APP_TAVO_API_KEY=${TAVO_API_KEY}
      - VUE_APP_TAVO_BASE_URL=https://api.tavo.ai
    restart: unless-stopped
```

## Deployment

### Production Build

```javascript
// package.json (scripts section)
{
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "test:unit": "vue-cli-service test:unit",
    "lint": "vue-cli-service lint"
  }
}
```

### Nginx Configuration

```nginx
# nginx.conf
server {
    listen 80;
    server_name your-domain.com;
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
```

This Vue.js integration provides a reactive, component-based interface for Tavo AI security scanning with Vuex state management, Vue Router navigation, comprehensive testing, and production deployment configurations.

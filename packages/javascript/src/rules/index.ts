/**
 * Rule management for TavoAI JavaScript SDK
 */

import { exec } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import { promisify } from 'util';
// @ts-ignore
const yaml = require('js-yaml');

const execAsync = promisify(exec);

export interface RuleBundle {
    name: string;
    version: string;
    description: string;
    rules: any[];
    categories: Record<string, string>;
    lastUpdated: Date;
}

export interface ScanResult {
    vulnerabilities: any[];
    passed: boolean;
    scanTime: number;
}

export interface RuleManagerConfig {
    cacheDir?: string;
}

export class RuleManager {
    private readonly cacheDir: string;
    private readonly bundles: Map<string, RuleBundle> = new Map();

    constructor(config: RuleManagerConfig = {}) {
        this.cacheDir = config.cacheDir || path.join(require('os').homedir(), '.tavoai', 'rules');
        this.ensureCacheDir();
    }

    private ensureCacheDir(): void {
        try {
            if (!fs.existsSync(this.cacheDir)) {
                fs.mkdirSync(this.cacheDir, { recursive: true });
            }
        } catch (error) {
            // Silently ignore directory creation errors in restricted environments
            console.warn('Failed to create cache directory:', error instanceof Error ? error.message : String(error));
        }
    }

    async downloadBundle(bundleName: string): Promise<RuleBundle> {
        try {
            // For now, use local file access since we have the repo locally
            // In production, this would download from GitHub releases
            const bundleDir = this.findBundleLocally(bundleName);
            if (bundleDir) {
                return this.loadBundleFromDirectory(bundleDir);
            }

            throw new Error(`Bundle '${bundleName}' not found`);
        } catch (error) {
            console.error(`Failed to download bundle ${bundleName}:`, error);
            throw new Error(`Failed to download bundle: ${error}`);
        }
    }

    private findBundleLocally(bundleName: string): string | null {
        // Check if we're in the workspace
        let currentDir = process.cwd();
        let workspaceRoot = currentDir;

        while (workspaceRoot !== path.dirname(workspaceRoot)) {
            const tavoRules = path.join(workspaceRoot, 'tavo-rules', 'bundles', bundleName);
            if (fs.existsSync(tavoRules)) {
                return tavoRules;
            }
            workspaceRoot = path.dirname(workspaceRoot);
        }
        return null;
    }

    private loadBundleFromDirectory(bundleDir: string): RuleBundle {
        const indexFile = path.join(bundleDir, 'index.json');
        if (!fs.existsSync(indexFile)) {
            throw new Error(`Bundle index not found: ${indexFile}`);
        }

        const indexData = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));

        // Load all YAML rule files
        const rules: any[] = [];
        const yamlFiles = fs.readdirSync(bundleDir).filter(file => file.endsWith('.yaml'));

        for (const yamlFile of yamlFiles) {
            try {
                const filePath = path.join(bundleDir, yamlFile);
                const yamlContent = fs.readFileSync(filePath, 'utf-8');
                const yamlData = yaml.load(yamlContent) as any; if (yamlData?.rules) {
                    rules.push(...yamlData.rules);
                }
            } catch (error) {
                console.warn(`Failed to load rules from ${yamlFile}:`, error);
            }
        }

        const bundle: RuleBundle = {
            name: indexData.name,
            version: indexData.version,
            description: indexData.description,
            rules,
            categories: indexData.categories || {},
            lastUpdated: new Date(indexData.metadata.last_updated)
        };

        this.bundles.set(bundle.name, bundle);
        return bundle;
    }

    getBundle(bundleName: string): RuleBundle | undefined {
        return this.bundles.get(bundleName);
    }

    listBundles(): string[] {
        return Array.from(this.bundles.keys());
    }
}

export class OpenGrepEngine {
    private readonly opengrepPath: string;

    constructor(opengrepPath: string = '') {
        this.opengrepPath = opengrepPath || this.findBundledEngine() || 'opengrep';
    }

    private findBundledEngine(): string | null {
        // Try to find bundled engine in SDK directory
        const sdkDir = path.dirname(path.dirname(path.dirname(__dirname)));
        const enginesDir = path.join(sdkDir, 'engines');

        const candidates = ['opengrep-core', 'opengrep-core.exe', 'opengrep'];
        for (const candidate of candidates) {
            const enginePath = path.join(enginesDir, candidate);
            if (fs.existsSync(enginePath)) {
                return enginePath;
            }
        }
        return null;
    }

    async checkOpenGrep(): Promise<void> {
        try {
            await execAsync(`${this.opengrepPath} --version`);
        } catch {
            throw new Error('OpenGrep executable not found. Please install OpenGrep.');
        }
    }

    async scanFile(filePath: string, rules: any[]): Promise<any[]> {
        if (!fs.existsSync(filePath)) {
            return [];
        }

        const findings: any[] = [];

        // Create temporary rule file
        const tempDir = require('os').tmpdir();
        const ruleFile = path.join(tempDir, `rules-${Date.now()}.yaml`);

        try {
            const ruleContent = yaml.dump({ rules });
            fs.writeFileSync(ruleFile, ruleContent);

            // Run OpenGrep
            const cmd = `${this.opengrepPath} --config ${ruleFile} --json ${filePath}`;

            const { stdout } = await execAsync(cmd, { timeout: 30000 });

            if (stdout) {
                try {
                    const output = JSON.parse(stdout);
                    findings.push(...(output.matches || []));
                } catch {
                    console.warn(`Failed to parse OpenGrep output: ${stdout}`);
                }
            }

        } catch (error: any) {
            if (error.code !== 1) { // Code 1 means matches found, which is not an error
                console.error(`OpenGrep scan failed:`, error);
            }
        } finally {
            // Clean up temporary file
            if (fs.existsSync(ruleFile)) {
                fs.unlinkSync(ruleFile);
            }
        }

        return findings;
    }

    async scanDirectory(dirPath: string, rules: any[], extensions?: string[]): Promise<any[]> {
        if (!fs.existsSync(dirPath)) {
            return [];
        }

        const allFindings: any[] = [];

        // Find files to scan
        const files = this.findFiles(dirPath, extensions);

        for (const filePath of files) {
            const findings = await this.scanFile(filePath, rules);
            allFindings.push(...findings);
        }

        return allFindings;
    }

    private findFiles(dirPath: string, extensions?: string[]): string[] {
        const files: string[] = [];

        const traverse = (currentPath: string) => {
            const items = fs.readdirSync(currentPath);

            for (const item of items) {
                const fullPath = path.join(currentPath, item);
                const stat = fs.statSync(fullPath);

                if (stat.isDirectory()) {
                    traverse(fullPath);
                } else if (stat.isFile()) {
                    if (!extensions || extensions.some(ext => fullPath.endsWith(ext))) {
                        if (!this.isBinaryFile(fullPath)) {
                            files.push(fullPath);
                        }
                    }
                }
            }
        };

        traverse(dirPath);
        return files;
    }

    private isBinaryFile(filePath: string): boolean {
        try {
            const buffer = fs.readFileSync(filePath);
            const chunk = buffer.subarray(0, Math.min(1024, buffer.length));
            return chunk.includes(0);
        } catch {
            return true;
        }
    }
}

export class OPAEngine {
    private readonly opaPath: string;

    constructor(opaPath: string = 'opa') {
        this.opaPath = opaPath;
    }

    async checkOPA(): Promise<void> {
        try {
            await execAsync(`${this.opaPath} version`);
        } catch {
            throw new Error('OPA executable not found. Please install OPA.');
        }
    }

    async evaluatePolicy(policyContent: string, inputData: any): Promise<any> {
        const tempDir = require('os').tmpdir();
        const policyFile = path.join(tempDir, `policy-${Date.now()}.rego`);
        const inputFile = path.join(tempDir, `input-${Date.now()}.json`);

        try {
            fs.writeFileSync(policyFile, policyContent);
            fs.writeFileSync(inputFile, JSON.stringify(inputData));

            const cmd = `${this.opaPath} eval --data ${policyFile} --input ${inputFile} --format json data`;

            const { stdout } = await execAsync(cmd, { timeout: 30000 });

            if (stdout) {
                return JSON.parse(stdout);
            }

            return {};

        } catch (error) {
            console.error(`OPA evaluation failed:`, error);
            return {};
        } finally {
            // Clean up temporary files
            if (fs.existsSync(policyFile)) fs.unlinkSync(policyFile);
            if (fs.existsSync(inputFile)) fs.unlinkSync(inputFile);
        }
    }
}

export class SecurityScanner {
    private readonly ruleManager: RuleManager;
    private readonly opengrep: OpenGrepEngine;
    private readonly opa: OPAEngine;
    private readonly scannerBinaryPath: string | null;

    constructor(ruleManager: RuleManager) {
        this.ruleManager = ruleManager;
        this.opengrep = new OpenGrepEngine();
        this.opa = new OPAEngine();
        this.scannerBinaryPath = this.findScannerBinary();
    }

    private findScannerBinary(): string | null {
        // Try to find scanner binary in SDK directory
        const sdkDir = path.dirname(path.dirname(path.dirname(__dirname)));
        const scannerPath = path.join(sdkDir, 'scanner', 'dist', 'tavo-scanner');

        if (fs.existsSync(scannerPath)) {
            return scannerPath;
        }

        // Try to find it in the workspace
        let currentDir = process.cwd();
        let workspaceRoot = currentDir;

        while (workspaceRoot !== path.dirname(workspaceRoot)) {
            const scannerPath = path.join(workspaceRoot, 'tavo-sdk', 'packages', 'scanner', 'dist', 'tavo-scanner');
            if (fs.existsSync(scannerPath)) {
                return scannerPath;
            }
            workspaceRoot = path.dirname(workspaceRoot);
        }

        // Fall back to system PATH
        try {
            const { execSync } = require('child_process');
            execSync('which tavo-scanner', { stdio: 'ignore' });
            return 'tavo-scanner';
        } catch {
            return null;
        }
    }

    async scanCodebase(pathToScan: string, bundleName: string = 'llm-security', useBinary: boolean = true): Promise<ScanResult> {
        const startTime = Date.now();

        // Try to use scanner binary if available and requested
        if (useBinary && this.scannerBinaryPath) {
            try {
                return await this.scanWithBinary(pathToScan, bundleName);
            } catch (error) {
                console.warn('Scanner binary failed, falling back to built-in scanning:', error);
                // Fall through to built-in scanning
            }
        }

        // Built-in scanning fallback
        let bundle = this.ruleManager.getBundle(bundleName);
        bundle ??= await this.ruleManager.downloadBundle(bundleName);

        const findings: any[] = [];

        // Scan with OpenGrep rules
        const opengrepRules = bundle.rules.filter(rule => rule.pattern);
        if (opengrepRules.length > 0) {
            const stat = fs.statSync(pathToScan);
            if (stat.isFile()) {
                findings.push(...await this.opengrep.scanFile(pathToScan, opengrepRules));
            } else {
                findings.push(...await this.opengrep.scanDirectory(pathToScan, opengrepRules));
            }
        }

        // TODO: Add OPA policy evaluation for more complex rules

        const scanTime = Date.now() - startTime;
        const passed = findings.length === 0;

        return {
            vulnerabilities: findings,
            passed,
            scanTime
        };
    }

    private async scanWithBinary(pathToScan: string, bundleName: string): Promise<ScanResult> {
        if (!this.scannerBinaryPath) {
            throw new Error('Scanner binary not available');
        }

        const cmd = `${this.scannerBinaryPath} "${pathToScan}" --bundle ${bundleName} --format json`;

        try {
            const { stdout } = await execAsync(cmd, { timeout: 300000 }); // 5 minute timeout

            if (stdout) {
                const result = JSON.parse(stdout);
                return {
                    vulnerabilities: result.vulnerabilities || [],
                    passed: result.passed || false,
                    scanTime: result.scan_time || 0
                };
            }

            throw new Error('No output from scanner binary');

        } catch (error: any) {
            if (error.code === 1) {
                // Code 1 means findings were found, try to parse output anyway
                try {
                    const result = JSON.parse(error.stdout || '{}');
                    return {
                        vulnerabilities: result.vulnerabilities || [],
                        passed: result.passed || false,
                        scanTime: result.scan_time || 0
                    };
                } catch {
                    // If we can't parse, assume findings were found
                    return {
                        vulnerabilities: [{ message: 'Security issues found' }],
                        passed: false,
                        scanTime: 0
                    };
                }
            }
            throw error;
        }
    }
}
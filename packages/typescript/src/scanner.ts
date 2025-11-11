/**
 * Tavo Scanner Wrapper
 *
 * Executes tavo-scanner as a subprocess with plugin/rule configuration.
 */

import { spawn } from 'child_process';
import * as crypto from 'crypto';
import { promises as fs } from 'fs';
import * as os from 'os';
import * as path from 'path';

export interface ScannerConfig {
  /** Path to tavo-scanner binary */
  scannerPath?: string;

  /** List of plugins to use */
  plugins?: string[];

  /** Plugin-specific configuration */
  pluginConfig?: Record<string, any>;

  /** Path to custom rules file */
  rulesPath?: string;

  /** Custom rules configuration */
  customRules?: Record<string, any>;

  /** Execution timeout in seconds */
  timeout?: number;

  /** Working directory for execution */
  workingDirectory?: string;

  /** Output format */
  outputFormat?: string;

  /** Output file path */
  outputFile?: string;
}

export interface ScanOptions {
  /** Static analysis enabled */
  staticAnalysis?: boolean;

  /** Static analysis plugins */
  staticPlugins?: string[];

  /** Custom rules path */
  staticRules?: string;

  /** Dynamic testing enabled */
  dynamicTesting?: boolean;

  /** Dynamic testing plugins */
  dynamicPlugins?: string[];

  /** Output format */
  outputFormat?: string;

  /** Output file path */
  outputFile?: string;

  /** Execution timeout */
  timeout?: number;

  /** Files to exclude */
  excludePatterns?: string[];

  /** Files to include */
  includePatterns?: string[];
}

export interface ScanResult {
  status: 'success' | 'error';
  results?: any[];
  output?: string;
  error?: string;
}

export class TavoScanner {
  private config: Required<ScannerConfig>;

  constructor(config: ScannerConfig = {}) {
    this.config = {
      scannerPath: config.scannerPath || this.findScannerBinary(),
      plugins: config.plugins || [],
      pluginConfig: config.pluginConfig || {},
      rulesPath: config.rulesPath,
      customRules: config.customRules || {},
      timeout: config.timeout || 300,
      workingDirectory: config.workingDirectory || process.cwd(),
      outputFormat: config.outputFormat || 'json',
      outputFile: config.outputFile,
    };
  }

  /**
   * Find the tavo-scanner binary
   */
  private findScannerBinary(): string {
    // Try relative to package
    const packageDir = path.resolve(__dirname, '../../../..');
    const scannerPath = path.join(packageDir, 'tavo-cli', 'bin', 'tavo-scanner');

    try {
      if (require('fs').existsSync(scannerPath)) {
        return scannerPath;
      }
    } catch {
      // Ignore
    }

    // Check PATH
    return 'tavo-scanner'; // Assume it's in PATH
  }

  /**
   * Scan a directory with tavo-scanner
   */
  async scanDirectory(
    targetPath: string,
    scanOptions?: ScanOptions,
    additionalArgs?: Record<string, any>
  ): Promise<ScanResult> {
    if (!this.config.scannerPath) {
      throw new Error('tavo-scanner binary not found. Please install tavo-cli or set scannerPath.');
    }

    // Merge configurations
    const mergedConfig = { ...this.config };

    if (scanOptions) {
      mergedConfig.plugins = scanOptions.staticPlugins || mergedConfig.plugins;
      mergedConfig.rulesPath = scanOptions.staticRules || mergedConfig.rulesPath;
      mergedConfig.timeout = scanOptions.timeout || mergedConfig.timeout;
      mergedConfig.outputFormat = scanOptions.outputFormat || mergedConfig.outputFormat;
      mergedConfig.outputFile = scanOptions.outputFile || mergedConfig.outputFile;
    }

    if (additionalArgs) {
      Object.assign(mergedConfig, additionalArgs);
    }

    // Prepare command arguments
    const args: string[] = [targetPath];

    // Add plugins
    if (mergedConfig.plugins && mergedConfig.plugins.length > 0) {
      mergedConfig.plugins.forEach(plugin => {
        args.push('--plugin', plugin);
      });
    }

    // Add rules
    if (mergedConfig.rulesPath) {
      args.push('--rules', mergedConfig.rulesPath);
    }

    // Add output options
    if (mergedConfig.outputFormat) {
      args.push('--format', mergedConfig.outputFormat);
    }

    if (mergedConfig.outputFile) {
      args.push('--output', mergedConfig.outputFile);
    }

    // Add timeout
    if (mergedConfig.timeout) {
      args.push('--timeout', mergedConfig.timeout.toString());
    }

    return this.executeScanner(args, mergedConfig.workingDirectory);
  }

  /**
   * Scan with specific plugins
   */
  async scanWithPlugins(
    targetPath: string,
    plugins: string[],
    options?: Partial<ScanOptions>
  ): Promise<ScanResult> {
    const scanOptions: ScanOptions = {
      ...options,
      staticPlugins: plugins,
    };

    return this.scanDirectory(targetPath, scanOptions);
  }

  /**
   * Scan with custom rules
   */
  async scanWithRules(
    targetPath: string,
    rulesPath: string,
    options?: Partial<ScanOptions>
  ): Promise<ScanResult> {
    const scanOptions: ScanOptions = {
      ...options,
      staticRules: rulesPath,
    };

    return this.scanDirectory(targetPath, scanOptions);
  }

  /**
   * Execute the scanner subprocess
   */
  private async executeScanner(args: string[], workingDirectory?: string): Promise<ScanResult> {
    return new Promise((resolve, reject) => {
      const child = spawn(this.config.scannerPath, args, {
        cwd: workingDirectory || this.config.workingDirectory,
        stdio: ['pipe', 'pipe', 'pipe'],
      });

      let stdout = '';
      let stderr = '';

      child.stdout?.on('data', (data) => {
        stdout += data.toString();
      });

      child.stderr?.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        if (code !== 0) {
          resolve({
            status: 'error',
            error: stderr || `Scanner exited with code ${code}`,
          });
          return;
        }

        // Try to parse JSON output
        try {
          const result = JSON.parse(stdout);
          resolve({
            status: 'success',
            results: result,
          });
        } catch {
          // If not JSON, return as text
          resolve({
            status: 'success',
            output: stdout,
          });
        }
      });

      child.on('error', (error) => {
        reject(new Error(`Failed to execute scanner: ${error.message}`));
      });

      // Set timeout
      setTimeout(() => {
        child.kill();
        reject(new Error(`Scanner timed out after ${this.config.timeout} seconds`));
      }, this.config.timeout * 1000);
    });
  }

  /**
   * Create a temporary plugin configuration file
   */
  async createPluginConfig(pluginName: string, config: Record<string, any>): Promise<string> {
    const tempPath = path.join(os.tmpdir(), `tavo-plugin-${pluginName}-${crypto.randomBytes(8).toString('hex')}.json`);
    await fs.writeFile(tempPath, JSON.stringify(config, null, 2));
    return tempPath;
  }

  /**
   * Create a temporary rules file
   */
  async createRulesFile(rules: Record<string, any>): Promise<string> {
    const tempPath = path.join(os.tmpdir(), `tavo-rules-${crypto.randomBytes(8).toString('hex')}.json`);
    await fs.writeFile(tempPath, JSON.stringify(rules, null, 2));
    return tempPath;
  }
}

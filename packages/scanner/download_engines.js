#!/usr/bin/env node

/**
 * Cross-platform engine downloader for Tavo Scanner
 * Downloads OpenGrep and OPA binaries for all platforms
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process');

const ENGINES_DIR = path.join(__dirname, 'engines');
const CACHE_DIR = path.join(require('os').homedir(), '.tavoai', 'engines');

// Ensure directories exist
function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

// Download file with progress and redirect handling
function downloadFile(url, dest) {
    return new Promise((resolve, reject) => {
        console.log(`Downloading from: ${url}`);
        console.log(`To: ${dest}`);

        const makeRequest = (requestUrl) => {
            const request = https.get(requestUrl, (response) => {
                // Handle redirects
                if (response.statusCode === 302 || response.statusCode === 301) {
                    const redirectUrl = response.headers.location;
                    console.log(`Redirecting to: ${redirectUrl}`);
                    return makeRequest(redirectUrl);
                }

                if (response.statusCode !== 200) {
                    reject(new Error(`Failed to download: ${response.statusCode} ${response.statusMessage}`));
                    return;
                }

                const file = fs.createWriteStream(dest);
                response.pipe(file);

                file.on('finish', () => {
                    file.close();
                    console.log(`Downloaded: ${dest}`);
                    resolve();
                });

                file.on('error', (err) => {
                    fs.unlink(dest, () => { }); // Delete the file on error
                    reject(err);
                });
            });

            request.on('error', (err) => {
                fs.unlink(dest, () => { }); // Delete the file on error
                reject(err);
            });
        };

        makeRequest(url);
    });
}

// Extract archives
function extractArchive(archivePath, extractTo) {
    const ext = path.extname(archivePath);

    if (ext === '.zip') {
        // Use Node.js unzip or fallback to system commands
        try {
            console.log(`Extracting zip: ${archivePath}`);
            if (process.platform === 'win32') {
                execSync(`powershell -command "Expand-Archive -Path '${archivePath}' -DestinationPath '${extractTo}' -Force"`, { stdio: 'inherit' });
            } else {
                execSync(`unzip -o "${archivePath}" -d "${extractTo}"`, { stdio: 'inherit' });
            }
        } catch (error) {
            console.log('unzip failed, trying alternative method...');
            // Fallback: try to use 7zip or other tools
            throw error;
        }
    } else if (ext === '.gz' && archivePath.endsWith('.tar.gz')) {
        console.log(`Extracting tar.gz: ${archivePath}`);
        execSync(`tar -xzf "${archivePath}" -C "${extractTo}"`, { stdio: 'inherit' });
    }
}

// Download OpenGrep
async function downloadOpenGrep() {
    console.log('Downloading OpenGrep...');
    const version = '1.10.0';
    const baseUrl = `https://github.com/opengrep/opengrep/releases/download/v${version}`;

    let asset;
    if (process.platform === 'linux') {
        asset = process.arch === 'x64' ? 'opengrep-core_linux_x86.tar.gz' : 'opengrep-core_linux_aarch64.tar.gz';
    } else if (process.platform === 'darwin') {
        asset = process.arch === 'x64' ? 'opengrep-core_osx_x86.tar.gz' : 'opengrep-core_osx_aarch64.tar.gz';
    } else if (process.platform === 'win32') {
        asset = 'opengrep-core_windows_x86.zip';
    } else {
        throw new Error(`Unsupported platform: ${process.platform}-${process.arch}`);
    }

    const url = `${baseUrl}/${asset}`;
    const dest = path.join(CACHE_DIR, asset);

    await downloadFile(url, dest);
    extractArchive(dest, ENGINES_DIR);
}

// Download OPA
async function downloadOPA() {
    console.log('Downloading OPA...');
    const baseUrl = 'https://github.com/open-policy-agent/opa/releases/latest/download';

    let asset;
    if (process.platform === 'linux') {
        asset = process.arch === 'x64' ? 'opa_linux_amd64_static' : 'opa_linux_arm64_static';
    } else if (process.platform === 'darwin') {
        asset = process.arch === 'x64' ? 'opa_darwin_amd64' : 'opa_darwin_arm64_static';
    } else if (process.platform === 'win32') {
        asset = 'opa_windows_amd64.exe';
    } else {
        throw new Error(`Unsupported platform: ${process.platform}-${process.arch}`);
    }

    const url = `${baseUrl}/${asset}`;
    const dest = path.join(ENGINES_DIR, process.platform === 'win32' ? 'opa.exe' : 'opa');

    await downloadFile(url, dest);

    // Make executable on Unix systems
    if (process.platform !== 'win32') {
        fs.chmodSync(dest, '755');
    }
}

// Main function
async function main() {
    try {
        console.log(`Platform: ${process.platform}-${process.arch}`);
        console.log(`Engines dir: ${ENGINES_DIR}`);
        console.log(`Cache dir: ${CACHE_DIR}`);

        ensureDir(ENGINES_DIR);
        ensureDir(CACHE_DIR);

        await downloadOpenGrep();
        await downloadOPA();

        console.log('All engines downloaded successfully!');
        console.log('Contents of engines directory:');
        const files = fs.readdirSync(ENGINES_DIR);
        files.forEach(file => {
            const fullPath = path.join(ENGINES_DIR, file);
            const stats = fs.statSync(fullPath);
            console.log(`  ${file} (${stats.size} bytes)`);
        });

    } catch (error) {
        console.error('Error downloading engines:', error.message);
        process.exit(1);
    }
}

main();
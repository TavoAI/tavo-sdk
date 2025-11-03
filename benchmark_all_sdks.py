#!/usr/bin/env python3
"""
SDK Performance Benchmarking Script
Tests all SDKs for basic functionality and performance metrics
"""

import time
import asyncio
import subprocess
import sys
from pathlib import Path

class SDKBenchmarker:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.results = {}

    async def run_python_benchmark(self):
        """Benchmark Python SDK"""
        print("🐍 Running Python SDK benchmark...")

        try:
            # Import and test basic functionality
            start_time = time.time()

            # Test import time
            import_time = time.time()
            from tavo.client import TavoClient
            import_time = time.time() - import_time

            # Test client creation
            creation_time = time.time()
            client = TavoClient(api_key="benchmark-key")
            creation_time = time.time() - creation_time

            # Test operation access
            access_time = time.time()
            device_ops = client.device()
            scanner_ops = client.scanner()
            code_ops = client.code_submission()
            access_time = time.time() - access_time

            total_time = time.time() - start_time

            self.results['python'] = {
                'status': 'SUCCESS',
                'import_time': import_time,
                'creation_time': creation_time,
                'access_time': access_time,
                'total_time': total_time,
                'operations_available': 16
            }

        except Exception as e:
            self.results['python'] = {
                'status': 'FAILED',
                'error': str(e)
            }

    def run_javascript_benchmark(self):
        """Benchmark JavaScript/TypeScript SDK"""
        print("📄 Running JavaScript SDK benchmark...")

        try:
            # Check if node_modules exists
            js_dir = self.base_dir / "packages" / "javascript"
            if not (js_dir / "node_modules").exists():
                print("  ⚠️  JavaScript dependencies not installed, skipping...")
                self.results['javascript'] = {
                    'status': 'SKIPPED',
                    'reason': 'Dependencies not installed'
                }
                return

            # Run test command
            start_time = time.time()
            result = subprocess.run(
                ["npm", "test"],
                cwd=js_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            total_time = time.time() - start_time

            if result.returncode == 0:
                self.results['javascript'] = {
                    'status': 'SUCCESS',
                    'total_time': total_time,
                    'tests_passed': result.stdout.count('✓') if '✓' in result.stdout else 'unknown'
                }
            else:
                self.results['javascript'] = {
                    'status': 'FAILED',
                    'error': result.stderr,
                    'total_time': total_time
                }

        except subprocess.TimeoutExpired:
            self.results['javascript'] = {
                'status': 'TIMEOUT',
                'error': 'Test execution timed out'
            }
        except Exception as e:
            self.results['javascript'] = {
                'status': 'ERROR',
                'error': str(e)
            }

    def run_java_benchmark(self):
        """Benchmark Java SDK"""
        print("☕ Running Java SDK benchmark...")

        try:
            java_dir = self.base_dir / "packages" / "java"

            start_time = time.time()
            result = subprocess.run(
                ["mvn", "test", "-q"],
                cwd=java_dir,
                capture_output=True,
                text=True,
                timeout=60
            )

            total_time = time.time() - start_time

            if result.returncode == 0:
                # Parse test results
                output = result.stdout + result.stderr
                tests_run = output.count("Tests run:")
                if tests_run > 0:
                    # Extract test count from Maven output
                    lines = output.split('\n')
                    tests_run = "unknown"
                    failures = 0
                    for line in lines:
                        if "Tests run:" in line:
                            parts = line.split(',')
                            tests_run = int(parts[0].split(':')[1].strip())
                            failures = int(parts[1].split(':')[1].strip())
                            break

                self.results['java'] = {
                    'status': 'SUCCESS',
                    'total_time': total_time,
                    'tests_run': tests_run,
                    'failures': failures
                }
            else:
                self.results['java'] = {
                    'status': 'FAILED',
                    'error': result.stderr,
                    'total_time': total_time
                }

        except subprocess.TimeoutExpired:
            self.results['java'] = {
                'status': 'TIMEOUT',
                'error': 'Test execution timed out'
            }
        except Exception as e:
            self.results['java'] = {
                'status': 'ERROR',
                'error': str(e)
            }

    def run_go_benchmark(self):
        """Benchmark Go SDK"""
        print("🔵 Running Go SDK benchmark...")

        try:
            go_dir = self.base_dir / "packages" / "go"

            start_time = time.time()
            result = subprocess.run(
                ["go", "test", "./..."],
                cwd=go_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            total_time = time.time() - start_time

            if result.returncode == 0:
                self.results['go'] = {
                    'status': 'SUCCESS',
                    'total_time': total_time,
                    'output': result.stdout.strip()
                }
            else:
                self.results['go'] = {
                    'status': 'FAILED',
                    'error': result.stderr,
                    'total_time': total_time
                }

        except subprocess.TimeoutExpired:
            self.results['go'] = {
                'status': 'TIMEOUT',
                'error': 'Test execution timed out'
            }
        except Exception as e:
            self.results['go'] = {
                'status': 'ERROR',
                'error': str(e)
            }

    def run_rust_benchmark(self):
        """Benchmark Rust SDK"""
        print("🦀 Running Rust SDK benchmark...")

        try:
            rust_dir = self.base_dir / "packages" / "rust"

            start_time = time.time()
            result = subprocess.run(
                ["cargo", "test"],
                cwd=rust_dir,
                capture_output=True,
                text=True,
                timeout=60
            )

            total_time = time.time() - start_time

            if result.returncode == 0:
                # Count tests
                output = result.stdout
                test_lines = [line for line in output.split('\n') if 'test result:' in line]
                total_tests = 0
                for line in test_lines:
                    if 'passed' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == 'passed':
                                total_tests += int(parts[i-1])
                                break

                self.results['rust'] = {
                    'status': 'SUCCESS',
                    'total_time': total_time,
                    'tests_passed': total_tests
                }
            else:
                self.results['rust'] = {
                    'status': 'FAILED',
                    'error': result.stderr,
                    'total_time': total_time
                }

        except subprocess.TimeoutExpired:
            self.results['rust'] = {
                'status': 'TIMEOUT',
                'error': 'Test execution timed out'
            }
        except Exception as e:
            self.results['rust'] = {
                'status': 'ERROR',
                'error': str(e)
            }

    def run_dotnet_benchmark(self):
        """Benchmark .NET SDK"""
        print("🔷 Running .NET SDK benchmark...")

        try:
            dotnet_dir = self.base_dir / "packages" / "dotnet"

            start_time = time.time()
            result = subprocess.run(
                ["dotnet", "test", "--verbosity", "quiet"],
                cwd=dotnet_dir,
                capture_output=True,
                text=True,
                timeout=30
            )

            total_time = time.time() - start_time

            if result.returncode == 0:
                self.results['dotnet'] = {
                    'status': 'SUCCESS',
                    'total_time': total_time,
                    'output': result.stdout.strip()
                }
            else:
                self.results['dotnet'] = {
                    'status': 'FAILED',
                    'error': result.stderr,
                    'total_time': total_time
                }

        except subprocess.TimeoutExpired:
            self.results['dotnet'] = {
                'status': 'TIMEOUT',
                'error': 'Test execution timed out'
            }
        except Exception as e:
            self.results['dotnet'] = {
                'status': 'ERROR',
                'error': str(e)
            }

    def print_report(self):
        """Print comprehensive benchmark report"""
        print("\n" + "="*80)
        print("🚀 SDK PERFORMANCE BENCHMARK REPORT")
        print("="*80)

        status_emojis = {
            'SUCCESS': '✅',
            'FAILED': '❌',
            'ERROR': '💥',
            'TIMEOUT': '⏰',
            'SKIPPED': '⚠️'
        }

        for sdk, result in self.results.items():
            status = result['status']
            emoji = status_emojis.get(status, '❓')

            print(f"\n{emoji} {sdk.upper()} SDK")
            print("-" * (len(sdk) + 5))

            if status == 'SUCCESS':
                total_time = result.get('total_time', 0)
                print(f"  Total Time: {total_time:.2f}s")
                if 'import_time' in result:
                    print(f"  Import Time: {result['import_time']:.3f}s")
                if 'creation_time' in result:
                    print(f"  Creation Time: {result['creation_time']:.3f}s")
                if 'access_time' in result:
                    print(f"  Access Time: {result['access_time']:.3f}s")
                if 'tests_run' in result:
                    print(f"  Tests Run: {result['tests_run']}")
                if 'tests_passed' in result:
                    print(f"  Tests Passed: {result['tests_passed']}")
                if 'operations_available' in result:
                    print(f"  Operations Available: {result['operations_available']}")

            elif status in ['FAILED', 'ERROR', 'TIMEOUT']:
                print(f"  Error: {result.get('error', 'Unknown error')}")
                if 'total_time' in result:
                    print(f"  Total Time: {result['total_time']:.2f}s")

            elif status == 'SKIPPED':
                print(f"  Reason: {result.get('reason', 'Unknown reason')}")

        # Summary
        successful = sum(1 for r in self.results.values() if r['status'] == 'SUCCESS')
        total = len(self.results)

        print(f"\n{'='*80}")
        print(f"📊 SUMMARY: {successful}/{total} SDKs completed successfully")
        print(f"{'='*80}")

        if successful == total:
            print("🎉 ALL SDKs PASSED performance benchmarking!")
        else:
            print(f"⚠️  {total - successful} SDK(s) had issues")

    async def run_all_benchmarks(self):
        """Run all SDK benchmarks"""
        print("🚀 Starting SDK Performance Benchmarking")
        print("Testing all 6 SDKs for functionality and performance...")

        # Run Python benchmark (async)
        await self.run_python_benchmark()

        # Run other benchmarks (sync)
        self.run_javascript_benchmark()
        self.run_java_benchmark()
        self.run_go_benchmark()
        self.run_rust_benchmark()
        self.run_dotnet_benchmark()

        # Print comprehensive report
        self.print_report()

async def main():
    benchmarker = SDKBenchmarker()
    await benchmarker.run_all_benchmarks()

if __name__ == "__main__":
    asyncio.run(main())

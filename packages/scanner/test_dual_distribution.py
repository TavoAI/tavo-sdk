#!/usr/bin/env python3
"""
Test script for dual distribution functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the scanner package to the path
sys.path.insert(0, str(Path(__file__).parent))

from dual_distribution_manager import (
    DualDistributionManager,
    BundleMetadata,
    BundleSource,
)


async def test_dual_distribution():
    """Test the dual distribution manager"""
    print("Testing Dual Distribution Manager...")

    # Create dual distribution manager
    manager = DualDistributionManager()

    # Test bundle listing
    print("\n1. Testing bundle listing:")
    bundles = manager.list_available_bundles()
    print(f"Available bundles: {len(bundles)}")
    for bundle in bundles:
        print(f"  - {bundle.id}: {bundle.name} ({bundle.pricing_tier})")

    # Test API key detection
    print("\n2. Testing API key detection:")
    has_key = manager.has_api_key()
    print(f"API key available: {has_key}")

    can_access_registry = manager.can_access_registry()
    print(f"Can access registry: {can_access_registry}")

    # Test bundle info retrieval
    print("\n3. Testing bundle info:")
    for bundle_id in ["owasp-llm-basic", "owasp-llm-pro"]:
        info = manager.get_bundle_info(bundle_id)
        if info:
            print(f"  {bundle_id}: {info.name} - {info.pricing_tier}")
            print(f"    Requires API key: {info.source.requires_api_key}")
        else:
            print(f"  {bundle_id}: Not found")

    # Test access messages
    print("\n4. Testing access messages:")
    for bundle_id in ["owasp-llm-basic", "owasp-llm-pro"]:
        message = manager.show_access_message(bundle_id)
        print(f"  {bundle_id}: {message}")

    print("\n✅ Dual distribution tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_dual_distribution())

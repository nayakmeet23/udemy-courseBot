#!/usr/bin/env python3
"""
Test script to check internet connectivity and website access
"""
import aiohttp
import asyncio
import requests
from urllib.parse import urlparse

def test_basic_connectivity():
    """Test basic internet connectivity"""
    print("=== Testing Basic Internet Connectivity ===")
    try:
        # Test basic internet connectivity
        response = requests.get("https://www.google.com", timeout=10)
        print(f"✓ Internet connectivity: OK (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"✗ Internet connectivity: FAILED - {type(e).__name__}: {e}")
        return False

def test_discudemy_access():
    """Test access to DiscUdemy"""
    print("\n=== Testing DiscUdemy Access ===")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        }
        response = requests.get("https://www.discudemy.com/all/1", headers=headers, timeout=15)
        print(f"✓ DiscUdemy access: OK (Status: {response.status_code})")
        if response.status_code == 200:
            print(f"  Content length: {len(response.text)} characters")
            if "card-header" in response.text:
                print("  ✓ Found course links in HTML")
            else:
                print("  ⚠ Course links not found in HTML (site structure may have changed)")
        return True
    except Exception as e:
        print(f"✗ DiscUdemy access: FAILED - {type(e).__name__}: {e}")
        return False

def test_yofreesamples_access():
    """Test access to YoFreeSamples"""
    print("\n=== Testing YoFreeSamples Access ===")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
        }
        response = requests.get("https://yofreesamples.com/courses/free-discounted-udemy-courses-list/", headers=headers, timeout=15)
        print(f"✓ YoFreeSamples access: OK (Status: {response.status_code})")
        if response.status_code == 200:
            print(f"  Content length: {len(response.text)} characters")
            if "wp-block-kadence-rowlayout" in response.text:
                print("  ✓ Found course containers in HTML")
            else:
                print("  ⚠ Course containers not found in HTML (site structure may have changed)")
        return True
    except Exception as e:
        print(f"✗ YoFreeSamples access: FAILED - {type(e).__name__}: {e}")
        return False

async def test_async_connectivity():
    """Test async connectivity using aiohttp"""
    print("\n=== Testing Async Connectivity (aiohttp) ===")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.discudemy.com/all/1", timeout=aiohttp.ClientTimeout(total=10), ssl=False) as resp:
                print(f"✓ Async DiscUdemy access: OK (Status: {resp.status})")
                content = await resp.read()
                print(f"  Content length: {len(content)} bytes")
                return True
    except Exception as e:
        print(f"✗ Async DiscUdemy access: FAILED - {type(e).__name__}: {e}")
        return False

def check_libraries():
    """Check if required libraries are installed and up to date"""
    print("\n=== Checking Required Libraries ===")
    
    try:
        import aiohttp
        print(f"✓ aiohttp: {aiohttp.__version__}")
    except ImportError:
        print("✗ aiohttp: NOT INSTALLED")
        print("  Install with: pip install aiohttp")
    
    try:
        import lxml
        print(f"✓ lxml: {lxml.__version__}")
    except ImportError:
        print("✗ lxml: NOT INSTALLED")
        print("  Install with: pip install lxml")
    
    try:
        import requests
        print(f"✓ requests: {requests.__version__}")
    except ImportError:
        print("✗ requests: NOT INSTALLED")
        print("  Install with: pip install requests")

def main():
    """Run all tests"""
    print("🔍 UdemyPy Connection Diagnostic Tool")
    print("=" * 50)
    
    # Check libraries first
    check_libraries()
    
    # Test basic connectivity
    internet_ok = test_basic_connectivity()
    
    if internet_ok:
        # Test website access
        discudemy_ok = test_discudemy_access()
        yofreesamples_ok = test_yofreesamples_access()
        
        # Test async connectivity
        asyncio.run(test_async_connectivity())
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 SUMMARY:")
        print(f"  Internet: {'✓' if internet_ok else '✗'}")
        print(f"  DiscUdemy: {'✓' if discudemy_ok else '✗'}")
        print(f"  YoFreeSamples: {'✓' if yofreesamples_ok else '✗'}")
        
        if not discudemy_ok:
            print("\n💡 SUGGESTIONS for DiscUdemy issues:")
            print("  1. Try using a VPN")
            print("  2. Check if the site is down: https://www.discudemy.com")
            print("  3. Try different user agents")
            print("  4. Check firewall/proxy settings")
    else:
        print("\n💡 SUGGESTIONS for internet issues:")
        print("  1. Check your internet connection")
        print("  2. Try accessing other websites")
        print("  3. Check firewall settings")
        print("  4. Try using a different network")

if __name__ == "__main__":
    main() 
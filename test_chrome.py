#!/usr/bin/env python3
"""
Simple test script to diagnose Chrome/Selenium issues
"""

import sys
import traceback

def test_imports():
    """Test if we can import required modules"""
    print("Testing imports...")
    try:
        from selenium import webdriver
        print("✅ Selenium imported successfully")
        
        from selenium.webdriver.chrome.service import Service
        print("✅ Chrome Service imported successfully")
        
        from selenium.webdriver.chrome.options import Options
        print("✅ Chrome Options imported successfully")
        
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ ChromeDriverManager imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_chrome_driver():
    """Test Chrome driver setup"""
    print("\nTesting Chrome driver setup...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        print("Setting up ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        print("✅ ChromeDriver setup successful")
        
        return service, chrome_options
    except Exception as e:
        print(f"❌ ChromeDriver setup error: {e}")
        traceback.print_exc()
        return None, None

def test_browser_launch():
    """Test launching the browser"""
    print("\nTesting browser launch...")
    try:
        service, chrome_options = test_chrome_driver()
        if not service:
            return False
        
        from selenium import webdriver
        
        print("Launching Chrome browser...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Chrome browser launched successfully!")
        
        print("Navigating to Google...")
        driver.get("https://www.google.com")
        print(f"✅ Page loaded: {driver.title}")
        
        print("Closing browser in 5 seconds...")
        import time
        time.sleep(5)
        driver.quit()
        print("✅ Browser closed successfully")
        
        return True
    except Exception as e:
        print(f"❌ Browser launch error: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔍 Chrome/Selenium Diagnostic Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please check your installation.")
        return
    
    # Test Chrome driver
    service, options = test_chrome_driver()
    if not service:
        print("\n❌ ChromeDriver test failed.")
        return
    
    # Test browser launch
    if not test_browser_launch():
        print("\n❌ Browser launch test failed.")
        return
    
    print("\n✅ All tests passed! Chrome should work with your automation script.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        traceback.print_exc()

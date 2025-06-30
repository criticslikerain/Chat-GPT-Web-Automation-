import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class CloudflareBypassChatGPT:
    def __init__(self, headless=False):
        # Gi setup nako ni para sa advanced Cloudflare bypass
        # Medyo komplikado ni pero effective kaayo based sa akong testing
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        # Diri nako gi setup ang Chrome with advanced Cloudflare bypass
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")  # Invisible mode

        # Mga advanced arguments para ma bypass ang Cloudflare - gikan ni sa deep research
        chrome_options.add_argument("--no-sandbox")  # Security bypass
        chrome_options.add_argument("--disable-dev-shm-usage")  # Memory optimization
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Main bypass trick
        chrome_options.add_argument("--disable-web-security")  # Disable security checks
        chrome_options.add_argument("--allow-running-insecure-content")  # Allow HTTP
        chrome_options.add_argument("--disable-extensions")  # No extensions
        chrome_options.add_argument("--disable-plugins")  # No plugins
        chrome_options.add_argument("--disable-gpu")  # GPU off
        chrome_options.add_argument("--no-first-run")  # Skip setup
        chrome_options.add_argument("--no-default-browser-check")  # Skip checks
        chrome_options.add_argument("--disable-default-apps")  # No default apps
        chrome_options.add_argument("--disable-popup-blocking")  # Allow popups
        chrome_options.add_argument("--disable-translate")  # No translation
        chrome_options.add_argument("--disable-background-timer-throttling")  # Performance
        chrome_options.add_argument("--disable-renderer-backgrounding")  # Keep active
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")  # Window mgmt
        chrome_options.add_argument("--disable-ipc-flooding-protection")  # IPC optimization
        chrome_options.add_argument("--disable-hang-monitor")  # No hang detection
        chrome_options.add_argument("--disable-client-side-phishing-detection")  # No phishing check
        chrome_options.add_argument("--disable-component-update")  # No auto updates
        chrome_options.add_argument("--disable-domain-reliability")  # No domain tracking
        chrome_options.add_argument("--disable-features=TranslateUI")  # No translate UI
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")  # Display optimization
        
        # Mga realistic user agents - gi rotate nako para dili ma detect
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")  # Random user agent

        # Experimental options para maximum stealth - gikan ni sa mga hacker forums
        chrome_options.add_experimental_option("excludeSwitches", [
            "enable-automation",  # Main automation flag
            "enable-logging",     # Disable logging
            "enable-blink-features=AutomationControlled"  # Blink automation
        ])
        chrome_options.add_experimental_option('useAutomationExtension', False)  # Very important!
        chrome_options.add_experimental_option("detach", True)  # Keep browser open

        # Advanced preferences para mas realistic ang browser behavior
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,    # Block notifications
                "media_stream": 2,     # Block camera/mic
                "geolocation": 2,      # Block location
                "camera": 2,           # Block camera
                "microphone": 2,       # Block microphone
            },
            "profile.managed_default_content_settings": {
                "images": 1  # Allow images para mas realistic
            },
            "profile.default_content_settings": {
                "popups": 0  # Allow popups
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        print("🛡️ Starting chrome with advanced Cloudflare bypass...")

        try:
            # Una nga method - system ChromeDriver
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Success! Chrome has started!")

        except Exception as e1:
            try:
                # Fallback method - automatic download
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service

                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ Success! Chrome with webdriver-manager has started!")

            except Exception as e2:
                print(f"❌ Failed to start Chrome: {e2}")
                raise Exception("Dili ma start ang Chrome browser")

        # I-apply ang advanced anti-detection scripts
        self.apply_stealth_scripts()
        
    def apply_stealth_scripts(self):
        """Apply comprehensive stealth scripts to bypass detection"""
        print("🔧 Applying stealth scripts...")
        
        # Remove webdriver traces
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        # Override plugins
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        """)
        
        # Override languages
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        """)
        
        # Add chrome runtime
        self.driver.execute_script("""
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
        """)
        
        # Override permissions
        self.driver.execute_script("""
            const originalQuery = window.navigator.permissions.query;
            return window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)
        
        # Mock WebGL
        self.driver.execute_script("""
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';
                }
                return getParameter(parameter);
            };
        """)
        
        # Override screen properties
        self.driver.execute_script("""
            Object.defineProperty(screen, 'colorDepth', {
                get: () => 24,
            });
            Object.defineProperty(screen, 'pixelDepth', {
                get: () => 24,
            });
        """)
        
        print("✅ Stealth scripts applied!")
    
    def human_like_delay(self, min_delay=0.5, max_delay=2.0):
        """Add human-like random delays"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        return delay
    
    def simulate_human_movement(self):
        """Simulate human mouse movements"""
        try:
            actions = ActionChains(self.driver)
            
            # Random mouse movements
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                actions.move_by_offset(x, y)
                actions.pause(random.uniform(0.1, 0.3))
            
            actions.perform()
            self.human_like_delay(0.2, 0.8)
            
        except Exception:
            pass  # Ignore errors in mouse simulation
    
    def visit_chatgpt(self):
        """Navigate to ChatGPT with maximum stealth"""
        print("🌐 Navigating to ChatGPT with stealth mode...")
        
        # Random pre-navigation delay
        delay = self.human_like_delay(2, 5)
        print(f"⏳ Pre-navigation delay: {delay:.1f}s")
        
        # Navigate to ChatGPT
        self.driver.get("https://chat.openai.com")
        
        # Wait for initial load
        load_delay = self.human_like_delay(3, 8)
        print(f"⏳ Page loading delay: {load_delay:.1f}s")
        
        # Simulate human behavior
        print("🖱️ Simulating human interactions...")
        self.simulate_human_movement()
        
        # Random scrolling
        scroll_amount = random.randint(50, 200)
        self.driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
        self.human_like_delay(0.5, 1.5)
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.human_like_delay(0.3, 1.0)
        
        print("✅ ChatGPT loaded with stealth techniques!")
    
    def wait_for_input_ready(self, timeout=30):
        """Wait for input field with human-like behavior"""
        print("🔍 Looking for input field...")
        
        selectors = [
            "textarea[placeholder*='Message']",
            "textarea[data-id='root']", 
            "#prompt-textarea",
            "textarea",
            "[contenteditable='true']",
            "div[contenteditable='true']"
        ]
        
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                print(f"✅ Found input field: {selector}")
                return element
            except TimeoutException:
                continue
        
        print("❌ Could not find input field")
        return None
    
    def human_type(self, element, text):
        """Type text with human-like characteristics"""
        print("⌨️ Typing with human-like behavior...")
        
        for char in text:
            element.send_keys(char)
            # Variable typing speed (30-200ms per character)
            delay = random.uniform(0.03, 0.2)
            
            # Occasional longer pauses (like thinking)
            if random.random() < 0.1:  # 10% chance
                delay += random.uniform(0.2, 0.8)
            
            time.sleep(delay)
    
    def send_message(self, message):
        """Send message with maximum human-like behavior"""
        print(f"📝 Preparing to send: {message}")
        
        input_field = self.wait_for_input_ready()
        if not input_field:
            return False
        
        # Clear field
        input_field.clear()
        self.human_like_delay(0.3, 0.8)
        
        # Human-like typing
        self.human_type(input_field, message)
        
        # Thinking pause before sending
        thinking_delay = self.human_like_delay(0.8, 3.0)
        print(f"🤔 Thinking pause: {thinking_delay:.1f}s")
        
        # Send message
        input_field.send_keys(Keys.RETURN)
        print("✅ Message sent!")
        
        return True
    
    def wait_for_response(self, timeout=60):
        """Wait for ChatGPT response"""
        print("⏳ Waiting for response...")
        
        response_selectors = [
            "[data-message-author-role='assistant']",
            ".markdown",
            "[class*='response']",
            "[class*='message']"
        ]
        
        start_time = time.time()
        last_length = 0
        stable_count = 0
        
        while time.time() - start_time < timeout:
            for selector in response_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        response = elements[-1].text.strip()
                        
                        if response and len(response) > 10:
                            if len(response) == last_length:
                                stable_count += 1
                                if stable_count >= 3:
                                    print("✅ Response complete!")
                                    return response
                            else:
                                stable_count = 0
                                last_length = len(response)
                                print(f"📝 Response: {len(response)} chars...")
                except Exception:
                    continue
            
            time.sleep(2)
        
        return "No response received"
    
    def ask_question(self, question):
        """Ask question with full stealth"""
        if self.send_message(question):
            return self.wait_for_response()
        return "Failed to send message"
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def main():
    """Main function with Cloudflare bypass"""
    bot = None
    try:
        print("🛡️ Starting ChatGPT with Cloudflare Bypass")
        print("=" * 50)
        
        bot = CloudflareBypassChatGPT(headless=False)
        bot.visit_chatgpt()
        
        print("\n🔑 Please log in manually and press Enter when ready...")
        input()
        
        print("\n🤖 Automation ready with Cloudflare bypass!")
        
        while True:
            question = input("\n💬 Your question: ")
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            if question.strip():
                print(f"\n{'='*60}")
                response = bot.ask_question(question)
                print(f"🤖 Response: {response}")
                print("="*60)
    
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if bot:
            bot.close()

if __name__ == "__main__":
    main()

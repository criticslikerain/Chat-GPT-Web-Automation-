import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ChatGPTAutomation:
    def __init__(self, headless=False):
        # Oy, gi setup nako ni para sa ChatGPT automation
        # Nindot kaayo ni siya, tested na nako sa akong laptop
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        # Diri nako gi setup ang Chrome browser, medyo lisod ni pero nindot ang result
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")  # Invisible mode, para dili makita

        # Mga settings para ma bypass ang Cloudflare - gikan ni sa research nako
        chrome_options.add_argument("--no-sandbox")  # Security bypass, needed ni
        chrome_options.add_argument("--disable-dev-shm-usage")  # Memory optimization
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Main trick para dili ma detect
        chrome_options.add_argument("--disable-web-security")  # Disable security checks
        chrome_options.add_argument("--allow-running-insecure-content")  # Allow HTTP content
        chrome_options.add_argument("--disable-extensions")  # No extensions para mas stealth
        chrome_options.add_argument("--disable-plugins")  # Disable plugins
        chrome_options.add_argument("--disable-gpu")  # GPU acceleration off
        chrome_options.add_argument("--no-first-run")  # Skip first run setup
        chrome_options.add_argument("--no-default-browser-check")  # Skip default browser check
        chrome_options.add_argument("--disable-default-apps")  # No default apps
        chrome_options.add_argument("--disable-popup-blocking")  # Allow popups
        chrome_options.add_argument("--disable-translate")  # No translation bar
        chrome_options.add_argument("--disable-background-timer-throttling")  # Performance tweak
        chrome_options.add_argument("--disable-renderer-backgrounding")  # Keep renderer active
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")  # Window management
        chrome_options.add_argument("--disable-ipc-flooding-protection")  # IPC optimization

        # User agent para murag real browser - gi copy nako ni sa akong Chrome
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Mga experimental options - gikan ni sa mga tutorial sa YouTube
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)  # Very important ni!
        chrome_options.add_experimental_option("detach", True)  # Keep browser open

        # Additional preferences para mas realistic ang browser
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,  # Block notifications
                "media_stream": 2,   # Block camera/mic
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        print("Gi try nako i-start ang Chrome browser with Cloudflare bypass...")

        try:
            # Una nga method - gamiton ang system ChromeDriver kung naa
            print("Method 1: Gi try nako ang system ChromeDriver...")
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Success! Na start na ang Chrome with system driver!")

        except Exception as e1:
            print(f"Method 1 failed: {e1}")

            try:
                # Ika-duha nga method - automatic download sa ChromeDriver
                print("Method 2: Gi try nako ang webdriver-manager...")
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service

                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ Success! Na start na ang Chrome with webdriver-manager!")

            except Exception as e2:
                print(f"Method 2 failed: {e2}")
                print("❌ Dili ma start ang Chrome browser.")
                print("\nPossible solutions:")
                print("1. I-check kung naa ba ang Google Chrome sa imong computer")
                print("2. Download manually ang ChromeDriver gikan sa: https://chromedriver.chromium.org/")
                print("3. I-add ang ChromeDriver sa imong PATH")
                raise Exception("Failed to start Chrome browser")
        
        # Mga advanced scripts para ma bypass ang detection - gikan ni sa research nako
        if self.driver:
            print("🛡️ Gi apply nako ang mga Cloudflare bypass techniques...")

            # Tanggalon ang webdriver property - main trick ni para dili ma detect
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # I-override ang plugins property para murag real browser
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")

            # I-set ang languages para murag gikan sa US
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")

            # I-add ang chrome property kay wala ni sa automation
            self.driver.execute_script("window.chrome = {runtime: {}}")

            # I-mock ang permissions para realistic
            self.driver.execute_script("Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})")

            # WebGL spoofing - para dili ma fingerprint ang hardware
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

            print("✅ Success! Na apply na ang mga Cloudflare bypass techniques!")
        
    def visit_chatgpt(self):
        # Moadto na ta sa ChatGPT website with human-like behavior
        print("Moadto na ta sa ChatGPT...")

        # Random delay para murag human ang behavior - gi research nako ni
        import random
        delay = random.uniform(2, 4)
        print(f"⏳ Maghulat ta og {delay:.1f}s before navigation (para murag human)...")
        time.sleep(delay)

        self.driver.get("https://chat.openai.com")

        # Maghulat para ma load ang page with random delay
        load_delay = random.uniform(3, 7)
        print(f"⏳ Nag load ang page... maghulat ta og {load_delay:.1f}s")
        time.sleep(load_delay)

        # I-simulate ang human scrolling behavior
        print("🖱️ Gi simulate nako ang human behavior...")
        self.driver.execute_script("window.scrollTo(0, 100);")  # Scroll down gamay
        time.sleep(random.uniform(0.5, 1.5))
        self.driver.execute_script("window.scrollTo(0, 0);")    # Balik sa top
        time.sleep(random.uniform(0.5, 1.0))

        print("✅ Success! Na load na ang ChatGPT page!")
        
    def wait_for_input_ready(self, timeout=30):
        # Maghulat ta para ready na ang input field
        print("Nangita ko sa input field...")
        try:
            # Mga different selectors nga gi try nako - gikan ni sa inspection sa ChatGPT
            selectors = [
                "textarea[placeholder*='Message']",  # Most common ni
                "textarea[data-id='root']",          # Alternative selector
                "#prompt-textarea",                  # ID-based selector
                "textarea",                          # Generic textarea
                "[contenteditable='true']",          # Contenteditable div
                "div[contenteditable='true']"        # Div version
            ]

            for selector in selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    print(f"✅ Nakit-an nako ang input field with selector: {selector}")
                    return element
                except TimeoutException:
                    continue  # Try next selector

            raise TimeoutException("Wala nakit-an ang input field")

        except TimeoutException:
            print("❌ Timeout - wala nakit-an ang input field")
            print("Current page title:", self.driver.title)
            print("Current URL:", self.driver.current_url)
            return None
    
    def send_message(self, message):
        # I-send ang message sa ChatGPT with human-like typing
        print(f"📝 Gi send nako ni: {message}")

        # Maghulat para ready na ang input field
        input_field = self.wait_for_input_ready()
        if not input_field:
            print("❌ Wala nakit-an ang input field")
            return False

        # I-clear ang existing text
        input_field.clear()
        time.sleep(0.5)  # Gamay nga delay

        # I-type ang message with human-like delays - para dili ma detect nga bot
        print("⌨️ Nag type ko with human-like speed...")
        import random
        for char in message:
            input_field.send_keys(char)
            # Random delay between keystrokes (50-150ms) - murag real typing
            time.sleep(random.uniform(0.05, 0.15))

        # Random pause before sending (murag nag think pa ang human)
        thinking_delay = random.uniform(0.5, 2.0)
        print(f"🤔 Nag pause ko og {thinking_delay:.1f}s before sending...")
        time.sleep(thinking_delay)

        # I-send ang message (Enter key)
        input_field.send_keys(Keys.RETURN)

        print("✅ Success! Na send na ang message!")
        return True
    
    def wait_for_response(self, timeout=60):
        """
        Wait for ChatGPT to respond and return the response text
        
        Args:
            timeout (int): Maximum time to wait for response
            
        Returns:
            str: The response text from ChatGPT
        """
        print("⏳ Waiting for ChatGPT response...")
        
        try:
            # Wait a moment for the response to start generating
            time.sleep(3)
            
            # Look for response containers
            response_selectors = [
                "[data-message-author-role='assistant']",
                ".markdown",
                "[class*='response']",
                "[class*='message']",
                "div[class*='group']"
            ]
            
            start_time = time.time()
            last_response_length = 0
            stable_count = 0
            
            while time.time() - start_time < timeout:
                for selector in response_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            # Get the last response (most recent)
                            last_response = elements[-1]
                            response_text = last_response.text.strip()
                            
                            if response_text and len(response_text) > 10:
                                # Check if response has stopped growing (indicating completion)
                                if len(response_text) == last_response_length:
                                    stable_count += 1
                                    if stable_count >= 3:  # Response stable for 3 checks
                                        print("✅ Response received and appears complete!")
                                        return response_text
                                else:
                                    stable_count = 0
                                    last_response_length = len(response_text)
                                    print(f"📝 Response growing... ({len(response_text)} characters)")
                    except Exception as e:
                        continue
                
                time.sleep(2)  # Wait before checking again
            
            print("⏰ Timeout waiting for response")
            return "No response received within timeout period"
            
        except Exception as e:
            print(f"❌ Error waiting for response: {e}")
            return f"Error: {e}"
    
    def ask_question(self, question):
        """
        Ask a question to ChatGPT and get the response
        
        Args:
            question (str): The question to ask
            
        Returns:
            str: ChatGPT's response
        """
        if self.send_message(question):
            return self.wait_for_response()
        else:
            return "Failed to send message"
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def main():
    """Main function to run the ChatGPT automation"""
    bot = None
    try:
        print("🚀 Starting ChatGPT Automation...")
        print("Note: You may need to log in to ChatGPT manually when the browser opens.")
        
        # Initialize the bot
        bot = ChatGPTAutomation(headless=False)  # Set to True for headless mode
        
        # Visit ChatGPT
        bot.visit_chatgpt()
        
        # Wait for user to log in manually
        print("\n" + "="*60)
        print("🔑 MANUAL LOGIN TIME")
        print("="*60)
        print("👆 A Chrome browser window should have opened with ChatGPT")
        print("")
        print("📋 Please complete these steps:")
        print("   1. 🔐 Log in to your ChatGPT account (if not already logged in)")
        print("   2. 🤖 Complete any CAPTCHA or verification if required")
        print("   3. 💬 Make sure you're on the main chat page (where you can type messages)")
        print("   4. ✅ Come back here and press Enter when ready")
        print("")
        print("💡 Tip: Leave this terminal window open and switch to the browser")
        print("="*60)

        # Wait for user confirmation
        input("Press Enter when you're logged in and ready to start automation... ")

        print("\n🔄 Checking if ChatGPT is ready...")
        time.sleep(2)
        
        # Interactive loop
        print("\n" + "🎉"*20)
        print("🤖 CHATGPT AUTOMATION IS NOW READY!")
        print("🎉"*20)
        print("\n📝 How it works:")
        print("   • Type your question below")
        print("   • The automation will send it to ChatGPT")
        print("   • ChatGPT's response will appear here")
        print("   • Type 'quit' when you're done")
        print("\n" + "-" * 60)

        question_count = 0

        while True:
            question_count += 1
            print(f"\n💬 Question #{question_count}:")
            user_question = input("➤ ")

            if user_question.lower() in ['quit', 'exit', 'q', 'stop']:
                print("\n👋 Thanks for using ChatGPT automation!")
                break

            if user_question.strip():
                print(f"\n{'='*70}")
                print(f"📤 SENDING TO CHATGPT: {user_question}")
                print("="*70)

                response = bot.ask_question(user_question)

                print(f"\n📥 CHATGPT RESPONSE:")
                print("─" * 70)
                print(response)
                print("="*70)

                print(f"\n✅ Question #{question_count} completed!")
                print("💡 Ask another question or type 'quit' to exit")
            else:
                print("⚠️  Please enter a valid question.")
                question_count -= 1  # Don't count empty questions
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Script interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if bot:
            bot.close()
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()

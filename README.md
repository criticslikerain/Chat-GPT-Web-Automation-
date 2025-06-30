# ChatGPT Bot Automation Thing

So basically I was bored one weekend and decided to mess around with making a bot that talks to ChatGPT automatically. Took me like 3 days to figure out all the weird Cloudflare stuff but whatever, it works now.



<div align="center">
  <img src="[https://github.com/user-attachments/assets/c72e6088-6263-42b5-be9d-4f100b1094db](https://github.com/criticslikerain/Chat-GPT-Web-Automation-/issues/1#issue-3187734469)" alt="zerotwo" width="350" >
</div>



## What this does

- Opens Chrome and goes to ChatGPT
- You can either use the terminal OR a fancy web interface (I got carried away and made a whole website)
- It types your questions into ChatGPT automatically
- Copies the response back to you
- Repeat until you get bored
- Has some tricks to avoid getting blocked by Cloudflare (took forever to figure out)
- Now has a beautiful web UI with animations because why not

## Stuff you need first

You need Python installed obviously. And Chrome browser. That's pretty much it. Oh and internet connection but if you're reading this you probably have that already.

## How to actually run this mess

Ok so there's like 4 different ways to do this because I kept adding stuff:

### The new fancy web interface way (RECOMMENDED)
This opens a beautiful website on port 3700:
```bash
python start_web_server.py
```
Or just double-click `start_server.bat` if you're on Windows

Then open your browser and go to: http://localhost:3700

### The old terminal way
Just run this and it should work:
```bash
python run_chatgpt.py
```

### If that doesn't work
Try the fancy version with more bypass stuff:
```bash
python chatgpt_cloudflare_bypass.py
```

### If you want to install stuff manually
```bash
pip install -r requirements.txt
python chatgpt_automation_simple.py
```

## What happens when you run it

### Web Interface Mode (the cool new way):
1. Run the web server script
2. Open your browser to http://localhost:3700
3. Click "Start Automation" button
4. Chrome opens in the background and goes to ChatGPT
5. You login manually (still not storing passwords, that's sketchy)
6. Come back to the web interface and start typing
7. Watch it type your questions automatically in real-time
8. Responses show up in the chat interface with fancy animations

### Terminal Mode (the old way):
1. Chrome opens up and goes to ChatGPT
2. You have to login yourself
3. Come back to the terminal and press Enter
4. Type whatever you want to ask ChatGPT
5. Watch it type your question automatically
6. Response shows up in your terminal
7. Ask more stuff or type 'quit' to stop

## Example of what it looks like

```
Your question: what's 2+2

CHATGPT RESPONSE:
2 + 2 equals 4.

Your question: tell me a dad joke

CHATGPT RESPONSE:
Why don't scientists trust atoms? Because they make up everything!

Your question: quit
```

## Files and what they do

- `web_server.py` - The new web server that runs the fancy interface
- `start_web_server.py` - Easy startup script for the web interface
- `start_server.bat` - Windows batch file to start everything
- `templates/index.html` - The beautiful web interface (spent way too much time on this)
- `static/app.js` - JavaScript that makes the web interface work
- `chatgpt_automation_simple.py` - Main automation script with Cloudflare bypass
- `chatgpt_cloudflare_bypass.py` - Advanced version with more stealth features
- `run_chatgpt.py` - The old terminal interface wrapper
- `requirements.txt` - All the Python packages you need
- `README.md` - This file you're reading right now

## Configuration Options

### Headless Mode
To run without opening a visible browser window:
```python
bot = ChatGPTAutomation(headless=True)
```

### Timeout Settings
Adjust response timeout (default 60 seconds):
```python
response = bot.wait_for_response(timeout=120)  # 2 minutes
```

## Troubleshooting

### Common Issues

1. **"Could not find input field"**
   - Make sure you're logged into ChatGPT
   - Ensure you're on the main chat page
   - Try refreshing the page

2. **"No response received"**
   - Check your internet connection
   - Increase the timeout value
   - Verify ChatGPT is responding normally

3. **ChromeDriver issues**
   - The script automatically downloads ChromeDriver
   - Make sure Chrome browser is installed
   - Check that Chrome is up to date

4. **Web interface won't load**
   - Make sure you're going to http://localhost:3700
   - Check if port 3700 is already in use
   - Try restarting the web server
   - Make sure all dependencies are installed with `pip install -r requirements.txt`

5. **Cloudflare blocks you**
   - Try the `chatgpt_cloudflare_bypass.py` version
   - Wait a bit and try again
   - Clear your browser cache maybe?

### Manual Login Required

The script will pause to allow you to:
- Log into your ChatGPT account
- Complete any CAPTCHA if required
- Navigate to the main chat interface

## Web Interface Features

The new web interface is pretty cool (if I do say so myself):

- **Beautiful animated UI** with particles floating around
- **Real-time chat interface** that looks like a proper messaging app
- **Status monitoring** with colored indicators so you know what's happening
- **Responsive design** that works on mobile too
- **Glass morphism effects** because it looks fancy
- **Smooth animations** for everything
- **Real-time updates** using WebSockets

Just open http://localhost:3700 in your browser and you'll see what I mean.

## Important Notes

- ⚠️ **Rate Limits**: Be mindful of ChatGPT's usage limits
- 🔐 **Login**: You need a valid ChatGPT account
- 🌐 **Internet**: Requires stable internet connection
- 🤖 **Automation Detection**: Some sites may detect automation
- 🌐 **Port 3700**: Make sure this port isn't being used by something else

## Legal and Ethical Considerations

- Use responsibly and in accordance with OpenAI's terms of service
- Don't use for spam or malicious purposes
- Respect rate limits and usage policies
- This is for educational and personal use

## Contributing

Feel free to improve this automation script by:
- Adding error handling
- Improving element detection
- Adding more features
- Optimizing performance

## License

This project is for educational purposes. Please respect OpenAI's terms of service when using this automation.

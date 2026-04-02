<img src="logo.jpeg" class="logo" width="120"/>
<img src="https://img.shields.io/github/downloads/C0m3b4ck/Vulntest-AI-Agent/total">
<br><b>🇪🇺🇪🇺🇪🇺Made in Europe🇪🇺🇪🇺🇪🇺

# Vulntest AI Agent

An open-source, prompt-driven AI agent for automated vulnerability command execution using configurable keyword-command mappings. Works offline, but has online functionality. Simple and easy to build on and customize for your own needs!

## Contributors  
Started on August 4th, 2025 by C0m3b4ck.

# Why I made this
I was watching some YouTube but then got annoyed at the constant cheesy AI ads telling that prompt engineering is the past and agents are the future. They also said how if I don't sign up for their webinar I will suffer. In order to prove them wrong, I made this and I quite like it! I though about such an "agent" earlier but never had the motivation.

## Requirements  
- Python 3.x (tested on Python 3.13)  
- Runs on Linux (tested on Ubuntu Linux), Windows might need modified file handling and model download
- Uses standard Python libraries: `os`, `re`, `subprocess`, `socket`  

## Installation  
Simply clone or download the script and create a `configs` folder alongside it.  

Add `.conf` files in `configs` describing keywords and commands (see Features).  

Run with:  
```

python3 agent_verX.py

```

## How it Works 
- **User Prompt:** You input a natural language prompt requesting vulnerability testing or network commands.  
- **Configuration Matching:** The agent reads your prompt, then looks for words from the keyword that are found both in the agent's function list using Ollama MCP functions.

- **Target Extraction:**  
The agent picks the correct tool based on your prompt.

- **Command Execution:** The correct function(s) are then executed.
- **User Confirmation:** Only executes on explicit user approval (if user inputs "yes"). 
- **Redirects:** If the prompt was previously incorrectly matched, a `redirects.conf` file can override the conf selection. That allows for correcting the model's tool choices.
  
## Features  
- **Prompt-based AI Agent:** Works with natural language inputs including domains, IPs and files.    
- **Dangerous Prompt Detection:** Checks for words written in safety.conf in prompt (for example "ddos"), then warns user about potential consequences

## Folder Structure  
```

agent_verX.py              \# Main AI agent script
configs/                   \# Folder containing keyword-command .conf files
configs/redirects.conf     \# Saves user redirects (created automatically)

```

## Roadmap / Future Enhancements  
- Add more functions to be extracted from keywords - if you need a specific one, just ask! 
- Support multiple target extraction per prompt
- More training on credited and openly available security data.
- Add logging and analytics of executed commands (and debugger mode)
- 
## Disclaimer  
Use responsibly. This tool is intended for authorized penetration testing and network diagnostics only. Using the tool to attack without consent is illegal.

---

If you have questions, feature requests or want to contribute, reach out to **C0m3b4ck.**


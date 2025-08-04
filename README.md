<img src="logo.jpeg" class="logo" width="120"/>
# Vulntest AI Agent  
<img src="https://img.shields.io/github/downloads/C0m3b4ck/Vulntest-AI-Agent/total">

An open-source, prompt-driven AI agent for automated vulnerability command execution using configurable keyword-command mappings. 100% offline. Simple and easy to build on and customize for your own needs!

## Contributors  
Started on August 4th, 2025 by C0m3b4ck.

## Requirements  
- Python 3.x (tested on Python 3.13)  
- Runs on Linux (tested on Ubuntu Linux), Windows might need modified file handling which will soon come :)
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
- **Configuration Matching:** The agent reads your prompt, then looks for words from the keyword that are also found in `.conf` files in the `configs` folder. Each `.conf` file contains:
  - First line: comma-separated keywords (what makes this .conf to be picked)  
  - Second line: the shell command template, with `{target}` parameter for IP/domain replacement  

- **Target Extraction:**  
  - First attempts to extract an IPv4 address from prompt.  
  - If none found, extracts domain names and resolves the first via DNS to an IP address.  

- **Command Execution:** The chosen command from the matched `.conf` file is customized with the extracted target and presented to the user for confirmation.
- **User Confirmation:** Only executes on explicit user approval (if user inputs "yes"). 
- **Redirects:** If the prompt was previously incorrectly matched, a `redirects.conf` file can override the conf selection. That allows for "training" the model or rather manually correcting its mistakes.
  
## Features  
- **Configurable Exploit/Network Commands:** Easily add or modify `.conf` files with keywords and commands to extend functionality without changing code.  
- **Prompt-based AI Agent:** Works with natural language inputs including domains and IPs.  
- **Domain Name Resolution:** Automatically resolves domains found in prompts to IPs for command execution.  
- **User Interaction:** Prompts before command execution and error handling with option to correct config matches.  
- **Redirect Learning:** User can teach the AI better matching via redirect mappings.  
- **Cross-Platform:** Runs on Windows and Linux environments with Python installed.

## Folder Structure  
```

agent_ver1.py              \# Main AI agent script
configs/                   \# Folder containing keyword-command .conf files
configs/redirects.conf     \# Saves user redirects (created automatically)
configs/config_here.conf   \# Any configs you might want to add

```

## Example `.conf` Files  
`ping.conf`  
```

ping,test,icmp
ping -c 4 {target}

```

`ddos.conf`  
```

ddos,stress,website
sudo hping3 --flood -S {target}

```

## Roadmap / Future Enhancements  
- Add more functions to be extracted from keywords
- (maybe) add safety measures for words like "ddos" that will warn the user about potential consequences. These words will be stored in safety.conf
- Support multiple target extraction per prompt  
- Add logging and analytics of executed commands (and debugger mode)
- Support other command substitution tokens besides `{target}`   

## What is up to you
- Adding additional arguments (like "no installation") to .conf files
- Making .conf files, though I will publish some example ones every now and then

## Disclaimer  
Use responsibly. This tool is intended for authorized penetration testing and network diagnostics only. Use to attack without consent is illegal.

---

If you have questions or want to contribute, reach out to C0m3b4ck.
```

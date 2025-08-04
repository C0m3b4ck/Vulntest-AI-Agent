import os
import re
import subprocess
import socket

CONFIG_DIR = './configs'
REDIRECTS_FILE = os.path.join(CONFIG_DIR, 'redirects.conf')
SAFETY_FILE = os.path.join(CONFIG_DIR, 'safety.conf')

def load_conf_files():
    confs = {}
    for filename in os.listdir(CONFIG_DIR):
        if filename.endswith('.conf') and filename != 'redirects.conf' and filename != 'safety.conf':
            path = os.path.join(CONFIG_DIR, filename)
            with open(path, 'r') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                if len(lines) >= 2:
                    keywords_line = lines[0]
                    command_line = lines[1]
                    keywords = [kw.strip().lower() for kw in keywords_line.split(',')]
                    confs[filename] = {'keywords': keywords, 'command': command_line}
    return confs

def load_redirects():
    redirects = {}
    if os.path.exists(REDIRECTS_FILE):
        with open(REDIRECTS_FILE, 'r') as f:
            for line in f:
                clean_line = line.strip()
                if clean_line and not clean_line.startswith('#'):
                    if '->' in clean_line:
                        prompt_text, redirect_file = map(str.strip, clean_line.split('->', 1))
                        redirects[prompt_text.lower()] = redirect_file
    return redirects

def save_redirect(prompt, conf_file):
    with open(REDIRECTS_FILE, 'a') as f:
        f.write(f"{prompt} -> {conf_file}\n")

def extract_domains(text):
    # Basic domain pattern, matches typical domain names (not exhaustive)
    domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
    return re.findall(domain_pattern, text)

def resolve_domain_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def extract_target(text):
    # Try extracting IP addresses first
    ip_pattern = r'(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)'
    ips = re.findall(ip_pattern, text)
    if ips:
        return ips[-1]

    # If no IPs found, try domains and resolve
    domains = extract_domains(text)
    if domains:
        resolved_ip = resolve_domain_to_ip(domains[0])
        if resolved_ip:
            print(f"AI Agent: Resolved domain '{domains[0]}' to IP {resolved_ip}.")
            return resolved_ip

    return None

def find_conf_for_prompt(prompt, confs, redirects):
    prompt_lower = prompt.lower()

    # Check redirects first
    for saved_prompt in redirects:
        if saved_prompt in prompt_lower:
            redirect_conf = redirects[saved_prompt]
            if redirect_conf in confs:
                return redirect_conf, confs[redirect_conf]

    # Otherwise match first conf with keyword in prompt
    for conf_name, conf_data in confs.items():
        for kw in conf_data['keywords']:
            if kw in prompt_lower:
                return conf_name, conf_data
    return None, None

def ask_and_save_redirect(prompt, confs):
    wrong = input("Was this a wrong configuration? Would you like to add a redirect for this prompt? (yes/no): ").strip().lower()
    if wrong == 'yes':
        print("Available configurations:")
        for idx, key in enumerate(confs.keys(), 1):
            print(f"{idx}: {key}")
        choice = input("Enter the number of the correct config to redirect this prompt to: ").strip()
        try:
            choice_idx = int(choice) - 1
            conf_keys = list(confs.keys())
            if 0 <= choice_idx < len(conf_keys):
                correct_conf = conf_keys[choice_idx]
                save_redirect(prompt.lower(), correct_conf)
                print(f"AI Agent: Redirect saved: '{prompt}' -> '{correct_conf}'")
            else:
                print("AI Agent: Invalid choice, nothing saved.")
        except ValueError:
            print("AI Agent: Invalid input, nothing saved.")

def load_safety_keywords():
    keywords = set()
    if os.path.exists(SAFETY_FILE):
        with open(SAFETY_FILE, 'r') as f:
            for line in f:
                kw = line.strip().lower()
                if kw and not kw.startswith('#'):
                    keywords.add(kw)
    return keywords

def check_safety(prompt, safety_keywords):
    prompt_lower = prompt.lower()
    for kw in safety_keywords:
        if kw in prompt_lower:
            return kw
    return None

def main():
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    confs = load_conf_files()
    redirects = load_redirects()
    safety_keywords = load_safety_keywords()

    prompt = input("Enter your prompt: ").strip()

    # SAFETY CHECK IMMEDIATELY AFTER PROMPT INPUT
    unsafe_kw = check_safety(prompt, safety_keywords)
    if unsafe_kw:
        print(f"AI Agent: WARNING - Your prompt contains a potentially dangerous keyword '{unsafe_kw}'.")
        print("Executing this command may have serious consequences (e.g., cause service disruption or be illegal).")
        confirm_warning = input("Are you absolutely sure you want to proceed? (yes/no): ").strip().lower()
        if confirm_warning != 'yes':
            print("AI Agent: Command aborted by user due to safety concerns.")
            ask_and_save_redirect(prompt, confs)
            return

    conf_name, conf_data = find_conf_for_prompt(prompt, confs, redirects)

    if not conf_data:
        print("AI Agent: Sorry, no matching configuration found for your prompt.")
        return

    print(f"AI Agent: Matched config '{conf_name}' with keywords {conf_data['keywords']}")
    target = extract_target(prompt)
    if not target:
        print("AI Agent: Could not find a valid IP target in the prompt.")
        return

    command_to_run = conf_data['command'].replace('{target}', target)
    print(f"AI Agent: Planned Command: {command_to_run}")

    confirm = input("Proceed with command? (yes/no): ").strip().lower()
    if confirm == 'yes':
        print("AI Agent: Executing command...")
        try:
            subprocess.run(command_to_run, shell=True)
        except Exception as e:
            print(f"AI Agent: Failed to execute command: {e}")
    else:
        print("AI Agent: Command aborted by user.")
        ask_and_save_redirect(prompt, confs)

if __name__ == "__main__":
    main()

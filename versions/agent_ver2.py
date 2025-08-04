import os
import re
import subprocess
import socket

CONFIG_DIR = './configs'
REDIRECTS_FILE = os.path.join(CONFIG_DIR, 'redirects.conf')

def load_conf_files():
    confs = {}
    for filename in os.listdir(CONFIG_DIR):
        if filename.endswith('.conf') and filename != 'redirects.conf':
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
    # Basic domain pattern, this matches typical domain names (not exhaustive)
    domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
    domains = re.findall(domain_pattern, text)
    return domains

def resolve_domain_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def extract_target(text):
    # First try to extract IPv4 addresses
    ip_pattern = r'(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)'
    ips = re.findall(ip_pattern, text)
    if ips:
        return ips[-1]

    # If no IPs, try domains
    domains = extract_domains(text)
    if domains:
        resolved_ip = resolve_domain_to_ip(domains[0])
        if resolved_ip:
            print(f"AI Agent: Resolved domain '{domains[0]}' to IP {resolved_ip}.")
            return resolved_ip

    return None

def find_conf_for_prompt(prompt, confs, redirects):
    prompt_lower = prompt.lower()

    # Check redirect overrides first
    for saved_prompt in redirects:
        if saved_prompt in prompt_lower:
            redirect_conf = redirects[saved_prompt]
            if redirect_conf in confs:
                return redirect_conf, confs[redirect_conf]

    # Otherwise find first conf matching any keyword
    for conf_name, conf_data in confs.items():
        for kw in conf_data['keywords']:
            if kw in prompt_lower:
                return conf_name, conf_data
    return None, None

def main():
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    confs = load_conf_files()
    redirects = load_redirects()

    prompt = input("Enter your prompt: ").strip()
    conf_name, conf_data = find_conf_for_prompt(prompt, confs, redirects)

    if not conf_data:
        print("AI Agent: Sorry, no matching configuration found for your prompt.")
        return

    print(f"AI Agent: Matched config '{conf_name}' with keywords {conf_data['keywords']}")
    target = extract_target(prompt)
    if not target:
        print("AI Agent: Could not find a valid IP target in the prompt.")
        return

    # Replace placeholder in command with actual target
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
        wrong = input("Was this a wrong configuration? Save a redirect? (yes/no): ").strip().lower()
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

if __name__ == "__main__":
    main()

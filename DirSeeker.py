

import urllib.error
import urllib.request
import threading
import queue
import sys
import urllib.parse


def show_banner():
    banner = r"""
    ____  _      ____            _             
    |  _ \(_)_ __/ ___|  ___  ___| | _____ _ __ 
    | | | | | '__\___ \ / _ \/ _ \ |/ / _ \ '__|
    | |_| | | |   ___) |  __/  __/   <  __/ |   
    |____/|_|_|  |____/ \___|\___|_|\_\___|_|   
                                         
                                                                        
    ════════════════════════════════════════════════════════════════════
    [*] WEB Directory & File Brute Forcer
    [*] Author: Aliakbar Babayev
    [*] Version: 1.0
    [*] Multi-threaded: 50 threads
    ════════════════════════════════════════════════════════════════════
    """
    print(banner)

def build_wordlist(wordlist_file):
    try:
        with open(wordlist_file, "rb") as f:
            raw_words = f.readlines()
    except FileNotFoundError:
        print(f"Error: Wordlist file '{wordlist_file}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading wordlist file: {e}")
        sys.exit(1)
    
    words = queue.Queue()

    for word in raw_words:
        word = word.rstrip().decode('utf-8')
        words.put(word)

    return words

def dir_bruter(target_url, word_queue, extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []

        if "." not in attempt:
            attempt_list.append(f"/{attempt}/")
        else:
            attempt_list.append(f"/{attempt}")
        
        if extensions:
            for extension in extensions:
                attempt_list.append(f"/{attempt}{extension}")
        
        for brute in attempt_list:
            url = f"{target_url}{urllib.parse.quote(brute)}"

            try:
                r = urllib.request.Request(url)
                response = urllib.request.urlopen(r)

                if len(response.read()):
                    print(f"[{response.code}] => {url}")
            
            except urllib.error.URLError as e:
                if hasattr(e, 'code') and e.code != 404:
                    print(f"!!! {e.code} => {url}")
            except Exception as e:
                # Handle other exceptions quietly
                pass

def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        show_banner()
        print("\nUsage: python dirseeker.py <url> <wordlist>")
        print("Example: python dirseeker.py http://example.com /path/to/wordlist.txt")
        sys.exit(1)
    
    # Show banner
    show_banner()
    
    # Get arguments from command line
    target_url = sys.argv[1]
    wordlist_file = sys.argv[2]
    
    # Set number of threads
    threads = 50
    extensions = [".php", ".bak", ".orig", ".inc", ".html", ".txt", ".js", ".css"]
    
    # Build wordlist
    word_queue = build_wordlist(wordlist_file)
    
    print(f"[*] Target URL: {target_url}")
    print(f"[*] Wordlist: {wordlist_file}")
    print(f"[*] Threads: {threads}")
    print(f"[*] Extensions: {', '.join(extensions)}")
    print("[*] Starting scan...")
    print("═" * 60)
    
    # Start threads
    for i in range(threads):
        t = threading.Thread(target=dir_bruter, args=(target_url, word_queue, extensions))
        t.start()

if __name__ == "__main__":
    main()
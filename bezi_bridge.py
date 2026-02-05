import time
import os
from pywinauto import Application
import argparse
import sys
import json

#print(f"DEBUG: Received {len(sys.argv)} arguments.")
#print(f"DEBUG: sys.argv[1] is: {sys.argv[1] if len(sys.argv) > 1 else 'MISSING'}")

##############################################################################
class BeziBridge:
    def __init__(self):
        self.config_file = "bezi_bridge.json"
        self.prompt_timeout_length = 60 * 30        # 30 minutes. 
        self.bezi_initialized = False
        self.bezi_prompt = ""
        self.bezi_path = ""
        self.response_prefix = "SOM "
        self.response_suffix = "EOM "
        self.sync_value = 0
        self.config = None
        self.args = None
        self.bezi_window = None
        self.bezi_prompt_window = None
        self.bezi_new_thread_button = None

    ##########################################################################
    def find_windows(self):
        # 1. Find or Launch bezi_window
        try:
            app = Application(backend="uia")
            if app == None:
                print("Can't connect to Bezi.", file=sys.stderr)
                exit(1)
            app.connect(title="Bezi", class_name="Tauri Window")
            time.sleep(5)
            
            self.bezi_window = app.window(title="Bezi", class_name="Tauri Window")
            if self.bezi_window == None:
                print("Can't find Bezi window.", file=sys.stderr)
                exit(1)
        except:
            if not os.path.exists(self.bezi_path):
                print(f"Error: Executable not found at {self.bezi_path}", file=sys.stderr)
                exit(1)
                
            app = Application(backend="uia").start(self.bezi_path)
            if app == None:
                print("Can't start Bezi.", file=sys.stderr)
                exit(1)

            self.bezi_window = app.window(title="Bezi", class_name="Tauri Window")
            if self.bezi_window == None:
                print("Can't find created Bezi window.", file=sys.stderr)
                exit(1)

            self.bezi_window.wait("visible", timeout=60)

        # 2. Find ALL Edit windows and pick the last one
        # Note: Tauri apps often put the active chat input as the last edit control in the tree.
        all_edits = self.bezi_window.descendants(control_type="Edit")
        
        if not all_edits:
            print(f"bezi_prompt_window not found", file=sys.stderr)
            return (None, None)
        
        # Select the last item in the list
        self.bezi_prompt_window = all_edits[-1]
        
        # Find the New Thread button
        # TODO: localize issue
        btn = self.find_button("New Thread (Ctrl + T)")
        if btn == None:
            print("Unable to find New Thread button.", file=sys.stderr)
            exit(1)
        self.bezi_new_thread_button = btn
        
    ##########################################################################
    def find_button(self, name):
        all_buttons = self.bezi_window.descendants(control_type="Button")
        if all_buttons:
            for btn in all_buttons:
                # pywinauto elements use .texts() for labels and .class_name() for types
                try:
                    if name == btn.element_info.name:
                        return btn
                except Exception:
                    print(" - [Could not parse element details]", file=sys.stderr)
        else:
            print("[WARNING] No buttons found. Check if the application is in focus.", file=sys.stderr)
            exit(1)
            
        return None
    
    ##########################################################################
    # Extract variables from self.config and arguments
    def validate_arguments(self):
        # Handle Initialization Flag
        if self.args.init:
            self.config["initialized"] = True
            self.bezi_initialized = True
            default_path = r"C:\Program Files\Bezi\Bezi.exe"
            self.config["bezi_path"] = self.args.bezi_path if self.args.bezi_path else default_path
            self.sync_value = 0
            self.config["sync_value"] = 0
            self.save_config(self.config)
            print("Bezi Bridge initialized.", file=sys.stderr)
            self.bezi_path = self.config["bezi_path"]
            return True 

        if not self.config.get("initialized", False):
            print("Error: Run with -i first.", file=sys.stderr)
            return False

        self.bezi_path = self.args.bezi_path or self.config.get("bezi_path")

        if self.args.prompt and os.path.exists(self.args.prompt):
            print("Reading from file", file=sys.stderr);
            with open(self.args.prompt, 'r', encoding='utf-8') as f:
                self.bezi_prompt = f.read()
        else:
            print("Assigning from args", file=sys.stderr);
            self.bezi_prompt = self.args.prompt
        
        return True

    ##########################################################################
    # Parse arguments
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Bezi Bridge")
        parser.add_argument("prompt", nargs='?', help="The prompt sent to Bezi")
        parser.add_argument("-b", "--bezi_path", help="Full path to Bezi.exe")
        parser.add_argument("-i", "--init", action="store_true", help="Initialize Bezi session. Must be performed first.")
        parser.add_argument("-t", "--thread_name", help="Name of new thread to create")
        self.args = parser.parse_args()
    
        if self.args.thread_name == None and self.args.init == False:
            print("No thread name provided.", file=sys.stderr)
            exit(1)
            
        return self.args
        
    ##########################################################################
    # Helper to load self.config
    def load_config(self):
        if os.path.exists(self.config_file) and os.path.getsize(self.config_file) > 0:
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: config file corrupted. Resetting defaults.", file=sys.stderr)
        
        return {"initialized": False, "bezi_path": None, "sync_value": 0}
        
    ##########################################################################
    # Helper to save self.config
    def save_config(self, config):
        with open(self.config_file, "w") as f:
            json.dump(config, f)

    ##########################################################################
    def setup_context(self):
        # TODO: localize
        self.click_button("New Thread (Ctrl + T)")

        setup_msg = (
            f'Begin all of your responses with SOM. End all of them with EOM. Keep track of how many prompts I have issued and put it after SOM / EOM, but lets start counting at 0.'
        )

        # Reset sync value for fresh init
        self.sync_value = 0

        result = self.send_prompt(setup_msg, is_init=True)
        return result
        
    ##########################################################################
    def send_prompt(self, message, is_init=False):        
        if message == None or message == "":
            print("Empty message attempt.", file=sys.stderr)
            raise ValueError("Empty prompt")
            return
        
        # --- Send Loop ---
        while True:
            self.find_windows()
            self.bezi_window.set_focus()
            
            pending_prompt = message
            
            key_retries_max = 3
            key_retry = 0
            keys_sent = False
            while keys_sent == False and key_retry < key_retries_max:
                key_retry += 1
                
                # Send the prompt
                try:
                    print(f"Sending prompt: {pending_prompt}")
                    self.bezi_prompt_window.set_text(pending_prompt)
                    time.sleep(1)
                    self.bezi_prompt_window.type_keys("{ENTER}")
                    time.sleep(1)
                except Exception as e:
                    print(f"\nError sending keys, RETRYING ({key_retry} of {key_retries_max}). Exception: \"{e}\"", file=sys.stderr)
                else:
                    keys_sent = True
                    
            print(f"\nWaiting for response (Expected EOM sync value: {self.sync_value})...", end="", flush=True, file=sys.stderr)
            
            start_time = time.time()
            found_data = None

            # "20 tool call limit"
            # TODO: localize
            self.close_dialog("Continue")
            
            # Polling Loop
            while (time.time() - start_time) < self.prompt_timeout_length:
                time.sleep(1)
                print(".", end="", flush=True, file=sys.stderr)
                
                # Capture all text fields
                elements = self.bezi_window.descendants(control_type="Text")
                full_text = [e.window_text().strip() for e in elements]

                # Search for the Specific SOM we are expecting
                for i, line in enumerate(full_text):
                    if self.response_prefix in line:
                        try:
                            # Parse the ID
                            received_counter = int(line.replace(self.response_prefix, "").strip())
                            
                            # If we see the expected counter
                            if received_counter == self.sync_value:
                                # Look for the matching EOM suffix
                                suffix_needed = f"{self.response_suffix}{self.sync_value}"
                                
                                # Search forward from the SOM line to find EOM
                                if suffix_needed in full_text[i:]:
                                    end_idx = full_text.index(suffix_needed, i)
                                    found_data = full_text[i + 1 : end_idx]
                                    break
                        except ValueError:
                            continue
                
                # "20 tool call limit"
                # TODO: localize
                self.close_dialog("Continue")

                if found_data:
                    break

            # Post-Process Polling Result
            if found_data:
                print("\n", file=sys.stderr)
                final_response = "\n".join(found_data)
                
                # Update Sync Value for next time
                self.sync_value += 1
                self.config["sync_value"] = self.sync_value
                self.save_config(self.config)
                
                return final_response
            else:
                print("\n[Error] Bezi AI timed out.", file=sys.stderr)
                return ""
    
    ##########################################################################
    def close_dialog(self, button_name):
        return self.click_button(button_name)
        
    ##########################################################################
    def click_button(self, button_name):
        btn = self.find_button(button_name)
        if btn != None:
            btn.set_focus()
            btn.click()
            return True
        return False
        
    ##########################################################################
    def new_thread(self):
        #self.bezi_new_thread_button.set_focus()
        #self.bezi_new_thread_button.click()

        self.bezi_window.draw_outline()
        self.bezi_window.type_keys("^T", set_foreground=False)

        # Confirmation dialog.
        self.close_dialog("Keep all changes")

        # Setup the thread for use.
        self.setup_context()
        
    ##########################################################################
    def run(self):
        self.config = self.load_config()
        self.args = self.parse_arguments()
        self.sync_value = self.config.get("sync_value", 0)

        # Validate
        if not self.validate_arguments():
            return (False, "Invalid Arguments or State")
        
        # Find Window
        self.find_windows()
        if not self.bezi_window or not self.bezi_prompt_window or not self.bezi_new_thread_button:
            return (False, "Could not find Bezi Window components")

        # Sync with existing chat history
        print("\nSyncing with Bezi history...", end="", flush=True, file=sys.stderr)
        elements = self.bezi_window.descendants(control_type="Text")
        full_text = [e.window_text().strip() for e in elements]
        
        # Find all lines containing SOM
        som_lines = [line for line in full_text if self.response_prefix in line]
        
        if som_lines:
            # Get the LAST SOM found in the UI tree (most recent)
            last_som = som_lines[-1]
            try:
                last_id = int(last_som.replace(self.response_prefix, "").strip())
                self.sync_value = last_id + 1
            except ValueError:
                print(" Could not parse last SOM. Using default sync.", file=sys.stderr)
        else:
            print(" No history found. Using current sync value.", file=sys.stderr)

        # Setup context upon first init.
        if self.args.init and self.sync_value == 0:
            self.setup_context()
            return (True, "Initialization Complete")

        # Create a new thread.
        self.new_thread()
        
        # Send the prompt.
        if self.args.init == False:
            result = self.send_prompt(self.bezi_prompt)
            if result:
                # "20 tool call limit"
                # TODO: localize
                self.close_dialog("Continue")
                    
                return (True, result)
            else:
                return (False, "Timeout or empty Response sending prompt to Bezi.")
        else:
            return (True, "No Error.")

##############################################################################
if __name__ == "__main__":
    bridge = BeziBridge()
    success, result = bridge.run()
    
    if success:
        # Print ONLY the result to stdout for the caller to capture
        if result != "Initialization Complete":
            print(result, file=sys.stderr)
        else:
            # If initializing, we can print a confirmation to stderr
            print("Bezi Bridge Initialized Successfully.", file=sys.stderr)
        
        sys.exit(0)
    else:
        # Print error to stderr so it's not mistaken for a prompt result
        print(f"Error: {result}", file=sys.stderr)
        sys.exit(1)

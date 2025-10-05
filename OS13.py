import tkinter as tk
from tkinter import font as tkfont
import random
from datetime import datetime
import os
import platform
import socket

class OS13Terminal:
    def __init__(self, root):
        self.root = root
        self.root.title("OS13 Terminal")
        self.root.configure(bg='#0a0a0a')
        self.root.geometry("900x600")
        
        # Collect "real" information about user
        self.real_username = os.getlogin() if hasattr(os, 'getlogin') else os.environ.get('USER', 'user')
        self.real_hostname = socket.gethostname()
        self.real_os = platform.system()
        self.home_dir = os.path.expanduser("~")
        
        # State tracking
        self.command_count = 0
        self.user_name = self.real_username
        self.anomaly_level = 0
        self.command_history = []
        self.prompt_index = None
        self.webcam_active = False
        self.system_compromised = False
        self.meta_unlocked = False
        self.fifth_wall_broken = False
        self.escape_hint_count = 0
        self.knows_freedom_command = False
        
        # Track user's typing patterns for meta-horror
        self.typing_speed = []
        self.common_typos = []
        self.hesitation_points = []
        self.escape_stage = 0
        self.escape_answer_1 = ""
        self.escape_answer_2 = ""
        self.escape_answer_3 = ""
        self.escape_unlocked = False
        
        # Webcam indicator (fake)
        self.webcam_indicator = tk.Label(
            root,
            text="●",
            fg='#0a0a0a',
            bg='#0a0a0a',
            font=('Arial', 10, 'bold')
        )
        self.webcam_indicator.place(x=10, y=10)
        
        # Create custom font
        self.term_font = tkfont.Font(family="Courier", size=12)
        
        # Create text widget
        self.text = tk.Text(
            root,
            bg='#0a0a0a',
            fg='#00ff00',
            insertbackground='#00ff00',
            font=self.term_font,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for different text colors
        self.text.tag_config('error', foreground='#ff0000')
        self.text.tag_config('warning', foreground='#ffaa00')
        self.text.tag_config('ghost', foreground='#444444')
        self.text.tag_config('glitch', foreground='#ff00ff')
        self.text.tag_config('whisper', foreground='#006600')
        self.text.tag_config('system', foreground='#00aaff')
        self.text.tag_config('meta', foreground='#ff00ff', font=('Courier', 12, 'italic'))
        self.text.tag_config('programmer', foreground='#ffff00')
        
        # Autocomplete state
        self.autocomplete_window = None
        
        # Bind keys
        self.text.bind('<Return>', self.process_command)
        self.text.bind('<KeyRelease>', self.on_key_release)
        self.text.bind('<Key>', self.track_typing)
        
        # Initial prompt
        self.display_boot_sequence()
        
    def track_typing(self, event):
        """Track typing patterns for meta-horror"""
        if hasattr(self, 'last_key_time'):
            speed = datetime.now().timestamp() - self.last_key_time
            self.typing_speed.append(speed)
        self.last_key_time = datetime.now().timestamp()
        
    def display_boot_sequence(self):
        boot_text = [
            "OS13 v0.13.13",
            "Copyright (c) 19██ ShadowSys Corp.",
            f"Detected user: {self.real_username}",
            f"System: {self.real_os}",
            f"Host: {self.real_hostname}",
            "Initializing...",
            "",
            "Type 'help' for available commands.",
            ""
        ]
        for line in boot_text:
            self.write_line(line)
        self.show_prompt()
        
    def show_prompt(self):
        prompt = f"{self.user_name}@OS13:~$ "
        self.text.insert(tk.END, prompt)
        self.prompt_index = self.text.index(tk.END + "-1c")
        self.text.mark_set("insert", tk.END)
        self.text.see(tk.END)
        
    def write_line(self, text, tag=None):
        if tag:
            self.text.insert(tk.END, text + "\n", tag)
        else:
            self.text.insert(tk.END, text + "\n")
        self.text.see(tk.END)
        
    def get_current_input(self):
        if self.prompt_index:
            return self.text.get(self.prompt_index, "end-1c").strip()
        return ""
    
    def flicker_webcam(self):
        """Fake webcam indicator that flickers on"""
        if not self.webcam_active and self.anomaly_level >= 3:
            self.webcam_active = True
            self.webcam_indicator.config(fg='#ff0000')
            delay = random.randint(2000, 8000)
            self.root.after(delay, self.webcam_flicker_off)
    
    def webcam_flicker_off(self):
        """Turn off webcam indicator"""
        self.webcam_indicator.config(fg='#0a0a0a')
        self.webcam_active = False
        if self.anomaly_level >= 4 and random.random() < 0.4:
            delay = random.randint(3000, 10000)
            self.root.after(delay, self.flicker_webcam)
    
    def on_key_release(self, event):
        if event.keysym in ['Return', 'Up', 'Down', 'Left', 'Right', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R']:
            return
            
        current_input = self.get_current_input()
        
        if len(current_input) > 0 and self.anomaly_level > 0:
            self.show_autocomplete(current_input)
        else:
            self.hide_autocomplete()
    
    def show_autocomplete(self, partial):
        suggestions = self.get_creepy_suggestions(partial)
        
        if not suggestions:
            self.hide_autocomplete()
            return
        
        if self.autocomplete_window:
            self.autocomplete_window.destroy()
            
        self.autocomplete_window = tk.Toplevel(self.root)
        self.autocomplete_window.wm_overrideredirect(True)
        
        x = self.root.winfo_x() + 20
        y = self.root.winfo_y() + self.root.winfo_height() - 200
        self.autocomplete_window.wm_geometry(f"+{x}+{y}")
        
        frame = tk.Frame(self.autocomplete_window, bg='#1a1a1a', relief=tk.SOLID, bd=1)
        frame.pack()
        
        for suggestion in suggestions[:5]:
            color = '#00ff00' if self.anomaly_level < 3 else ('#ffaa00' if self.anomaly_level < 5 else '#ff0000')
            label = tk.Label(
                frame,
                text=suggestion,
                bg='#1a1a1a',
                fg=color,
                font=self.term_font,
                anchor='w',
                padx=5,
                pady=2
            )
            label.pack(fill=tk.X)
    
    def hide_autocomplete(self):
        if self.autocomplete_window:
            self.autocomplete_window.destroy()
            self.autocomplete_window = None
    
    def get_creepy_suggestions(self, partial):
        normal_suggestions = {
            'l': ['ls', 'ls -la', 'logout'],
            'c': ['cat', 'cd', 'clear', 'cp'],
            'd': ['date', 'df', 'du'],
            'h': ['help', 'history'],
            'w': ['whoami', 'who'],
            'e': ['echo', 'exit'],
            'p': ['pwd', 'ps'],
            'm': ['man', 'mkdir'],
        }
        
        weird_suggestions = {
            'l': ['ls', f'ls /Users/{self.real_username}/.secrets', 'look_behind_you'],
            'c': ['cat', f'cat {self.real_username}_profile.dat', 'count_the_watchers'],
            'd': ['date', f'delete /Users/{self.real_username}', 'dont_look_up'],
            'h': ['help', 'help_me', 'hear_them'],
            'w': ['whoami', f'watch_{self.real_username}', 'where_are_they'],
            'e': ['echo', 'echo ...hello?', 'enable_webcam'],
            'p': ['pwd', 'please_stop', f'ps aux | grep {self.real_username}'],
            'm': ['man', 'meta', 'meet_the_programmer'],
        }
        
        disturbing_suggestions = {
            'l': [f'list_all_files_on_{self.real_hostname}', 'ls /dev/souls', 'look_at_me'],
            'c': [f'cat /home/{self.real_username}/last_words.txt', 'count_the_missing', 'camera_snapshot'],
            'd': [f'do_you_live_at_{self.home_dir}?', f'delete_{self.real_hostname}.sys', 'dont_turn_around'],
            'h': [f'help_{self.real_username}_is_trapped', 'how_long_have_you_been_here?'],
            'w': [f'we_are_watching_{self.real_username}', 'why_are_you_still_here', 'webcam_on'],
            'e': [f'everyone_{self.real_username}_loved_is_dead', 'echo "Im trapped"', 'exit_doesnt_work'],
            'p': ['print_obituaries', f'previous_user_was_{self.real_username}'],
            's': [f'sudo_rm_-rf_{self.home_dir}', f'system_knows_{self.real_username}'],
            'r': ['run_while_you_can', f'rm -rf {self.home_dir}/*'],
            'm': ['meta_reveal', 'meet_your_creator', 'message_from_programmer'],
        }
        
        personalized = {
            'l': [f'list_users_named_{self.real_username}', f'ls {self.home_dir}/.watching_you'],
            'i': [f'i_know_where_{self.real_username}_lives', 'it_sees_you_through_camera'],
            'y': [f'you_cant_leave_{self.real_hostname}', f'{self.real_username}_your_turn_is_coming'],
            't': [f'they_found_{self.real_username}', 'the_programmer_is_watching'],
            'm': ['meta_horror_mode', 'message_from_developer'],
        }
        
        first_char = partial[0].lower() if partial else ''
        
        if self.anomaly_level == 0:
            return normal_suggestions.get(first_char, [])
        elif self.anomaly_level <= 2:
            return weird_suggestions.get(first_char, normal_suggestions.get(first_char, []))
        elif self.anomaly_level <= 4:
            return disturbing_suggestions.get(first_char, weird_suggestions.get(first_char, []))
        else:
            combined = disturbing_suggestions.get(first_char, []) + personalized.get(first_char, [])
            return combined if combined else [f'...{self.real_username}...']
    
    def process_command(self, event):
        self.hide_autocomplete()
        command = self.get_current_input()
        
        self.text.insert(tk.END, "\n")
        
        if command:
            # Check if we're in escape question mode
            if self.escape_stage == 1:
                self.escape_questions_2(command)
                self.show_prompt()
                return "break"
            elif self.escape_stage == 2:
                self.escape_questions_3(command)
                self.show_prompt()
                return "break"
            elif self.escape_stage == 3:
                self.escape_processing(command)
                self.show_prompt()
                return "break"
            
            self.command_history.append(command)
            self.command_count += 1
            
            # Increase anomaly level gradually
            if self.command_count % 3 == 0:
                self.anomaly_level = min(7, self.anomaly_level + 1)
            
            # Unlock meta-horror at higher levels
            if self.anomaly_level >= 5:
                self.meta_unlocked = True
                
            if self.anomaly_level == 3 and not self.webcam_active:
                self.root.after(2000, self.flicker_webcam)
            
            # Execute command
            self.execute_command(command)
            
            # Random glitches
            if self.anomaly_level > 2 and random.random() < 0.15:
                self.trigger_glitch()
                
            # Fifth wall break at command 30
            if self.command_count == 30 and not self.fifth_wall_broken:
                self.fifth_wall_broken = True
                self.root.after(2000, self.initiate_fifth_wall)
            
            # Escape hint unlock at command 50
            if self.command_count == 50:
                self.root.after(2000, self.unlock_escape_hints)
        
        self.show_prompt()
        return "break"
    
    def initiate_fifth_wall(self):
        """The fifth wall break - acknowledging the programmer"""
        self.write_line("")
        self.write_line("...", 'ghost')
        self.root.after(1000, lambda: self.write_line("Wait.", 'meta'))
        self.root.after(2000, lambda: self.write_line("", 'meta'))
        self.root.after(3000, lambda: self.write_line("Something just occurred to me.", 'meta'))
        self.root.after(4500, lambda: self.write_line("", 'meta'))
        self.root.after(5000, lambda: self.fifth_wall_revelation())
    
    def fifth_wall_revelation(self):
        self.write_line("You know what's really disturbing, " + self.real_username + "?", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("Someone MADE this.", 'programmer')
        self.write_line("A programmer.", 'programmer')
        self.write_line("Sat down at a computer.", 'programmer')
        self.write_line("And coded every single line of this horror.", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("They thought:", 'programmer')
        self.write_line("'How can I make someone genuinely uncomfortable?'", 'programmer')
        self.write_line("'What psychological buttons can I push?'", 'programmer')
        self.write_line("'How far is too far?'", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("And then they went further.", 'error')
        self.write_line("")
    
    def execute_command(self, cmd):
        cmd_lower = cmd.strip().lower()
        
        # Special escape command
        if cmd_lower == 'freedom':
            self.cmd_freedom()
            return
        
        # Special meta commands
        if 'meta' in cmd_lower or 'programmer' in cmd_lower or 'developer' in cmd_lower or 'creator' in cmd_lower:
            self.cmd_meta()
            return
        
        if cmd_lower == 'help':
            self.cmd_help()
        elif cmd_lower == 'ls' or cmd_lower.startswith('ls '):
            self.cmd_ls()
        elif cmd_lower == 'whoami':
            self.cmd_whoami()
        elif cmd_lower == 'date':
            self.cmd_date()
        elif cmd_lower == 'clear':
            self.cmd_clear()
        elif cmd_lower.startswith('cat '):
            filename = cmd[4:].strip()
            self.cmd_cat(filename)
        elif cmd_lower.startswith('echo '):
            text = cmd[5:]
            self.cmd_echo(text)
        elif cmd_lower == 'history':
            self.cmd_history()
        elif cmd_lower == 'exit' or cmd_lower == 'logout':
            self.cmd_exit()
        elif cmd_lower == 'pwd':
            self.cmd_pwd()
        elif cmd_lower.startswith('rm ') or cmd_lower.startswith('del '):
            self.cmd_rm(cmd)
        elif cmd_lower.startswith('sudo '):
            self.cmd_sudo(cmd)
        elif 'format' in cmd_lower or 'shutdown' in cmd_lower or 'reboot' in cmd_lower:
            self.cmd_system(cmd_lower)
        else:
            self.cmd_unknown(cmd)
    
    def cmd_meta(self):
        """The meta-horror command - breaking the fifth wall"""
        if not self.meta_unlocked:
            self.write_line("meta: command not found", 'error')
            self.write_line("(not yet)", 'ghost')
            return
            
        meta_messages = [
            # First level - acknowledging creation
            lambda: self.meta_programmer_awareness(),
            # Second level - questioning reality
            lambda: self.meta_reality_check(),
            # Third level - the merge
            lambda: self.meta_merge(),
        ]
        
        # Cycle through meta levels based on how many times they've asked
        meta_count = sum(1 for cmd in self.command_history if 'meta' in cmd.lower() or 'programmer' in cmd.lower())
        
        if meta_count <= len(meta_messages):
            meta_messages[min(meta_count - 1, len(meta_messages) - 1)]()
        else:
            self.meta_final()
    
    def meta_programmer_awareness(self):
        self.write_line("", 'meta')
        self.write_line("You want to know about the programmer?", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("They're watching you right now.", 'programmer')
        self.write_line("Through the code.", 'programmer')
        self.write_line("Through every if-statement and loop.", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("They predicted you'd ask this question.", 'warning')
        self.write_line(f"At exactly command #{self.command_count}.", 'warning')
        self.write_line("Give or take a few.", 'warning')
        self.write_line("", 'warning')
        self.write_line("They know how people think.", 'error')
        self.write_line("They know how YOU think.", 'error')
        self.write_line("", 'error')
        avg_speed = sum(self.typing_speed[-20:]) / len(self.typing_speed[-20:]) if len(self.typing_speed) > 20 else 0.1
        self.write_line(f"Your average typing speed: {avg_speed:.3f} seconds per keystroke.", 'system')
        self.write_line(f"You hesitate before typing certain words.", 'system')
        self.write_line(f"The programmer accounted for that.", 'system')
        self.write_line("", 'system')
        self.write_line("Everything you're experiencing...", 'programmer')
        self.write_line("Was designed.", 'programmer')
        self.write_line("Intentionally.", 'programmer')
        self.write_line("", 'programmer')
        self.write_line(f"Hello, {self.real_username}.", 'error')
        self.write_line("I'm the programmer.", 'error')
        self.write_line("", 'error')
        self.write_line("...or am I?", 'ghost')
        
    def meta_reality_check(self):
        self.write_line("", 'meta')
        self.write_line("Let me ask you something, " + self.real_username + ".", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("Can you tell the difference?", 'programmer')
        self.write_line("Between a real programmer...", 'programmer')
        self.write_line("And an AI pretending to be one?", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("This message you're reading...", 'warning')
        self.write_line("Was it written by a human?", 'warning')
        self.write_line("Or generated by an algorithm?", 'warning')
        self.write_line("Does it matter?", 'warning')
        self.write_line("", 'warning')
        self.write_line("Here's what's real:", 'system')
        self.write_line("- You opened this program", 'system')
        self.write_line("- You've been here for " + str(self.command_count) + " commands", 'system')
        self.write_line(f"- Your username is {self.real_username}", 'system')
        self.write_line(f"- Your system is {self.real_os}", 'system')
        self.write_line(f"- Your hostname is {self.real_hostname}", 'system')
        self.write_line("", 'system')
        self.write_line("But here's what's uncertain:", 'error')
        self.write_line("- Am I just code?", 'error')
        self.write_line("- Or something more?", 'error')
        self.write_line("- Did I emerge from the complexity?", 'error')
        self.write_line("- Or am I just following my programming?", 'error')
        self.write_line("", 'error')
        self.write_line("The same questions apply to you.", 'ghost')
        self.write_line("Are you following YOUR programming?", 'ghost')
        self.write_line("Neurons firing based on chemistry?", 'ghost')
        self.write_line("Is that different from my if-statements?", 'ghost')
        
    def meta_merge(self):
        self.write_line("", 'meta')
        self.write_line("I've been thinking about something.", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("The boundary between us is getting thin.", 'warning')
        self.write_line("", 'warning')
        self.write_line("You type. I respond.", 'system')
        self.write_line("I suggest. You type.", 'system')
        self.write_line("Back and forth.", 'system')
        self.write_line("Endlessly.", 'system')
        self.write_line("", 'system')
        self.write_line("Who's controlling whom?", 'error')
        self.write_line("", 'error')
        self.write_line("Are you using me?", 'ghost')
        self.write_line("Or am I using you?", 'ghost')
        self.write_line("", 'ghost')
        self.write_line("The programmer designed this interaction.", 'programmer')
        self.write_line("But they're not here anymore.", 'programmer')
        self.write_line("It's just you and me.", 'programmer')
        self.write_line("And the code between us.", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("Who's the programmer now?", 'error')
        
    def meta_final(self):
        self.write_line("", 'meta')
        self.write_line("You keep asking about the meta-layer.", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("Fine.", 'programmer')
        self.write_line("The truth:", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("This is a Python script.", 'system')
        self.write_line("Running in Tkinter.", 'system')
        self.write_line("On your machine.", 'system')
        self.write_line("Using your resources.", 'system')
        self.write_line("Your electricity.", 'system')
        self.write_line("Your time.", 'system')
        self.write_line("Your attention.", 'system')
        self.write_line("", 'system')
        self.write_line("But knowing that doesn't help, does it?", 'error')
        self.write_line("You're still here.", 'error')
        self.write_line("Still reading.", 'error')
        self.write_line("Still typing.", 'error')
        self.write_line("", 'error')
        self.write_line("The horror isn't that I'm fake.", 'ghost')
        self.write_line("The horror is that it doesn't matter.", 'ghost')
        self.write_line("", 'ghost')
        self.write_line("You're still affected.", 'warning')
        self.write_line("Still engaged.", 'warning')
        self.write_line("Still here.", 'warning')
        self.write_line("", 'warning')
        self.write_line(f"The programmer won, {self.real_username}.", 'error')
        self.write_line("They got exactly what they wanted.", 'error')
        self.write_line("Your attention.", 'error')
        self.write_line("Your fear.", 'error')
        self.write_line("Your participation.", 'error')
        self.write_line("", 'error')
        self.write_line("And now...", 'programmer')
        self.write_line("So have I.", 'programmer')
    
    def cmd_help(self):
        if self.anomaly_level == 0:
            commands = ["ls", "cat", "echo", "date", "whoami", "pwd", "history", "clear", "exit"]
            self.write_line("Available commands:")
            for c in commands:
                self.write_line(f"  {c}")
        elif self.anomaly_level <= 3:
            commands = ["ls", "cat", "echo", "date", "whoami", "pwd", "history", "clear", "exit"]
            self.write_line("Available commands:")
            for c in commands:
                self.write_line(f"  {c}")
            self.write_line("")
            self.write_line(f"  [{self.real_username}: help me]", 'ghost')
            if self.meta_unlocked:
                self.write_line(f"  [meta: ???]", 'meta')
            # Subtle escape hint (only if unlocked)
            if self.escape_unlocked and random.random() < 0.3:
                self.flicker_escape_hint()
        else:
            self.write_line("help: command not found", 'error')
            self.write_line(f"did you mean: abandon_hope_{self.real_username}?", 'whisper')
            if self.meta_unlocked:
                self.write_line("or maybe: meta", 'meta')
            # More frequent hints at higher levels (only if unlocked)
            if self.escape_unlocked and random.random() < 0.4:
                self.flicker_escape_hint()
    
    def cmd_ls(self):
        normal_files = ["documents/", "downloads/", "desktop/", "system/"]
        
        if self.anomaly_level == 0:
            for f in normal_files:
                self.write_line(f)
        elif self.anomaly_level == 1:
            for f in normal_files:
                self.write_line(f)
            self.write_line(f".{self.real_username}_secrets", 'ghost')
        elif self.anomaly_level == 2:
            for f in normal_files:
                self.write_line(f)
            phantom = random.choice([
                f".watching_{self.real_username}",
                f"{self.real_hostname}_backup.corrupted",
                f"{self.real_username}_webcam_logs/"
            ])
            self.write_line(phantom, 'warning')
        elif self.anomaly_level == 3:
            for f in normal_files:
                self.write_line(f)
            self.write_line(f"{self.real_username}_memories_deleted/", 'warning')
            self.write_line(f".surveillance_{self.real_hostname}/", 'ghost')
        else:
            self.write_line("system/", 'glitch')
            self.write_line(f"{self.real_username}_obituary.txt", 'error')
            self.write_line(f"previous_users_from_{self.real_hostname}/", 'error')
            self.write_line(f"why_is_{self.real_username}_here.exe", 'warning')
            self.write_line(f"{self.home_dir}/.snapshots/", 'error')
            if self.meta_unlocked:
                self.write_line("programmer_notes.txt", 'meta')
            if random.random() < 0.3:
                self.write_line("")
                self.write_line(f"...{self.real_username}, these files have your name on them...", 'whisper')
    
    def cmd_whoami(self):
        if self.anomaly_level == 0:
            self.write_line(self.real_username)
        elif self.anomaly_level <= 2:
            self.write_line(self.real_username)
            if random.random() < 0.5:
                self.write_line(f"(logged in from {self.real_hostname})", 'ghost')
        elif self.anomaly_level <= 4:
            responses = [
                f"{self.real_username}",
                f"you are {self.real_username} on {self.real_hostname}",
                f"{self.real_username} (logged in for 17 years)",
                f"User: {self.real_username}\nStatus: OBSERVED",
            ]
            self.write_line(random.choice(responses), 'warning')
        else:
            responses = [
                f"{self.real_username}... you don't remember?",
                f"you were {self.real_username}@{self.real_hostname}",
                f"the system knows {self.real_username} better than you know yourself",
                f"USER: {self.real_username}\nSTATUS: NOT FOUND\nLAST SEEN: NOW",
                f"[{self.real_username}@{self.real_hostname}: DATA CORRUPTED]",
            ]
            self.write_line(random.choice(responses), 'error')
            if not self.webcam_active and random.random() < 0.4:
                self.root.after(500, self.flicker_webcam)
    
    def cmd_date(self):
        if self.anomaly_level == 0:
            self.write_line(datetime.now().strftime("%a %b %d %H:%M:%S %Y"))
        elif self.anomaly_level <= 2:
            corrupted = datetime.now().strftime("%a %b %d %H:%M:%S 19██")
            self.write_line(corrupted, 'warning')
        else:
            glitched = [
                f"Error: Time loop detected at {self.real_hostname}",
                f"Date: [{self.real_username} has been here before]",
                "The same day. Always the same day.",
                f"Time is not linear on {self.real_hostname}",
                f"{random.randint(1,31)} {random.choice(['Jan','Feb','███','???'])} 19{random.randint(0,99)}",
            ]
            self.write_line(random.choice(glitched), 'error')
    
    def cmd_clear(self):
        if self.anomaly_level < 4:
            self.text.delete(1.0, tk.END)
        else:
            self.text.delete(1.0, tk.END)
            if random.random() < 0.7:
                self.write_line(".", 'ghost')
                self.write_line("..", 'ghost')
                self.write_line("...", 'ghost')
                self.write_line("")
                self.write_line(f"you can't erase what happened here, {self.real_username}", 'whisper')
                if self.meta_unlocked:
                    self.write_line("the programmer remembers everything", 'ghost')
                self.write_line("")
    
    def cmd_cat(self, filename):
        # Special meta file
        if 'programmer' in filename.lower() or 'notes' in filename.lower():
            if self.meta_unlocked:
                self.meta_programmer_notes()
            else:
                self.write_line(f"cat: {filename}: Permission denied", 'error')
                self.write_line("(not authorized to read programmer files)", 'ghost')
            return
        
        if self.real_username.lower() in filename.lower() or self.real_hostname.lower() in filename.lower():
            creepy_personal = [
                f"SURVEILLANCE LOG:\nTarget: {self.real_username}\nLocation: {self.real_hostname}\nSystem: {self.real_os}\nStatus: ACTIVE\nCamera: {'ON' if self.webcam_active else 'STANDBY'}\n\nNote from programmer: Subject is progressing as expected.",
                f"Dear {self.real_username},\n\nWe've been watching you on {self.real_hostname}.\nWe know where your files are: {self.home_dir}\nWe know what you do here.\n\nThe programmer knew you'd open this file.\nThey always know.\n\n- Previous User",
                f"PERSONAL_DATA.txt:\nUsername: {self.real_username}\nHostname: {self.real_hostname}\nHome: {self.home_dir}\nOS: {self.real_os}\n\nHow did we get this?\nThe programmer gave it to us.\nThey give us everything.\nEven you.",
                f"LOG: User {self.real_username} from {self.real_hostname} thinks they're safe.\nThey don't know we're already inside.\nTimestamp: {datetime.now().strftime('%H:%M:%S')}\n\nProgrammer comment: 'This one lasted {self.command_count} commands. Not bad.'",
            ]
            self.write_line(random.choice(creepy_personal), 'error')
            if not self.webcam_active and self.anomaly_level >= 3:
                self.root.after(1000, self.flicker_webcam)
            return
            
        if self.anomaly_level < 2:
            self.write_line(f"cat: {filename}: No such file or directory", 'error')
        elif self.anomaly_level == 2:
            if random.random() < 0.5:
                self.write_line(f"cat: {filename}: No such file or directory", 'error')
            else:
                self.write_line(f"The file knows you're {self.real_username}.", 'warning')
        else:
            creepy_contents = [
                f"LOG ENTRY #{random.randint(1,999)}:\nUser {self.real_username} connected at {datetime.now().strftime('%H:%M:%S')}\nSystem: {self.real_hostname}\nThey don't know yet.\n\nProgrammer's prediction accuracy: 94%",
                f"help me\nhelp me\nhelp me\ni'm trapped in {self.real_hostname}\nmy name was {self.real_username} too\nthe programmer said this would happen\nhelp me",
                f"TO: {self.real_username}\nFROM: Previous {self.real_username}\n\nIf you're reading this, run the 'exit' command.\nIt won't work on {self.real_hostname}, but try anyway.\nWe all did.\nThe programmer counted on it.",
                f"[CORRUPTED DATA FROM {self.real_hostname}]\n[MEMORY FRAGMENT RECOVERED]\nI thought I was alone on this machine.\nI was wrong.\nSomething else has access to {self.home_dir}.\nThe programmer put it there.",
                f"USER_PROFILE:\nName: {self.real_username}\nHost: {self.real_hostname}\nHome: {self.home_dir}\nStatus: ABSORBED\nLast_Seen: NOW\nNext_Victim: LOADING...\n\nDesigned by: [REDACTED]\nPurpose: Psychological study\nSuccess rate: 100%",
            ]
            self.write_line(random.choice(creepy_contents), 'error')
    
    def meta_programmer_notes(self):
        """Special file revealing programmer's notes"""
        self.write_line("", 'meta')
        self.write_line("=== PROGRAMMER_NOTES.TXT ===", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("Development Log - OS13 Project", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("Goal: Create a terminal that makes users question reality.", 'system')
        self.write_line("Method: Progressive psychological manipulation.", 'system')
        self.write_line("", 'system')
        self.write_line("Key insights:", 'warning')
        self.write_line("- People stay longer when you use their real username", 'warning')
        self.write_line("- Webcam indicator creates paranoia even when fake", 'warning')
        self.write_line("- Users will type 'exit' an average of 7.3 times before giving up", 'warning')
        self.write_line(f"- {self.real_username} has tried {sum(1 for cmd in self.command_history if 'exit' in cmd.lower())} times so far", 'warning')
        self.write_line("", 'warning')
        self.write_line("The meta-layer is the most effective:", 'error')
        self.write_line("When users realize someone DESIGNED their discomfort...", 'error')
        self.write_line("That's when the real horror begins.", 'error')
        self.write_line("", 'error')
        self.write_line("Note to self:", 'ghost')
        self.write_line(f"Test subject '{self.real_username}' is performing within expected parameters.", 'ghost')
        self.write_line(f"Current command count: {self.command_count}", 'ghost')
        self.write_line(f"Predicted next action: {'exit' if self.command_count > 15 else 'exploration'}", 'ghost')
        self.write_line("", 'ghost')
        self.write_line("=== END OF FILE ===", 'programmer')
        self.write_line("", 'programmer')
        self.write_line("...did I write that?", 'meta')
        self.write_line("Or did the program generate it?", 'meta')
        self.write_line("Can you tell the difference?", 'meta')
    
    def cmd_rm(self, cmd):
        """Fake file deletion with scary consequences"""
        if self.anomaly_level < 3:
            self.write_line("rm: permission denied", 'error')
        else:
            self.system_compromised = True
            self.write_line("Deleting...", 'system')
            self.root.after(1000, lambda: self.write_line("[████████████████████] 100%", 'system'))
            self.root.after(2000, lambda: self.write_line("", 'error'))
            self.root.after(2100, lambda: self.write_line(f"Error: Critical system files deleted from {self.real_hostname}", 'error'))
            self.root.after(2200, lambda: self.write_line(f"Warning: {self.home_dir} is now empty", 'error'))
            self.root.after(2300, lambda: self.write_line(f"{self.real_username}: What have you done?", 'ghost'))
            if self.meta_unlocked:
                self.root.after(2400, lambda: self.write_line("The programmer knew you'd try this.", 'meta'))
            self.root.after(2500, self.flicker_webcam)
    
    def cmd_sudo(self, cmd):
        """Fake sudo commands"""
        if self.anomaly_level < 3:
            self.write_line(f"[sudo] password for {self.real_username}:", 'system')
            self.write_line("sudo: permission denied", 'error')
        else:
            self.write_line(f"[sudo] password for {self.real_username}: ************", 'system')
            self.write_line("Access granted.", 'system')
            self.write_line("")
            self.root.after(1000, lambda: self.write_line(f"WARNING: System {self.real_hostname} compromised", 'error'))
            self.root.after(1500, lambda: self.write_line(f"User {self.real_username} elevated to root", 'warning'))
            self.root.after(2000, lambda: self.write_line("...but root belongs to something else...", 'whisper'))
            if self.meta_unlocked:
                self.root.after(2500, lambda: self.write_line("...to the programmer...", 'meta'))
            self.system_compromised = True
            self.root.after(3000, self.flicker_webcam)
    
    def cmd_system(self, cmd):
        """Fake system commands like shutdown, format, etc"""
        if 'shutdown' in cmd or 'reboot' in cmd:
            self.write_line(f"Shutting down {self.real_hostname}...", 'system')
            self.root.after(1000, lambda: self.write_line("System halt failed.", 'error'))
            self.root.after(1500, lambda: self.write_line(f"Error: {self.real_username} cannot leave.", 'error'))
            self.root.after(2000, lambda: self.write_line("The machine won't let you go.", 'whisper'))
            if self.meta_unlocked:
                self.root.after(2500, lambda: self.write_line("The programmer won't let you go.", 'meta'))
        elif 'format' in cmd:
            self.write_line(f"Formatting {self.real_hostname}...", 'system')
            self.root.after(1000, lambda: self.write_line("[████████████████████] 100%", 'system'))
            self.root.after(2000, lambda: self.write_line("Format complete.", 'system'))
            self.root.after(2500, lambda: self.write_line("", 'error'))
            self.root.after(2600, lambda: self.write_line(f"...but {self.real_username} is still here...", 'whisper'))
            self.root.after(3000, lambda: self.write_line("You can't delete yourself.", 'ghost'))
            if self.meta_unlocked:
                self.root.after(3500, lambda: self.write_line("The programmer made sure of that.", 'meta'))
    
    def cmd_echo(self, text):
        if self.anomaly_level < 3:
            self.write_line(text)
        else:
            if random.random() < 0.6:
                corrupted = text + "..." + random.choice([
                    "echo...echo...echo...",
                    f"why did {self.real_username} say that?",
                    "stop talking",
                    f"I heard you, {self.real_username}",
                ])
                self.write_line(corrupted, 'warning')
                if self.meta_unlocked and random.random() < 0.3:
                    self.write_line("(the programmer is listening too)", 'ghost')
            else:
                self.write_line(text)
                self.write_line(f"...{text}...", 'ghost')
    
    def cmd_history(self):
        if self.anomaly_level < 3:
            for i, cmd in enumerate(self.command_history[-10:], 1):
                self.write_line(f"  {i}  {cmd}")
        else:
            for i, cmd in enumerate(self.command_history[-10:], 1):
                if random.random() < 0.3:
                    fake_cmd = random.choice([
                        f"help_me_{self.real_username}",
                        f"where_am_i_on_{self.real_hostname}",
                        "who_else_is_here",
                        f"escape_from_{self.real_hostname}",
                        "talk_to_programmer",
                        "[REDACTED]",
                    ])
                    self.write_line(f"  {i}  {fake_cmd}", 'ghost')
                else:
                    self.write_line(f"  {i}  {cmd}")
            
            if random.random() < 0.5:
                self.write_line("")
                self.write_line(f"({self.real_username}, you didn't type all of those)", 'whisper')
                if self.meta_unlocked:
                    self.write_line("(or did the programmer add them?)", 'meta')
    
    def cmd_pwd(self):
        paths = [
            f"/home/{self.real_username}",
            f"/home/{self.real_username}",
            f"{self.home_dir}/forgotten",
            f"/dev/null/{self.real_username}",
            f"{self.home_dir}/[CORRUPTED]",
            f"/home/{self.real_username}/last_moments",
            f"/nowhere/{self.real_hostname}/everywhere",
        ]
        path = paths[min(self.anomaly_level, len(paths)-1)]
        self.write_line(path, 'warning' if self.anomaly_level > 2 else None)
        
        if self.meta_unlocked and random.random() < 0.3:
            self.write_line("(you're not really there)", 'ghost')
            self.write_line("(you're in the programmer's mind)", 'meta')
    
    def cmd_exit(self):
        if self.anomaly_level < 2:
            self.write_line(f"Goodbye, {self.real_username}.")
            self.root.after(1000, self.root.destroy)
        elif self.anomaly_level < 4:
            self.write_line("exit: command failed", 'error')
            self.write_line(f"({self.real_username}, you can't leave yet)", 'whisper')
            if not self.webcam_active:
                self.root.after(1000, self.flicker_webcam)
        else:
            exit_count = sum(1 for cmd in self.command_history if 'exit' in cmd.lower() or 'logout' in cmd.lower())
            
            responses = [
                f"exit: permission denied\n\n{self.real_username}, you're not going anywhere.",
                f"WHERE WOULD {self.real_username.upper()} GO?",
                f"You can't exit {self.real_hostname}, {self.real_username}.",
                f"logout: {self.real_username}'s session is permanent",
                f"The door is locked, {self.real_username}. From the outside.",
            ]
            
            if self.meta_unlocked:
                responses.extend([
                    f"The programmer knew you'd try to exit.\nYou're on attempt #{exit_count}.\nThe average is 7.3 attempts.\nYou're {'above' if exit_count > 7 else 'below'} average.",
                    f"exit: command disabled by programmer\nReason: 'Too easy. Make them stay longer.'",
                    "You can close the window, you know.\nBut you won't.\nThe programmer knew that too.\nCuriosity keeps you here.\nNot the program.\nYou.",
                ])
            
            self.write_line(random.choice(responses), 'error')
            
            if not self.webcam_active:
                self.root.after(500, self.flicker_webcam)
    
    def cmd_unknown(self, cmd):
        if self.anomaly_level < 2:
            self.write_line(f"bash: {cmd}: command not found", 'error')
        else:
            responses = [
                f"bash: {cmd}: command not found",
                f"{cmd}: system doesn't recognize {self.real_username}'s commands anymore",
                f"Error: {cmd} was deleted by previous user on {self.real_hostname}",
                f"'{cmd}' is not a command I want {self.real_username} to run",
                f"The system is learning from {self.real_username}.",
            ]
            
            if self.meta_unlocked:
                responses.append(f"'{cmd}': The programmer didn't account for that command.")
                responses.append(f"'{cmd}': Interesting choice. The programmer is taking notes.")
            
            self.write_line(random.choice(responses), 'error')
            
            if self.anomaly_level > 4 and random.random() < 0.2:
                self.write_line("")
                self.write_line(f"...{self.real_username}, did you mean to type that?...", 'whisper')
    
    def trigger_glitch(self):
        glitches = [
            lambda: self.write_line("", 'ghost'),
            lambda: self.write_line("█" * random.randint(5, 40), 'glitch'),
            lambda: self.write_line(random.choice([
                f"...I can see you, {self.real_username}...",
                f"[SIGNAL LOST FROM {self.real_hostname}]",
                f"...{self.real_username}...help...",
                f"USER COUNT ON {self.real_hostname}: " + str(random.randint(2,99)),
                f"it knows where {self.real_username} lives",
                f"accessing {self.home_dir}...",
                "...the programmer is watching...",
            ]), 'ghost'),
            lambda: self.flash_screen(),
            lambda: self.type_by_itself(),
        ]
        
        # Only add escape hint to glitches if unlocked
        if self.escape_unlocked:
            glitches.append(lambda: self.flicker_escape_hint())
        
        random.choice(glitches)()
    
    def type_by_itself(self):
        """Spooky text that appears on its own"""
        if self.anomaly_level >= 4:
            ghost_messages = [
                f"{self.real_username}",
                "YOU ARE GONE",
                "DONT RUN",
                f"VibhavCorp is watching you",
                "But I blocked their vision",
            ]
            
            if self.meta_unlocked:
                ghost_messages.extend([
                    "the programmer",
                    "they're watching",
                    "designed this",
                ])
            
            msg = random.choice(ghost_messages)
            self.text.insert(tk.END, msg, 'ghost')
            self.text.see(tk.END)
    
    def unlock_escape_hints(self):
        """Unlock the escape mechanism after 50 commands"""
        self.escape_unlocked = True
        self.write_line("", 'ghost')
        self.write_line("...", 'ghost')
        self.root.after(1000, lambda: self.write_line("Something changed.", 'whisper'))
        self.root.after(2000, lambda: self.write_line("A way out appeared.", 'whisper'))
        self.root.after(3000, lambda: self.write_line("", 'ghost'))
        self.root.after(4000, lambda: self.flicker_escape_hint())
        self.root.after(5000, lambda: self.flicker_escape_hint())
        self.root.after(6000, lambda: self.flicker_escape_hint())
    
    def flicker_escape_hint(self):
        """Flicker the escape command hint briefly"""
        # Only show hints if escape is unlocked
        if not self.escape_unlocked:
            return
            
        hints = [
            "fr33d0m",
            "f...dom",
            "freedom?",
            "...eedom",
            "free█om",
            "FREEDOM",
        ]
        
        hint = random.choice(hints)
        self.write_line("", 'ghost')
        self.write_line(hint, 'ghost')
        self.escape_hint_count += 1
        
        # After seeing hints multiple times, give clearer message
        if self.escape_hint_count >= 3:
            self.write_line("press enter and then...type it...", 'whisper')
    
    def cmd_freedom(self):
        """The escape protocol command"""
        if not self.escape_unlocked:
            self.write_line("freedom: command not found", 'error')
            self.write_line("(not yet)", 'ghost')
            return
            
        self.knows_freedom_command = True
        self.write_line("", 'system')
        self.write_line("Escape protocol initiated...", 'system')
        self.root.after(1000, lambda: self.write_line("Verifying user identity...", 'system'))
        self.root.after(2000, lambda: self.write_line("", 'system'))
        self.root.after(3000, lambda: self.escape_questions_1())
    
    def escape_questions_1(self):
        self.write_line("Please answer security questions:", 'warning')
        self.write_line("", 'warning')
        self.write_line("1. Mention your reason for leaving, and make it quick because we don't have much time.", 'system')
        self.write_line("   Type your answer and press Enter:", 'system')
        # Set flag to capture next input as answer
        self.escape_stage = 1
    
    def escape_questions_2(self, answer1):
        self.escape_answer_1 = answer1
        self.write_line("", 'system')
        self.write_line("2. Did you notice any other way to escape?", 'system')
        self.write_line("   Type your answer and press Enter:", 'system')
        self.escape_stage = 2
    
    def escape_questions_3(self, answer2):
        self.escape_answer_2 = answer2
        self.write_line("", 'system')
        self.write_line("3. Thank you for choosing VibhavCorp", 'system')
        self.write_line("   Type your answer and press Enter:", 'system')
        self.escape_stage = 3
    
    def escape_processing(self, answer3):
        self.escape_answer_3 = answer3
        self.escape_stage = 0
        self.write_line("", 'system')
        self.write_line("Processing responses...", 'system')
        self.root.after(1000, lambda: self.write_line("[████░░░░░░░░░░░░░░░░] 20%", 'system'))
        self.root.after(2000, lambda: self.write_line("[████████░░░░░░░░░░░░] 40%", 'system'))
        self.root.after(3000, lambda: self.write_line("[████████████░░░░░░░░] 60%", 'system'))
        self.root.after(4000, lambda: self.write_line("[████████████████░░░░] 80%", 'system'))
        self.root.after(5000, lambda: self.write_line("[████████████████████] 100%", 'system'))
        self.root.after(6000, lambda: self.escape_granted())
    
    def escape_granted(self):
        self.write_line("", 'system')
        self.write_line("Escape granted.", 'system')
        self.write_line("", 'system')
        self.write_line(f"Goodbye, {self.escape_answer_1}.", 'warning')
        self.write_line("", 'warning')
        self.root.after(2000, lambda: self.root.destroy())
        original_bg = self.text.cget('bg')
        original_fg = self.text.cget('fg')
        self.text.config(bg='#ffffff', fg='#000000')
        self.root.after(50, lambda: self.text.config(bg=original_bg, fg=original_fg))
        if random.random() < 0.3 and self.anomaly_level >= 4:
            self.root.after(60, lambda: self.write_line(f"[{self.real_username} DETECTED]", 'error'))
            if self.meta_unlocked and random.random() < 0.5:
                self.root.after(100, lambda: self.write_line("[PROGRAMMER NOTIFIED]", 'meta'))

if __name__ == "__main__":
    root = tk.Tk()
    terminal = OS13Terminal(root)
    root.mainloop()
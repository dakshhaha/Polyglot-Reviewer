# main.py
import re
import os
import time
import platform
import random
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.prompt import Prompt

# --- Configuration ---
# A simple mock "database" of review rules for different languages
REVIEW_RULES = {
    "python": [
        {"regex": r"def\s+[A-Z]", "message": "Function names should be snake_case.", "type": "style"},
        {"regex": r"print\(.*\)", "message": "Found a 'print' statement. Ensure it's not for debugging.", "type": "suggestion"},
        {"regex": r".{90,}", "message": "Line exceeds 88 characters, consider breaking it up.", "type": "style"},
        {"regex": r"except\s*:", "message": "Avoid bare 'except:' clauses. Specify the exception type.", "type": "warning"},
    ],
    "javascript": [
        {"regex": r"var\s+", "message": "Consider using 'let' or 'const' instead of 'var'.", "type": "suggestion"},
        {"regex": r"==(?!=)", "message": "Use strict equality '===' instead of '==' to avoid type coercion bugs.", "type": "warning"},
        {"regex": r"function\s+[A-Z]", "message": "Function names are typically camelCase in JavaScript.", "type": "style"},
        {"regex": r"console\.log\(.*\)", "message": "Found 'console.log'. Remove before deploying to production.", "type": "suggestion"},
    ],
    "java": [
        {"regex": r"catch\s*\(\s*Exception\s+e\s*\)\s*{\s*}", "message": "Empty catch block. At least log the exception.", "type": "warning"},
        {"regex": r"public\s+class\s+[a-z]", "message": "Class names should start with an uppercase letter (PascalCase).", "type": "style"},
        {"regex": r"String\s*==", "message": "Do not use '==' to compare Strings. Use '.equals()' instead.", "type": "error"},
    ],
    "cpp": [
        {"regex": r"using namespace std;", "message": "'using namespace std;' is bad practice in headers.", "type": "warning"},
        {"regex": r"goto\s+\w+;", "message": "Use of 'goto' is heavily discouraged.", "type": "warning"},
        {"regex": r"new\s+[a-zA-Z0-9_]+(\[.*\])?(?!;)", "message": "Potential memory leak. Does every 'new' have a corresponding 'delete'?", "type": "error"},
    ],
    "go": [
        {"regex": r"fmt\.Println", "message": "Found 'Println'. Consider using a structured logger in production.", "type": "suggestion"},
    ],
    "rust": [
         {"regex": r"\.unwrap\(\)", "message": "'.unwrap()' can cause a panic. Use 'match' or 'if let' for robust error handling.", "type": "warning"},
         {"regex": r"mut\s+\w+:", "message": "Mutable variable declared. Ensure its scope of mutability is as small as possible.", "type": "suggestion"},
    ]
}

FILE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".go": "go",
    ".rs": "rust",
}

class HackerTerminal:
    """
    A powerful, hacker-themed terminal UI for reviewing code files.
    """
    def __init__(self):
        self.console = Console()

    def animated_text(self, text, style="bold green"):
        """Helper function to print text with a typing animation."""
        for char in text:
            self.console.print(f"[{style}]{char}[/{style}]", end="")
            time.sleep(0.02)
        self.console.print()

    def print_welcome(self):
        """Prints the hacker-style welcome banner."""
        # Switched to a clearer, block-style ASCII art
        ascii_art = r"""
██████╗ ██╗      ██████╗ ██╗   ██╗  ██████╗ ████████╗
██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝ ██╔════╝ ╚══██╔══╝
██████╔╝██║     ██║   ██║ ╚████╔╝  ██║  ███╗   ██║   
██╔═══╝ ██║     ██║   ██║  ╚██╔╝   ██║   ██║   ██║   
██║     ███████╗╚██████╔╝   ██║    ╚██████╔╝   ██║   
╚═╝     ╚══════╝ ╚═════╝    ╚═╝     ╚═════╝    ╚═╝   
        """
        welcome_message = (
            f"[bold green]{ascii_art}[/bold green]\n\n"
            "[bold]Polyglot Code Reviewer[/bold] [dim]v2.5[/dim]\n"
            "[dim]-- unauthorized access detected --[/dim]"
        )
        self.console.print(Panel(
            welcome_message,
            title="[red]SYSTEM BREACH[/red]",
            border_style="bold red",
            padding=(1, 2)
        ))
        self.animated_text(">>> Type 'help' for available commands or 'exit' to cover your tracks.")

    def print_help(self):
        """Prints the help message with command usage."""
        table = Table(
            title="[bold green]:: [white]Command Matrix[/white] ::[/bold green]",
            show_header=True,
            header_style="bold white on green",
            border_style="green"
        )
        table.add_column("Directive", style="cyan", width=20)
        table.add_column("Functionality")

        table.add_row("review <file_path>", "Initiate deep code analysis on a target file.")
        table.add_row("scan", "Scan current directory for injectable code targets.")
        table.add_row("sysinfo", "Display compromised system information.")
        table.add_row("help", "Display this command matrix.")
        table.add_row("clear", "Wipe terminal traces.")
        table.add_row("exit", "Terminate session and erase logs.")

        self.console.print(table)

    def print_sysinfo(self):
        """Displays mock system information for thematic effect."""
        panel_content = (
            f"[green]Kernel[/green]:\t\t[bold white]{platform.system()} {platform.release()}[/bold white]\n"
            f"[green]Hostname[/green]:\t[bold white]matrix-node-07[/bold white]\n"
            f"[green]User[/green]:\t\t[bold red]root[/bold red]\n"
            f"[green]Network[/green]:\t[bold white]eth0 @ 10.0.7.21[/bold white]\n"
            f"[green]Uptime[/green]:\t\t[bold white]217 days, 14:03:51[/bold white]"
        )
        self.console.print(Panel(panel_content, title="[bold green]System Status[/bold green]", border_style="green"))

    def scan_directory(self):
        """Scans the current directory for supported file types."""
        self.console.print("\n[yellow]Scanning for targets in current directory...[/yellow]")
        targets = []
        with os.scandir('.') as it:
            for entry in it:
                if entry.is_file():
                    _, ext = os.path.splitext(entry.name)
                    if ext in FILE_EXTENSIONS:
                        targets.append((entry.name, FILE_EXTENSIONS[ext]))

        if not targets:
            self.console.print("[red]No valid targets found.[/red]")
            return

        table = Table(title="[bold green]Scan Results[/bold green]", border_style="green")
        table.add_column("Filename", style="cyan")
        table.add_column("Detected Language", style="yellow")

        for name, lang in targets:
            table.add_row(name, lang)
        
        self.console.print(table)

    def review_file(self, file_path):
        """Analyzes a given file and prints the report with a hacker theme."""
        if not os.path.exists(file_path):
            self.console.print(f"[bold red]FATAL:[/bold red] Target file not found at '{file_path}'")
            return

        _, ext = os.path.splitext(file_path)
        language = FILE_EXTENSIONS.get(ext)

        if not language:
            self.console.print(f"[bold red]ERROR:[/bold red] Unknown file type: '{ext}'. Cannot compile rule set.")
            return
        
        self.animated_text(f">>> Initializing analysis engine for {language} payload...")
        time.sleep(0.5)
        self.animated_text(">>> Parsing Abstract Syntax Tree...")
        time.sleep(0.5)
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None, style="green", complete_style="bold green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            transient=True
        ) as progress:
            task = progress.add_task("[green]Applying vulnerability rule set...[/green]", total=100)
            while not progress.finished:
                progress.update(task, advance=1.5)
                time.sleep(0.02)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.console.print(f"\n[bold]Execution Report: [cyan]{file_path}[/cyan] ([green]{language}[/green])[/bold]")
        
        syntax = Syntax(content, language, theme="monokai", line_numbers=True)
        self.console.print(Panel(syntax, title="[green]Source Code Intercept[/green]", border_style="green"))

        lines = content.split('\n')
        findings = []
        rules = REVIEW_RULES.get(language, [])
        for i, line in enumerate(lines, 1):
            for rule in rules:
                if re.search(rule["regex"], line):
                    findings.append({"line": i, "message": rule["message"], "type": rule["type"]})
        
        if not findings:
            self.console.print("\n[bold green]Target is clean. No vulnerabilities found.[/bold green] :lock:")
            return

        report_table = Table(title="[bold]Vulnerability Assessment[/bold]", show_header=True, header_style="bold red")
        report_table.add_column("LNC", style="dim", width=6)
        report_table.add_column("Class", width=12)
        report_table.add_column("Intel")

        type_styles = {
            "error": "[bold red]CRITICAL[/bold red]",
            "warning": "[bold yellow]HIGH[/bold yellow]",
            "suggestion": "[bold cyan]MEDIUM[/bold cyan]",
            "style": "[bold magenta]LOW[/bold magenta]",
        }

        for find in findings:
            report_table.add_row(
                str(find["line"]),
                type_styles.get(find["type"], find["type"].upper()),
                find["message"]
            )
        
        self.console.print(report_table)

    def run(self):
        """Main application loop."""
        os.system('cls' if os.name == 'nt' else 'clear') # Force clear console
        self.print_welcome()
        
        while True:
            try:
                prompt_text = "[bold red]root@polyglot[/bold red][white]:[/white][bold blue]~#[/bold blue] "
                command_str = Prompt.ask(prompt_text, console=self.console)
                parts = command_str.strip().split()
                if not parts:
                    continue
                
                command = parts[0].lower()

                if command == "exit":
                    self.animated_text("\n>>> Terminating session...", style="bold yellow")
                    time.sleep(0.5)
                    self.animated_text(">>> Wiping logs...", style="bold yellow")
                    time.sleep(1)
                    self.console.print("[bold red]CONNECTION TERMINATED.[/bold red]")
                    break
                elif command == "help":
                    self.print_help()
                elif command == "clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_welcome()
                elif command == "sysinfo":
                    self.print_sysinfo()
                elif command == "scan":
                    self.scan_directory()
                elif command == "review":
                    if len(parts) > 1:
                        self.review_file(parts[1])
                    else:
                        self.console.print("[bold red]ERROR:[/bold red] Target file required. Usage: review <file_path>")
                else:
                    self.console.print(f"[bold red]ERROR:[/bold red] Unknown directive '{command}'. Type 'help' for options.")

            except KeyboardInterrupt:
                self.console.print("\n[bold yellow]Forced termination signal detected. Wiping traces...[/bold yellow]")
                break
            except Exception as e:
                self.console.print(f"[bold red]FATAL KERNEL PANIC: {e}[/bold red]")

if __name__ == "__main__":
    # To test this, create a dummy file e.g., 'test.js' with some code.
    # Example test.js:
    # var x = 10;
    # function MyFunc() { console.log('hello'); }
    # if (x == '10') { /* do something */ }
    
    # Then run the script and type: review test.js or scan
    
    bot = HackerTerminal()
    bot.run()

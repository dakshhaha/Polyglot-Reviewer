Polyglot Reviewer CLI

A High-Level Code Analysis & Vulnerability Scanner with a Hacker-Themed UI.

This isn't your average linter. The Polyglot Reviewer is a command-line tool designed to look and feel like a sophisticated hacking utility, providing deep code analysis for multiple programming languages. It identifies potential vulnerabilities, stylistic issues, and common errors, all within a slick, terminal-based interface.

Core Features

- Multi-Language Payload Analysis: Supports a wide range of languages including Python, JavaScript, Java, C++, Go, and Rust.

- Vulnerability Assessment: Classifies findings into CRITICAL, HIGH, MEDIUM, and LOW severities.

- Immersive Hacker UI: Built with rich to provide a visually appealing and interactive terminal experience.

- Target Scanning: Automatically scans directories to find supported code files to analyze.

- Thematic Experience: From the "SYSTEM BREACH" welcome message to the command directives, every element is designed to fit the theme.

Getting Started

To get the tool running on your local machine, follow these steps.

Prerequisites

Python 3.6+

pip package manager

Installation & Setup

Clone the repository:
git clone https://github.com/your-username/polyglot-reviewer.git
cd polyglot-reviewer

Install dependencies:
The only external dependency is the rich library for the UI.
pip install rich

Execute the tool:
Run the main.py script to launch the terminal interface.
python main.py

Command Matrix

Once the tool is running, you can use the following directives:

Directive: review 

Directive: scan
Functionality: Scan current directory for injectable code targets.

Directive: sysinfo
Functionality: Display compromised system information.

Directive: help
Functionality: Display this command matrix.

Directive: clear
Functionality: Wipe terminal traces.

Directive: exit
Functionality: Terminate session and erase logs.

Contributing

Contributions to the Polyglot Reviewer are welcome. If you have ideas for new rules, support for more languages, or UI enhancements, feel free to fork the repository and submit a pull request.

Fork the Project

Create your Feature Branch (git checkout -b feature/NewPayload)

Commit your Changes (git commit -m 'Add new payload')

Push to the Branch (git push origin feature/NewPayload)

Open a Pull Request

License

Distributed under the Apache License 2.0. See LICENSE and NOTICE files for more information.
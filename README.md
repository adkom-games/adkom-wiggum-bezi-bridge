# ADKOM Wiggum-Bezi Python Bridge

Ralph Wiggum comes to Bezi!

This is an automated bridge for interacting with the **[Bezi](https://www.bezi.com)** desktop application using Python and PowerShell, implementing the [Ralph Wiggum](https://github.com/ghuntley/how-to-ralph-wiggum) loop for **Bezi**. This tool handles automated prompting, thread management, and synchronization with Bezi's AI history via `pywinauto`.

## Features

* **UPM Integration:** Install directly into Unity via Git URL.
* **Automated UI Interaction:** Uses `pywinauto` to handle window focus, text input, and button interactions.
* **Self-Healing Environment:** PowerShell script automatically manages the Python Virtual Environment (`.venv`).
* **Performance Logging:** Automatically tracks the duration of every AI iteration and exports data to `bezi_performance.csv`.
* **Robust Prompting:** Uses temporary file passing to bypass Windows command-line character limits.

## Requirements

* **Windows OS** (Required for `pywinauto` / UIA backend).
* **[Python 3.x](https://www.python.org/)** (With the Python Launcher `py` installed).
* **[Bezi Desktop App](https://www.bezi.com)** installed.

## Installation & Setup (Unity)

1. Clone the repo into /Assets/BeziBridge.
2. The specification for what game to build is in /Assets/BeziBridge/specs, the default spec describes a Roll-A-Ball type game.

## Usage

The bridge logic is driven by the `loop.ps1` script located in the package folder.

1.  Open PowerShell in the package directory.
2.  Run the loop with your desired mode:

| Command | Description |
| :--- | :--- |
| `.\loop.ps1` | Build mode, unlimited iterations. |
| `.\loop.ps1 20` | Build mode, max 20 iterations. |
| `.\loop.ps1 plan` | Plan mode, unlimited iterations. |
| `.\loop.ps1 plan 5` | Plan mode, max 5 iterations. |

### Performance Tracking
Upon completion, the script generates an **Execution Report** in the terminal and appends the data to `bezi_performance.csv`. This allows you to monitor if the AI response time increases as the conversation history grows.

## How it Works

1.  **Initialization:** `loop.ps1` ensures Python dependencies are installed.
2.  **Prompt Sync:** The script reads your `PROMPT_build.md` or `PROMPT_plan.md`.
3.  **Bridge Execution:** `bezi_bridge.py` uses `pywinauto` to find the Bezi Tauri window, starts a new Bezi "Thread" with a clean context, and sends the prompt.
4.  **Telemetry:** The duration of the round-trip is recorded for performance analysis.

## Links

- [Bezi](https://www.bezi.com)
- [Geoffrey Huntley - Ralph Wiggum as a "software engineer"](https://ghuntley.com/ralph/)
- [GitHub - Ralph Wiggum](https://github.com/ghuntley/how-to-ralph-wiggum)
- [Python 3.x](https://www.python.org/)

## Supported Platforms

This is a Windows-only product, due to dependencies on pywinauto, and the loop.ps1 script.

## License

Distributed under the MIT License. See [`LICENSE.txt`](file:/LICENSE.txt) for more information.

# Script Runner

Script Runner is a command-line tool that helps you manage and run Python scripts with their associated virtual environments. It automatically detects virtual environments and allows you to create aliases for your scripts, making them easier to run from anywhere.

## Features

- Register Python scripts with easy-to-remember aliases
- Automatic virtual environment detection for Python scripts
- Run scripts using their associated Python environment
- List all registered scripts
- Remove scripts from the registry
- Prune non-existent scripts automatically
- Cross-platform support (Windows and Unix-like systems)

## Installation

```bash
pip install script_runner
```

## Quick Start

1. Register a script:
```bash
script_runner add path/to/your/script.py -a myscript
```

2. Run the script using its alias:
```bash
script_runner run myscript [args...]
```

## Commands

- `add`: Register a Python script
  ```bash
  script_runner add PATH [-a ALIAS] [-p PYTHON_PATH]
  ```
  - `PATH`: Path to the Python script
  - `-a, --alias`: Custom alias for the script (defaults to script filename)
  - `-p, --python`: Specific Python executable to use (auto-detected if not specified)

- `run`: Execute a registered script
  ```bash
  script_runner run ALIAS [ARGS...]
  ```
  - `ALIAS`: The script's alias
  - `ARGS`: Optional arguments to pass to the script

- `list`: Display all registered scripts
  ```bash
  script_runner list
  ```

- `remove`: Delete a script from the registry
  ```bash
  script_runner remove ALIAS
  ```

- `prune`: Remove all non-existent scripts from the registry
  ```bash
  script_runner prune
  ```

## Configuration

Script Runner stores its configuration in `~/.config/script_runner/scripts.json`. This file contains the mapping between aliases and their corresponding scripts, along with the Python executable path for each script.

## Virtual Environment Detection

Script Runner automatically detects virtual environments by looking for `pyvenv.cfg` files in parent directories (up to 5 levels by default). It will use the Python executable from the nearest virtual environment found. If no virtual environment is detected, it will use the system Python that was used to install Script Runner.

## Requirements

- Python 3.8 or higher
- Click 8.0 or higher

## Aliases

The tool can be invoked using either `script_runner` or the shorter alias `sr`:

```bash
sr add script.py
sr run myscript
```

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment
3. Install development dependencies
4. Run tests with pytest

The project uses pytest for testing. Test files are available in the project root and cover core functionality like virtual environment detection and script registration.

## License

This project is licensed under the MIT License. This means you can:
- Use it commercially
- Modify it
- Distribute it
- Use it privately
- Use it for any purpose

No warranties are provided and the author is not liable for any issues.

## Contributing

This is a personal utility project with minimal maintenance. While you're welcome to:
- Fork the repository
- Use it as you see fit
- Create your own version

Please note that I may not actively review pull requests or issues. Feel free to fork and modify the project to suit your needs.

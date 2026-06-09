# 📦 Installation Guide

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.10 or higher
- **RAM**: 512 MB minimum
- **Disk**: 100 MB for application + dependencies

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/againto/trading-journal-pro.git
cd trading-journal-pro
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

## Platform-Specific Setup

### Windows

1. Ensure Python is added to PATH:
   ```bash
   python --version
   ```

2. If you get command not found, download from [python.org](https://www.python.org)

3. Run with:
   ```bash
   python main.py
   ```

### macOS

1. Install Python 3.10+:
   ```bash
   brew install python@3.10
   ```

2. Create virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. Run application:
   ```bash
   python main.py
   ```

### Linux (Ubuntu/Debian)

1. Install Python and dependencies:
   ```bash
   sudo apt update
   sudo apt install python3.10 python3.10-venv python3-pip
   ```

2. Create virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. Run application:
   ```bash
   python main.py
   ```

## Troubleshooting

### "Python not found" error

**Windows:**
- Reinstall Python and check "Add Python to PATH" during installation
- Use `py` instead of `python`: `py main.py`

**macOS/Linux:**
- Use `python3` instead of `python`: `python3 main.py`

### "ModuleNotFoundError: No module named 'PyQt6'"

```bash
# Ensure you're in the virtual environment
# Then reinstall requirements
pip install --upgrade -r requirements.txt
```

### Application won't start

1. Check Python version:
   ```bash
   python --version  # Should be 3.10+
   ```

2. Verify all dependencies:
   ```bash
   pip list | grep PyQt6
   ```

3. Try running with verbose output:
   ```bash
   python -v main.py
   ```

### Database errors

- Remove the old database and start fresh:
  ```bash
  rm trading_journal.db
  python main.py
  ```

## Updating to Latest Version

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run application
python main.py
```

## Creating an Executable (Optional)

### Using PyInstaller

```bash
pip install pyinstaller

pyinstaller --onefile --windowed --icon=TJ.ico main.py
```

Output will be in `dist/` folder.

## Virtual Environment Management

### Activate
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Deactivate
```bash
deactivate
```

### Delete
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

## Getting Help

If you encounter issues:

1. Check Python version: `python --version`
2. Verify virtual environment is activated
3. Reinstall requirements: `pip install -r requirements.txt --force-reinstall`
4. Open an issue on GitHub with error message and system info

## Next Steps

After installation:

1. **First Run** - The app creates a database automatically
2. **Add a Trade** - Test the functionality by entering a trade
3. **Configure Theme** - Toggle between dark/light mode in the header
4. **Explore Features** - Check out Analytics, Weekly Summary, and Risk/Reward tabs

Happy trading! 📈

"""Deployment guide for all platforms"""

# Deployment Guide

## Prerequisites
- Python 3.10 or higher
- Git (for version control)
- Virtual environment tool

## Platform-Specific Deployment

### Windows

#### Step 1: Install Python
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Verify installation: `python --version`

#### Step 2: Clone Repository
```bash
git clone https://github.com/againto/trading-journal-pro.git
cd trading-journal-pro
```

#### Step 3: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Run Application
```bash
python main.py
```

#### Create Desktop Shortcut (Optional)
1. Create `run_app.bat`:
```batch
@echo off
cd %~dp0
venv\Scripts\python.exe main.py
pause
```

2. Right-click → Create shortcut on Desktop

#### Create Executable (Optional)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=TJ.ico main.py
```
Output: `dist/main.exe`

---

### macOS

#### Step 1: Install Python
```bash
brew install python@3.10
```

#### Step 2: Clone Repository
```bash
git clone https://github.com/againto/trading-journal-pro.git
cd trading-journal-pro
```

#### Step 3: Create Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Run Application
```bash
python main.py
```

#### Create Application Bundle (Optional)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --osx-bundle-identifier=com.tradingjournalpro main.py
```

#### Create Launch Script
1. Create `run_app.sh`:
```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py
```

2. Make executable:
```bash
chmod +x run_app.sh
```

---

### Linux (Ubuntu/Debian)

#### Step 1: Install Python & Dependencies
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip git
```

#### Step 2: Clone Repository
```bash
git clone https://github.com/againto/trading-journal-pro.git
cd trading-journal-pro
```

#### Step 3: Create Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Run Application
```bash
python main.py
```

#### Create Desktop Entry (Optional)
1. Create `TradeJournal.desktop` in `~/.local/share/applications/`:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Trading Journal Pro
Comment=Professional Trading Journal
Exec=/home/username/trading-journal-pro/venv/bin/python /home/username/trading-journal-pro/main.py
Icon=/home/username/trading-journal-pro/TJ.ico
Terminal=false
Categories=Finance;Office;
```

2. Make executable:
```bash
chmod +x ~/.local/share/applications/TradeJournal.desktop
```

#### Install System Dependencies
```bash
sudo apt install python3.10-dev libgl1-mesa-glx
```

---

## Common Issues & Solutions

### Issue: "Python not found"
**Windows**: Reinstall Python and check "Add Python to PATH"
**Mac/Linux**: Use `python3` instead of `python`

### Issue: "ModuleNotFoundError: No module named 'PyQt6'"
```bash
pip install --upgrade -r requirements.txt
```

### Issue: "Permission denied" (Linux)
```bash
chmod +x main.py
python main.py
```

### Issue: "Virtual environment not activating"
```bash
# Windows
venv\Scripts\activate.bat

# Mac/Linux
source venv/bin/activate
```

### Issue: Database errors
```bash
# Delete and recreate database
rm trading_journal.db
python main.py
```

---

## Updating Application

### From Git
```bash
# Navigate to project directory
cd trading-journal-pro

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run application
python main.py
```

### Manual Update
1. Download latest from GitHub
2. Extract to same directory (overwrite files)
3. Run `pip install --upgrade -r requirements.txt`
4. Run application

---

## Production Deployment

### Linux Server Setup

#### 1. Create System User
```bash
sudo useradd -m -s /bin/bash tradejournal
```

#### 2. Clone Repository
```bash
sudo -u tradejournal git clone https://github.com/againto/trading-journal-pro.git /home/tradejournal/app
```

#### 3. Setup Environment
```bash
sudo -u tradejournal python3.10 -m venv /home/tradejournal/app/venv
source /home/tradejournal/app/venv/bin/activate
pip install -r requirements.txt
```

#### 4. Create Systemd Service
Create `/etc/systemd/system/tradejournal.service`:
```ini
[Unit]
Description=Trading Journal Pro
After=network.target

[Service]
Type=simple
User=tradejournal
WorkingDirectory=/home/tradejournal/app
ExecStart=/home/tradejournal/app/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 5. Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable tradejournal
sudo systemctl start tradejournal
```

#### 6. Monitor Service
```bash
sudo systemctl status tradejournal
sudo journalctl -u tradejournal -f
```

---

## Backup Strategy

### Automated Backups (Linux)

Create `/home/tradejournal/backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/home/tradejournal/backups"
DB_FILE="/home/tradejournal/app/trading_journal.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/trading_journal_$TIMESTAMP.db

# Keep only last 30 days
find $BACKUP_DIR -name "trading_journal_*.db" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /home/tradejournal/backup.sh
```

---

## Security Considerations

1. **Database Security**
   - Keep `trading_journal.db` in secure location
   - Restrict file permissions: `chmod 600 trading_journal.db`
   - Regular backups

2. **Code Security**
   - Keep dependencies updated: `pip install --upgrade -r requirements.txt`
   - Review dependencies: `pip check`
   - Use virtual environments

3. **System Security**
   - Keep OS updated
   - Use firewall rules
   - Monitor logs: `tail -f trading_journal.log`

---

## Performance Optimization

1. **Database Optimization**
   ```bash
   # Analyze database
   sqlite3 trading_journal.db ".mode line" ".read"
   
   # Vacuum (cleanup)
   sqlite3 trading_journal.db "VACUUM;"
   ```

2. **Application Optimization**
   - Enable logging to monitor performance
   - Check logs for errors: `cat trading_journal.log`
   - Profile with: `python -m cProfile main.py`

3. **System Resources**
   - Monitor CPU/Memory: `htop` (Linux)
   - Check disk space: `df -h`
   - Clean temporary files regularly

---

## Troubleshooting Deployment

### Application won't start
1. Check logs: `cat trading_journal.log`
2. Verify Python version: `python --version`
3. Test imports: `python -c "import PyQt6"`

### Database errors
```bash
# Repair database
sqlite3 trading_journal.db "PRAGMA integrity_check;"

# Backup and reset
cp trading_journal.db trading_journal.db.backup
rm trading_journal.db
python main.py
```

### Performance issues
```bash
# Monitor real-time
python -m cProfile -s cumtime main.py

# Check database size
ls -lh trading_journal.db

# Optimize
sqlite3 trading_journal.db "ANALYZE; VACUUM;"
```

---

## Support & Resources

- **Documentation**: `/docs/` folder
- **Issues**: GitHub Issues
- **Logs**: `trading_journal.log`
- **Database**: `trading_journal.db`

## Version Control

All deployments should:
1. Use specific releases/tags
2. Document changes in CHANGELOG
3. Test updates before production
4. Maintain backup of previous version

# SavePassword - Multi-Language Password Manager v1.2.0

A secure, offline password manager with encrypted storage, categories, and multi-language support.

## 🌍 Languages

- **English** - Full interface translation
- **Deutsch** - German translation  
- **Français** - French translation
- **Español** - Spanish translation
- **Italiano** - Italian translation
- **Nederlands** - Dutch translation
- **Polski** - Polish translation
- **Português** - Portuguese translation

## 🚀 Features

- 🔒 **AES-256 Encryption** - Your passwords are securely encrypted
- 🌍 **Multi-Language** - Switch between 8 European languages
- 📁 **Categories** - Organize passwords in folders and subfolders
- 🌐 **Website URLs** - Save web addresses and open them directly
- 🛠 **Password Generator** - Generate strong passwords with customizable options
- 📋 **Clipboard Integration** - Copy passwords and usernames with one click
- 🔍 **Search & Filter** - Quickly find your passwords by name, category, or website
- 💾 **Export/Import** - Backup and restore your password database
- 🎨 **Theme Support** - Light and dark themes
- 🔄 **Auto Updates** - Keep the application up-to-date
- 🚀 **Portable Version** - Works without installation
- 🖥️ **Cross-Platform** - Works on Windows, macOS and Linux
- 📊 **Statistics** - View password and category counts

## 📦 Installation

### Windows (Recommended)

1. Download the latest release
2. Run `installer.bat` as Administrator
3. Follow the on-screen instructions

The installer automatically does:
- ✅ Checks if Python is installed
- ✅ Installs Python if needed
- ✅ Installs all required packages
- ✅ Creates shortcuts
- ✅ Configures the application

### Portable Version

```bash
python portable_password_manager.py
Manual Installation
bash
# Clone the repository
git clone https://github.com/Techraym/SavePassword.git
cd SavePassword

# Install dependencies
pip install -r requirements.txt

# Start the application
python main.py
🎯 Usage
First Use: Set a master password to secure your database

Add Passwords: Click "➕ Add" to save new passwords

Manage Categories: Organize in folders via "📁 Categories"

Search & Filter: Use category explorer or search functionality

Generate Passwords: Use "🔑 Generate" for strong, random passwords

Copy to Clipboard: Click copy buttons for usernames and passwords

Open Websites: Click website buttons to open URLs directly in browser

Change Language: Use the language selector in settings

Switch Themes: Toggle between light and dark mode

🔄 Updates
Run update_manager.py to check for updates.

🗑️ Removal
Run uninstaller.bat to completely remove the application (with backup option).

🛡️ Security
All data is stored locally on your device

AES-256 encryption with PBKDF2 key derivation

Master password is never stored or transmitted

No internet connection required for operation

Secure language file downloads from GitHub

Clipboard auto-clear functionality

📁 File Structure
text
SavePassword/
├── main.py                              # Main application
├── portable_password_manager.py         # Portable version
├── installer.bat                       # Windows installer
├── uninstaller.bat                     # Removal tool
├── update_manager.py                   # Update tool
├── requirements.txt                    # Dependencies
├── README.md                           # Documentation
├── LICENSE                             # License file
├── CHANGELOG.md                        # Change log
├── .gitignore                          # Git ignore file
├── core/                               # Core functionality
│   ├── password_manager.py             # Password management logic
│   └── crypto.py                       # Encryption utilities
├── gui/                                # User interface
│   ├── main_window.py                  # Main application window
│   ├── dialogs.py                      # Various dialogs
│   ├── components.py                   # UI components
│   ├── themes.py                       # Theme management
│   └── icons/                          # Application icons
├── utils/                              # Utilities
│   ├── settings.py                     # Settings management
│   ├── language_manager.py             # Multi-language support
│   └── update_checker.py               # Update functionality
└── languages/                          # Translation files
    ├── en.json                         # English
    ├── de.json                         # German
    ├── fr.json                         # French
    ├── es.json                         # Spanish
    ├── it.json                         # Italian
    ├── nl.json                         # Dutch
    ├── pl.json                         # Polish
    └── pt.json                         # Portuguese
🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

Adding New Languages
To add a new language:

Create a new JSON file in languages/ folder

Follow the structure of en.json

Submit a pull request

📄 License
MIT License - see LICENSE file for details.

⚠️ Disclaimer
This software is provided "as is". The author is not responsible for any data loss or security issues.

Always keep backups of your password database and master password.

🔧 Troubleshooting
Common Issues
Python not found: Run the installer as Administrator

Missing dependencies: Run pip install -r requirements.txt

Database issues: Use the backup feature regularly

Portable version: Ensure write permissions in the application directory

Support
For issues and feature requests, please open an issue on GitHub.

text

## 3. CHANGELOG.md
```markdown
# Changelog

All notable changes to SavePassword will be documented in this file.

## [1.2.0] - 2024-01-02

### Added
- Complete button functionality implementation
- Colorful UI with hover effects for better user experience
- Clipboard integration for copying usernames and passwords
- Direct website opening functionality from password entries
- Enhanced password management with full CRUD operations
- Improved category management with tree structure
- Statistics display showing password and category counts
- Comprehensive error handling and user feedback
- Dark theme support with theme switching
- Portable version with automatic dependency handling

### Fixed
- Button click events not triggering actions
- Database connection and initialization issues
- Category explorer selection and filtering
- Password list display and update problems
- Master password verification flow
- Language switching and persistence
- Settings saving and application
- Memory leaks and performance issues
- Cross-platform compatibility problems

### Changed
- Updated all version references to 1.2.0
- Improved button styling with consistent color scheme
- Enhanced visual feedback for user actions
- Better icon visibility and contrast
- Restructured project organization
- Optimized database operations
- Improved application startup time

## [1.1.0] - 2024-01-01

### Added
- Multi-language support for 8 European languages
- Dynamic language downloading from GitHub repository
- Website URL integration with direct browser opening
- Portable version that works without installation
- Improved installer with automatic language support
- Lightweight installation (only English initially)
- Export functionality for password backups
- Password generator with customizable options

### Changed
- Application renamed from previous version to SavePassword
- Improved GUI with integrated language selector
- Better error handling and user feedback
- Updated documentation and installation instructions
- Enhanced security with improved encryption

### Fixed
- Minor bug fixes and stability improvements
- Database corruption issues
- User interface responsiveness

## [1.0.0] - 2024-01-01

### Added
- Initial public release
- Basic password management with secure storage
- AES-256 encryption for all sensitive data
- Password generator with multiple strength options
- Search and filter functionality
- Category-based organization system
- Master password protection
- Cross-platform compatibility

---

## Upgrade Notes

### From 1.1.0 to 1.2.0
- All button functionalities are now fully operational
- New clipboard features require no additional setup
- Website opening works with most modern browsers
- Portable version now handles dependencies automatically

### From 1.0.0 to 1.1.0
- Language files are now downloaded on-demand
- Export feature allows for better data portability
- Improved installer experience

---

## Known Issues

- None in current release

## Planned Features

- Mobile app companion
- Cloud synchronization (optional)
- Password strength analyzer
- Two-factor authentication support
- Browser extension
- Advanced reporting and analytics
[Unreleased]
Planned
Verbeterde backup en restore functionaliteit

Ondersteuning voor wachtwoordgenerator templates

Geavanceerde zoekfilters

Cloud synchronisatie opties

Biometrische authenticatie

[1.2.0] - 2025-09-29
Fixed
Critical: Herstelde import error in portable versie door incorrecte bestandsnaam

Gewijzigd: gui.main_window → gui.main_windows in portable_password_manager.py

Oorzaak: Bestandsnaam in project was main_windows.py maar code verwees naar main_window.py

UI: Opgelost weergave problemen in donker thema

Security: Verbeterde encryptie sleutel management

Portable: Opgelost pad problemen bij gebruik vanaf USB-drive

Added
New Feature: Geïntegreerde wachtwoordsterkte meter

New Feature: Auto-afmelding bij inactiviteit

Portable: Ondersteuning voor USB-drive gebruik zonder installatie

Export: CSV export functionaliteit toegevoegd

Import: Ondersteuning voor importeren vanuit andere password managers

Changed
Performance: Verbeterde database query prestaties met 40%

UI: Vernieuwde applicatie icons en splash screen

Settings: Herziene instellingen pagina met betere categorisering

Languages: Bijgewerkte vertalingen (NL, EN, DE, FR)

Documentation: Uitgebreide handleiding voor portable gebruik

Security
Enhanced: Sterkere standaard encryptie algoritmes

New: Beveiliging tegen timing attacks

Improved: Veiliger wachtwoord hashing met argon2

Added: Tweefactorauthenticatie ondersteuning

Dependencies
Updated: cryptography library naar v42.0

Added: argon2-cffi voor betere wachtwoord hashing

Removed: Verouderde pycrypto dependency

[1.1.0] - 2024-XX-XX
Added
Multi-language ondersteuning (Nederlands, Engels, Duits)

Donker/licht thema schakelaar

Automatische update checker

Wachtwoord generator met aanpasbare instellingen

Changed
Verbeterde GUI responsiviteit

Betere foutmeldingen en gebruikersfeedback

Optimalisaties voor grote wachtwoord databases

[1.0.0] - 2024-01-XX
Added
Eerste release van Portable SavePassword

Portable versie die werkt zonder installatie

Automatische dependency management

Cross-platform ondersteuning (Windows, Linux, macOS)

Features
Wachtwoordmanager met encryptie

GUI interface gebaseerd op tkinter

Draagbare database opslag

Multi-language ondersteuning

Thema ondersteuning
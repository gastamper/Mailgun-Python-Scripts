# mailgun.py
Python scripts for pulling bounces and complaints from Mailgun via API

# Installation & Configuration
Scripts assume Linux with Python3 being used.  Changes must be made to the 'Configuration' section of each script to reflect your individual Mailgun account, API key, and desired output file.

# Features
- Pulls the last 30 days worth of bounces/complaints from Mailgun via API
- For complaints, sorts (badly) based upon date prior to export.

# Future ideas
Error checking, fix terrible iteration in complaints' date sorting, option to delete pulled records.


```
# Requirements for Digital Library Application

# Core Python Libraries
tkinter
bson
datetime

# Database Libraries
pymongo==4.6.1
python-dotenv==1.0.0

# Optional but recommended
typing
```

Installation Instructions:
1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install requirements
```bash
pip install -r requirements.txt
```

3. Ensure MongoDB is installed and running locally
```bash
# For Ubuntu/Debian
sudo systemctl start mongod

# For macOS (with Homebrew)
brew services start mongodb-community

# For Windows
# Start MongoDB from Services or Command Prompt
```
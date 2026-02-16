# Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Windows Users

1. **Double-click `start.bat`** - This will:
   - Create virtual environment
   - Install all dependencies
   - Create .env file
   - Check MongoDB connection
   - Start the application

2. **Add your OpenAI API Key**:
   - Open `.env` file
   - Replace `your_openai_api_key_here` with your actual API key
   - Save the file

3. **Start MongoDB** (if not running):
   ```bash
   mongod
   ```

4. **Open browser**: http://localhost:8000

### Linux/Mac Users

1. **Run the start script**:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

2. **Follow the same steps as Windows** for API key and MongoDB

## 📝 Manual Setup

If you prefer manual setup:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 5. Edit .env and add your OpenAI API key

# 6. Start MongoDB
mongod

# 7. Run the application
python app/main.py
```

## ✅ Verify Installation

1. Open http://localhost:8000 - You should see the home page
2. Go to Upload page and upload a PDF
3. Go to Chat page and ask a question

## 🆘 Common Issues

### "MongoDB connection error"
- Make sure MongoDB is running: `mongod`
- Or update `MONGO_URI` in `.env` to point to MongoDB Atlas

### "OpenAI API error"
- Check your API key in `.env` file
- Verify your OpenAI account has credits

### "Port 8000 already in use"
- Change the port in `app/main.py` (line 51)
- Or stop the process using port 8000

## 🎉 You're Ready!

Upload a PDF document and start asking questions!

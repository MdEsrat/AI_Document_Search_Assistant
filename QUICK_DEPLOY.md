# 🚀 QUICK START: Deploy Your App in 5 Minutes

## Your app is on GitHub but not live yet. Here's how to make it a running web app:

## Option 1: Hugging Face Spaces (EASIEST - FREE)

### Step 1: Create HF Space
1. Go to https://huggingface.co/new-space
2. **Space name**: `ai-document-search`
3. **SDK**: Select **Docker** ⚠️ IMPORTANT
4. **Visibility**: Public (free)
5. Click **Create Space**

### Step 2: Connect Your GitHub
1. In your new Space, go to **Settings** tab
2. Scroll to **Linked repositories**
3. Click **Connect to GitHub**
4. Authorize Hugging Face
5. Select repository: `MdEsrat/AI_Document_Search_Assistant`
6. Select branch: `main`
7. Click **Connect**

### Step 3: Wait for Build
- HF will automatically build your Docker container
- Watch in **Logs** tab (takes 5-10 minutes)
- Once done, your app will be LIVE! 🎉

### Step 4: Access Your App
Your live URL: `https://huggingface.co/spaces/YOUR_USERNAME/ai-document-search`

---

## Option 2: Render (FREE - Good Alternative)

1. Go to https://render.com
2. Sign up (free)
3. Click **New +** → **Web Service**
4. Connect your GitHub repository
5. Settings:
   - **Environment**: Docker
   - **Plan**: Free
6. Click **Deploy**
7. Wait 5-10 minutes
8. You'll get a URL like: `https://your-app.onrender.com`

---

## Option 3: Railway (FREE $5/month credit)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select `AI_Document_Search_Assistant`
5. Railway auto-detects Dockerfile
6. Click **Deploy**
7. Get your live URL

---

## Option 4: Local Deployment (For Testing)

If you just want to run it locally to test:

```bash
# Using Docker
docker build -t doc-search .
docker run -p 7860:7860 doc-search

# Visit: http://localhost:7860
```

---

## 🎯 RECOMMENDED: Hugging Face Spaces

✅ **Why?**
- Free forever
- Easy GitHub integration
- Auto-deploys on every commit
- Great for AI/ML apps
- We already prepared all files!

✅ **What's Ready:**
- Dockerfile ✓
- Port 7860 configured ✓
- All dependencies ✓
- Full deployment guide ✓

---

## ⚡ Quick Deploy to HF (Command Line Method)

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Create space
huggingface-cli repo create ai-document-search --type space --space_sdk docker

# Add remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/ai-document-search

# Push
git push hf main
```

---

## 🔑 Add Secrets (Optional)

If using OpenAI:
1. Go to Space Settings
2. Add secret: `OPENAI_API_KEY` = your_new_key
3. Restart the Space

---

## 🆘 Need Help?

See detailed guide: [DEPLOYMENT_HF.md](DEPLOYMENT_HF.md)

---

## After Deployment:

Your app will have a public URL like:
- HF: `https://huggingface.co/spaces/MdEsrat/ai-document-search`
- Render: `https://ai-doc-search.onrender.com`
- Railway: `https://ai-doc-search.railway.app`

Anyone can access it! 🌍

# 🚀 Hugging Face Spaces Deployment Guide

This guide will help you deploy your AI Document Search Assistant to Hugging Face Spaces.

## 📋 Prerequisites

- Hugging Face account (https://huggingface.co/join)
- Git installed locally (optional, for GitHub integration)

## 🎯 Deployment Options

### Option 1: Direct Upload (Easiest)
Best for quick deployment without GitHub setup.

### Option 2: GitHub Integration (Recommended)
Best for continuous deployment and version control.

---

## 🚀 Option 1: Direct Upload to Hugging Face

### Step 1: Create a New Space

1. Go to https://huggingface.co/new-space
2. Fill in the details:
   - **Space name**: `document-search-assistant` (or your preferred name)
   - **License**: MIT
   - **SDK**: Select **Docker**
   - **Space hardware**: CPU basic (free tier works fine)
   - **Visibility**: Public or Private

3. Click **Create Space**

### Step 2: Prepare Your Files

Make sure you have these key files in your project:
- ✅ `Dockerfile` (already created)
- ✅ `requirements.txt` (already exists)
- ✅ `README_HF.md` (rename to `README.md` for HF)
- ✅ All `app/` and `frontend/` folders
- ✅ `data/` folder structure

### Step 3: Upload Files

1. In your new Space, click **Files** tab
2. Click **Add file** → **Upload files**
3. Upload all project files except:
   - `.env` (don't upload secrets!)
   - `__pycache__/` folders
   - `.pyc` files
   - Local database files in `data/`

### Step 4: Rename README

1. Delete the default `README.md` in your Space
2. Rename `README_HF.md` to `README.md` 
3. Edit the README metadata at the top:
   ```yaml
   ---
   title: AI Document Search Assistant
   emoji: 📚
   colorFrom: blue
   colorTo: purple
   sdk: docker
   pinned: false
   license: mit
   ---
   ```

### Step 5: Configure Secrets (Optional)

Only needed if using OpenAI models:

1. Go to **Settings** tab in your Space
2. Scroll to **Repository secrets**
3. Click **New secret**
4. Add:
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
5. Click **Save**

### Step 6: Deploy

1. Hugging Face will automatically build your Docker container
2. Watch the **Logs** tab for build progress
3. Build takes 5-10 minutes typically
4. Once complete, your app will be live! 🎉

### Step 7: Test Your Deployment

1. Visit your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
2. Upload a PDF document
3. Ask questions about it
4. Verify the chat functionality works

---

## 🔄 Option 2: GitHub Integration (Recommended)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit for HF deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/document-search-assistant.git

# Push
git push -u origin main
```

### Step 2: Create Space with GitHub

1. Go to https://huggingface.co/new-space
2. Fill in details and select **Docker** SDK
3. After creating the Space, go to **Settings** tab
4. Under **Linked repositories**, click **Connect to GitHub**
5. Authorize Hugging Face to access your GitHub
6. Select your repository
7. Choose the branch (usually `main`)

### Step 3: Configure Auto-Deployment

1. Every push to your GitHub repository will trigger a rebuild
2. Add secrets in **Settings** → **Repository secrets** (if needed)
3. Your Space will automatically update on every commit

### Step 4: Update README

In your GitHub repo, rename `README_HF.md` to `README.md` or update the existing README with Hugging Face metadata at the top.

---

## 🔧 Configuration Tips

### Using Local Models (Free)

By default, the app uses free local models:
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **LLM**: You'll need to configure a local LLM or use OpenAI

Set in Dockerfile or as environment variable:
```dockerfile
ENV USE_LOCAL_MODELS=True
```

### Using OpenAI Models

If you have an OpenAI API key:
```dockerfile
ENV USE_LOCAL_MODELS=False
```

Then add `OPENAI_API_KEY` as a Space secret.

### Storage Considerations

Hugging Face Spaces provide:
- **Persistent storage**: Limited to Space storage quota
- **Temporary storage**: Resets on rebuild

To persist uploads and vector store:
- Files in `data/uploads/` and `data/chroma/` persist between restarts
- But may be lost on rebuilds
- Consider adding backup mechanisms for production use

### MongoDB Alternative

Since MongoDB isn't available on HF Spaces, the app gracefully falls back:
- Vector store (ChromaDB) still works
- Chat history works in-memory
- For production, consider:
  - External MongoDB Atlas (free tier available)
  - SQLite for local storage
  - Update `MONGO_URI` in secrets

---

## 🐛 Troubleshooting

### Build Fails

**Check logs** in the **Logs** tab:

1. **Missing dependencies**: Verify `requirements.txt` is complete
2. **Port issues**: HF Spaces require port 7860 (already configured in Dockerfile)
3. **Memory issues**: Upgrade to a larger Space hardware

### App Not Loading

1. Check if build completed successfully
2. Verify port 7860 is exposed in Dockerfile
3. Check logs for runtime errors

### MongoDB Errors

The app is designed to work without MongoDB:
- Vector search still works (uses ChromaDB)
- Chat history may be in-memory only
- To fix: Add external MongoDB URI as secret

### Slow Response

1. **Use local models**: Faster than API calls
2. **Upgrade hardware**: CPU basic → CPU/GPU upgrade
3. **Optimize chunk size**: Reduce `CHUNK_SIZE` in config

### Upload Issues

1. Check file size limits (HF has limits)
2. Verify `data/uploads/` directory exists and is writable
3. Check disk space quota

---

## 📊 Monitoring Your Space

### View Metrics

- **Settings** → **Analytics**: See usage stats
- **Logs** tab: Real-time application logs
- **Community** tab: User feedback and issues

### Updating Your Space

**Direct Upload Method:**
1. Upload new/modified files via web interface
2. Space rebuilds automatically

**GitHub Integration Method:**
1. Push changes to GitHub
2. HF automatically pulls and rebuilds
3. Monitor deployment in **Logs** tab

---

## 🎨 Customization

### Change Theme

Edit the README.md metadata:
```yaml
---
emoji: 🤖  # Change emoji
colorFrom: red  # Change color scheme
colorTo: yellow
---
```

### Add Demo Content

Pre-populate with sample PDFs:
1. Add PDFs to `data/uploads/` before deployment
2. Run a script to index them on startup

### Custom Domain

1. Upgrade to Hugging Face Pro
2. Configure custom domain in Settings

---

## 💡 Best Practices

1. **Use `.gitignore`**: Don't commit `.env`, `__pycache__`, local DBs
2. **Monitor costs**: If using OpenAI, monitor API usage
3. **Rate limiting**: Consider adding rate limits for public Spaces
4. **Error handling**: The app already has good error handling
5. **Logs**: Use logs to debug issues
6. **Secrets**: Always use Secrets for API keys, never hardcode
7. **Testing**: Test locally with Docker before deploying:
   ```bash
   docker build -t doc-search .
   docker run -p 7860:7860 doc-search
   ```

---

## 📚 Additional Resources

- [HF Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Docker Spaces Guide](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)

---

## ✅ Deployment Checklist

- [ ] Create Hugging Face account
- [ ] Create new Space with Docker SDK
- [ ] Upload/connect all project files
- [ ] Rename README_HF.md to README.md
- [ ] Add metadata to README
- [ ] Configure secrets (if using OpenAI)
- [ ] Wait for build to complete
- [ ] Test document upload
- [ ] Test chat functionality
- [ ] Monitor logs for errors
- [ ] Share your Space! 🎉

---

## 🎉 Success!

Once deployed, share your Space:
- URL: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
- Embed widget available in Space settings
- Share on social media with #HuggingFace #RAG

Need help? Open an issue or check HF community forums!

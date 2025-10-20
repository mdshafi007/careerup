# 🚀 CareerUp Deployment Guide

## **Architecture**
- **Frontend**: Vercel (React)
- **Backend**: Railway (Flask + LangChain)
- **APIs**: Gemini AI, Adzuna

---

## **PART 1: Deploy Backend to Railway** 🚂

### **Step 1: Push to GitHub**
```bash
cd c:\Users\skmds\OneDrive\Desktop\careerup
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### **Step 2: Create Railway Account**
1. Go to https://railway.app
2. Sign up with GitHub
3. Verify your email

### **Step 3: Deploy Backend**
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `mdshafi007/careerup`
4. Railway will auto-detect it's a Python app
5. Click **"Add variables"** and add:
   ```
   GEMINI_API_KEY=AIzaSyA8dSFPIhCKj9S17pVhtAoQ6Tk6sjG3RFM
   ADZUNA_APP_ID=64dc4e8c
   ADZUNA_APP_KEY=baa7f34a425567cf3b07dcd4f7794b4c
   JSEARCH_API_KEY=2c3d611c5cmsh6cf91b87ec1d26fp1abOb7jsn64a79d6e6df1
   ```

### **Step 4: Configure Build**
Railway should auto-detect:
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Root Directory**: `backend`

If not, set manually in **Settings → Build**

### **Step 5: Get Your Railway URL**
1. Go to **Settings → Networking**
2. Click **"Generate Domain"**
3. Copy the URL: `https://careerup-production-xxxx.up.railway.app`
4. **Save this URL!** You'll need it for Vercel

### **Step 6: Test Backend**
Visit: `https://your-railway-url.railway.app/api/health`

Should return:
```json
{
  "status": "healthy",
  "service": "CareerUp Backend",
  "gemini_configured": true,
  "adzuna_configured": true
}
```

✅ **Backend is live!**

---

## **PART 2: Deploy Frontend to Vercel** ⚡

### **Step 1: Create Vercel Account**
1. Go to https://vercel.com
2. Sign up with GitHub
3. Authorize Vercel to access your repos

### **Step 2: Deploy Frontend**
1. Click **"Add New Project"**
2. Import your repository: `mdshafi007/careerup`
3. Vercel will auto-detect React

### **Step 3: Configure Project**
- **Framework Preset**: Create React App
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `build` (auto-detected)

### **Step 4: Add Environment Variable**
In **Environment Variables** section, add:
```
REACT_APP_API_URL=https://your-railway-url.railway.app
```
**Replace with your actual Railway URL from Part 1, Step 5!**

### **Step 5: Deploy**
1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. Get your Vercel URL: `https://careerup.vercel.app`

### **Step 6: Test Frontend**
1. Visit your Vercel URL
2. Upload a test resume PDF
3. Check if it works end-to-end

✅ **Frontend is live!**

---

## **PART 3: Connect Frontend & Backend** 🔗

### **Update Backend CORS**
1. Go to Railway dashboard
2. Open your backend project
3. Go to **Variables**
4. Add your Vercel URL to allowed origins (already configured in code)

The code already allows:
```python
"https://*.vercel.app"
```

### **Update Frontend API URL (if needed)**
If you need to change the backend URL later:
1. Go to Vercel dashboard
2. Your project → **Settings → Environment Variables**
3. Edit `REACT_APP_API_URL`
4. **Redeploy** to apply changes

---

## **PART 4: Post-Deployment Checklist** ✅

### **Test Everything:**
- [ ] Backend health endpoint works
- [ ] Frontend loads correctly
- [ ] File upload works
- [ ] PDF text extraction works
- [ ] AI analysis returns results
- [ ] Jobs are fetched from Adzuna
- [ ] Apply links work
- [ ] Mobile responsive

### **Common Issues & Fixes:**

#### **Issue 1: CORS Error**
**Fix**: Check Railway environment variables include all domains

#### **Issue 2: 500 Error on Backend**
**Fix**: Check Railway logs:
```
Railway Dashboard → Your Project → Deployments → View Logs
```

#### **Issue 3: Frontend Can't Connect**
**Fix**: Verify `REACT_APP_API_URL` in Vercel env variables

#### **Issue 4: API Keys Not Working**
**Fix**: Re-add environment variables in Railway, redeploy

---

## **PART 5: Custom Domain (Optional)** 🌐

### **Vercel Custom Domain:**
1. Buy domain (Namecheap, GoDaddy, etc.)
2. Vercel Dashboard → Your Project → **Settings → Domains**
3. Add your domain: `careerup.com`
4. Update DNS records (Vercel will guide you)

### **Railway Custom Domain:**
1. Railway Dashboard → Your Project → **Settings → Networking**
2. Add custom domain: `api.careerup.com`
3. Update DNS CNAME record

---

## **Monitoring & Maintenance** 📊

### **Railway Dashboard:**
- Monitor usage: $5 credit/month
- Check logs for errors
- View metrics (CPU, RAM, requests)

### **Vercel Dashboard:**
- View analytics
- Monitor build times
- Check bandwidth usage

---

## **Estimated Costs** 💰

| Service | Free Tier | Notes |
|---------|-----------|-------|
| **Railway** | $5 credit/month | Should last all month for your usage |
| **Vercel** | Unlimited | Free for hobby projects |
| **Gemini AI** | Generous free tier | ~60 requests/minute free |
| **Adzuna API** | 100 requests/month | Should be enough |

**Total: FREE** (Railway credit covers backend hosting)

---

## **Quick Deploy Commands** ⚡

```bash
# Push code to GitHub
git add .
git commit -m "Update deployment"
git push origin main

# Railway auto-deploys on push
# Vercel auto-deploys on push

# Manual redeploy (if needed):
# Railway: Dashboard → Redeploy
# Vercel: Dashboard → Redeploy
```

---

## **Your Deployment URLs** 📍

**Frontend (Vercel):**
```
https://careerup.vercel.app
```

**Backend (Railway):**
```
https://careerup-production-xxxx.up.railway.app
```

**Health Check:**
```
https://your-railway-url.railway.app/api/health
```

---

## **Support** 💬

### **Railway Issues:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

### **Vercel Issues:**
- Docs: https://vercel.com/docs
- Support: support@vercel.com

---

**🎉 Congratulations! Your CareerUp app is now live!**

Share it with friends, add to your portfolio, and put it on your resume! 🚀

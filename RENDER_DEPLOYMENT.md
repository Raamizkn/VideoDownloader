# Deploying to Render

Render is perfect for this video downloader application because it supports:
- ✅ Long-running processes (no execution time limits)
- ✅ Persistent disk storage for downloads
- ✅ Background threading support
- ✅ Free tier available

## Quick Deploy

### Option 1: Deploy via Render Dashboard (Recommended)

1. **Create a Render Account**
   - Go to [render.com](https://render.com)
   - Sign up for a free account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository (or use the public repo option)

3. **Configure the Service**
   - **Name**: `youtube-downloader` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or choose a paid plan for more resources)

4. **Add Persistent Disk (Optional but Recommended)**
   - Go to your service settings
   - Click "Disks" → "Connect New Disk"
   - **Name**: `downloads-disk`
   - **Mount Path**: `/opt/render/project/src/downloads`
   - **Size**: 1 GB (or more if needed)
   - This ensures downloads persist across deployments

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - Your app will be available at `https://your-app-name.onrender.com`

### Option 2: Deploy via render.yaml (Infrastructure as Code)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Import render.yaml in Render Dashboard**
   - Go to Render Dashboard
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and create the service

## Environment Variables

No environment variables are required for basic operation. The app will:
- Use the `downloads/` folder for storing videos
- Automatically detect the PORT from Render's environment

## Important Notes

### Free Tier Limitations
- **Spins down after 15 minutes of inactivity** - First request after spin-down takes ~30 seconds
- **512 MB RAM** - Should be sufficient for most downloads
- **Disk storage** - 1 GB free (enough for several videos)

### Upgrading to Paid Tier
- **No spin-down** - Always available
- **More RAM** - Better for large video downloads
- **More disk space** - Store more videos

### Download Storage
- Videos are stored in the `downloads/` folder
- If you added a persistent disk, they'll persist across deployments
- Without a disk, downloads are lost on each deployment

### Custom Domain
1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain and follow DNS setup instructions

## Monitoring

- **Logs**: View real-time logs in the Render dashboard
- **Metrics**: Monitor CPU, memory, and disk usage
- **Alerts**: Set up alerts for service issues

## Troubleshooting

### Build Fails
- Check that all dependencies are in `requirements.txt`
- Ensure Python version is compatible (3.11+)

### Downloads Not Working
- Check logs for yt-dlp errors
- Verify disk is mounted correctly
- Check available disk space

### Service Spins Down
- Free tier services spin down after 15 minutes
- First request after spin-down takes longer
- Upgrade to paid tier to avoid spin-down

## Updating Your App

1. Push changes to your GitHub repository
2. Render automatically detects changes and redeploys
3. Or manually trigger a deploy from the dashboard

## Cost

- **Free Tier**: $0/month (with limitations)
- **Starter Plan**: $7/month (no spin-down, more resources)
- **Professional Plan**: $25/month (even more resources)

Your app is now ready to download YouTube videos on Render! 🚀


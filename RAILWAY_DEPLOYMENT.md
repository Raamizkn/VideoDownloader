# Deploying to Railway

Railway is a great alternative to Render. It's often faster and has a very generous trial.

### Steps to Deploy:

1.  **Login to Railway**: Go to [railway.app](https://railway.app) and sign in with GitHub.
2.  **Create New Project**: Click **"New Project"** -> **"Deploy from GitHub repo"**.
3.  **Select Repository**: Choose your `VideoDownloader` repo.
4.  **Add Variables**: Railway will automatically detect your `Procfile`. You don't need to add a `PORT` variable manually; Railway handles it.
5.  **Deploy**: It will start building automatically.

### Why use Railway?
- **Fast Builds**: Typically faster than Render.
- **Auto-Detect**: It will use your existing `Procfile` and `requirements.txt`.
- **No Sleep**: Railway apps don't "sleep" on the free tier like Render ones do, so your first download will be instant.

**Note**: Just like Render's free tier, files saved to `./downloads` will be wiped when the app restarts. Always use the **"Download to Computer"** button to save your videos permanently.


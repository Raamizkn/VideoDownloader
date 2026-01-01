# Deploying to Vercel

## ⚠️ Important Limitations

**Vercel has significant limitations for video downloading:**

1. **Execution Time Limits:**
   - Free tier: 10 seconds max
   - Pro tier: 60 seconds max
   - Video downloads often take longer than this

2. **File Storage:**
   - Files are stored in `/tmp` which is ephemeral
   - Files are deleted when the function ends
   - No persistent storage available

3. **Memory Limits:**
   - Free tier: 1024 MB
   - Large video files may exceed this

4. **No Background Processing:**
   - Threading doesn't work in serverless functions
   - Downloads must complete within the request timeout

## Better Alternatives

For a video downloader, consider these platforms instead:

### 1. **Railway** (Recommended)
- No execution time limits
- Persistent storage
- Easy deployment
- Free tier available

### 2. **Render**
- Long-running processes supported
- Persistent storage
- Free tier available

### 3. **Fly.io**
- Good for Python apps
- Persistent volumes
- Generous free tier

### 4. **Heroku**
- Classic platform for Flask apps
- Add-ons for storage
- Paid plans required

## If You Still Want to Deploy to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel
```

4. For production:
```bash
vercel --prod
```

## Recommended Architecture Changes for Vercel

To make this work better on Vercel, you'd need to:

1. **Use a Queue System:**
   - Queue downloads to external service (Redis Queue, AWS SQS)
   - Process downloads on a separate worker

2. **Stream Downloads:**
   - Stream video directly to user's browser
   - Don't store files on server

3. **Use External Storage:**
   - Upload to S3, Cloudflare R2, or similar
   - Provide download links to users

4. **Client-Side Download:**
   - Use yt-dlp in browser (via WebAssembly)
   - Or use a service like yt-dlp API

## Current Setup

The current setup will work for very short videos (< 10 seconds), but will timeout for most real-world use cases.


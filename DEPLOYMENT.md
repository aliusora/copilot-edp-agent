# 🚀 Deployment Guide

This guide covers deploying the Microsoft Copilot Chat application to various platforms.

## 📋 Pre-Deployment Checklist

- [ ] OpenAI API key secured
- [ ] Dependencies tested locally
- [ ] Cache directory added to `.gitignore`
- [ ] No sensitive data in repository
- [ ] README.md updated
- [ ] Requirements.txt finalized

## 🌐 Deployment Options

### 1. Streamlit Community Cloud (Recommended)

**Best for**: Free hosting, easy setup, automatic deployments

#### Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Go to** [share.streamlit.io](https://share.streamlit.io)

3. **Deploy**:
   - Click "New app"
   - Select your GitHub repository
   - Set main file: `app.py`
   - Click "Deploy"

4. **Add Secrets**:
   - Go to app settings → Secrets
   - Add:
     ```toml
     OPENAI_API_KEY = "sk-your-api-key-here"
     ```

**Limitations**: Free tier has resource limits (1 GB RAM, shared CPU)

---

### 2. Heroku

**Best for**: Scalable hosting, custom domains

#### Steps:

1. **Create `Procfile`**:
   ```bash
   echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   ```

2. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variable**:
   ```bash
   heroku config:set OPENAI_API_KEY=sk-your-api-key-here
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **Open app**:
   ```bash
   heroku open
   ```

**Cost**: Starts at $7/month (Eco dynos)

---

### 3. AWS (EC2 or ECS)

**Best for**: Enterprise deployments, full control

#### EC2 Setup:

1. **Launch EC2 instance** (Ubuntu 22.04, t3.medium recommended)

2. **SSH into instance**:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   ```

4. **Clone repository**:
   ```bash
   git clone https://github.com/yourusername/copilot-edp-agent.git
   cd copilot-edp-agent
   ```

5. **Install Python packages**:
   ```bash
   pip3 install -r requirements.txt
   ```

6. **Set environment variable**:
   ```bash
   echo 'export OPENAI_API_KEY="sk-your-key"' >> ~/.bashrc
   source ~/.bashrc
   ```

7. **Run with systemd** (create `/etc/systemd/system/copilot-chat.service`):
   ```ini
   [Unit]
   Description=Microsoft Copilot Chat
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/copilot-edp-agent
   Environment="OPENAI_API_KEY=sk-your-key"
   ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

8. **Start service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable copilot-chat
   sudo systemctl start copilot-chat
   ```

9. **Configure Nginx** (create `/etc/nginx/sites-available/copilot-chat`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

10. **Enable and restart Nginx**:
    ```bash
    sudo ln -s /etc/nginx/sites-available/copilot-chat /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

**Cost**: ~$30-50/month (t3.medium)

---

### 4. Docker

**Best for**: Containerized deployments, cloud platforms

#### Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and run:

```bash
docker build -t copilot-chat .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-your-key copilot-chat
```

#### Deploy to Docker Hub:

```bash
docker tag copilot-chat yourusername/copilot-chat:latest
docker push yourusername/copilot-chat:latest
```

---

### 5. Azure App Service

**Best for**: Microsoft ecosystem integration

#### Steps:

1. **Create App Service**:
   ```bash
   az webapp up --name copilot-chat --runtime PYTHON:3.11
   ```

2. **Set environment variable**:
   ```bash
   az webapp config appsettings set --name copilot-chat \
     --settings OPENAI_API_KEY=sk-your-key
   ```

3. **Deploy**:
   ```bash
   git push azure main
   ```

**Cost**: Starts at ~$55/month (B1 tier)

---

## 🔐 Security Best Practices

### API Key Management

✅ **Do**:
- Use environment variables or secrets management
- Rotate keys regularly
- Use separate keys for dev/staging/prod
- Monitor API usage

❌ **Don't**:
- Commit API keys to Git
- Share keys in plain text
- Use production keys for testing
- Hardcode keys in application

### Additional Security

1. **Enable HTTPS** (use Let's Encrypt for free SSL)
2. **Set up authentication** (if needed for internal use)
3. **Rate limiting** (protect against abuse)
4. **Monitor logs** (track errors and usage)

---

## 📊 Monitoring & Maintenance

### Health Checks

Monitor these metrics:
- API response time
- Cache hit rate
- Error rate
- Memory usage
- API quota remaining

### Logs

Check logs for:
- Failed API calls
- Content extraction errors
- Cache issues
- User errors

### Updates

Regular maintenance:
- Update dependencies monthly
- Review and update UNC sources quarterly
- Monitor OpenAI API changes
- Test with new Streamlit releases

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: App won't start
- **Solution**: Check Python version (3.10+), verify API key

**Issue**: Slow responses
- **Solution**: Enable caching, increase cache TTL

**Issue**: Out of memory
- **Solution**: Reduce max tokens, limit concurrent users

**Issue**: API rate limit errors
- **Solution**: Implement request queuing, upgrade API plan

---

## 📞 Support

For deployment issues:
- Check Streamlit forums: [discuss.streamlit.io](https://discuss.streamlit.io)
- Review Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)
- Open GitHub issue for app-specific problems

---

**Last Updated**: October 2025

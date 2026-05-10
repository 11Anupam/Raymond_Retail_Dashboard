# Raymond Retail Intelligence - Deployment Guide

## 🚀 Quick Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)
- This repository pushed to GitHub

### Step-by-Step Deployment

#### 1. Push to GitHub
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Raymond Retail Intelligence Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/raymond-retail-intelligence.git
git push -u origin main
```

#### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app** button
3. Select:
   - GitHub repo: `your-username/raymond-retail-intelligence`
   - Branch: `main`
   - Main file path: `app.py`
4. Click **Deploy!**

The dashboard will be live at: `https://share.streamlit.io/your-username/raymond-retail-intelligence`

---

## 🐳 Deployment via Docker

### Build Docker Image
```bash
docker build -t raymond-retail:latest .
```

### Run Locally
```bash
docker run -p 8501:8501 raymond-retail:latest
```

### Push to Docker Hub
```bash
docker tag raymond-retail:latest your-username/raymond-retail:latest
docker push your-username/raymond-retail:latest
```

### Deploy to Cloud Platforms

**AWS ECS:**
```bash
aws ecs create-service \
  --cluster my-cluster \
  --service-name raymond-retail \
  --task-definition raymond-retail:1 \
  --desired-count 1
```

**Google Cloud Run:**
```bash
gcloud run deploy raymond-retail \
  --source . \
  --platform managed \
  --region us-central1
```

**Azure Container Instances:**
```bash
az container create \
  --resource-group myResourceGroup \
  --name raymond-retail \
  --image your-username/raymond-retail:latest \
  --ports 8501 \
  --cpu 1 --memory 1
```

---

## 📦 Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] `.gitignore` configured properly
- [ ] Code tested locally with `streamlit run app.py`
- [ ] No hardcoded secrets or API keys
- [ ] `README.md` updated with deployment info
- [ ] `.streamlit/config.toml` configured
- [ ] Git repository initialized and pushed to GitHub

---

## ⚙️ Environment Variables (Optional)

Create `.streamlit/secrets.toml` for sensitive data:
```toml
[database]
host = "localhost"
port = 5432

[api]
key = "your-api-key"
```

---

## 🔍 Post-Deployment Testing

After deployment, verify:

1. **Access Dashboard**: Open the deployed URL
2. **Load Data**: Check if synthetic data loads without errors
3. **Interactive Charts**: Try clicking/hovering on charts
4. **Filters**: Test store, category, and date filters
5. **Exports**: Download a report (CSV/TXT)
6. **Performance**: Check page load time (should be < 3 seconds)

---

## 🚨 Troubleshooting Deployment

### Issue: "ModuleNotFoundError"
- **Solution**: Ensure all imports are in `requirements.txt`
- **Check**: `pip freeze > requirements.txt`

### Issue: "Memory Limit Exceeded"
- **Solution**: Reduce synthetic data size in `data_generator.py`
- **Change**: `days=180, num_transactions=2000` instead of 365/5000

### Issue: "Dashboard Loads Slowly"
- **Solution**: Enable caching
- **Already done**: `@st.cache_data` decorators in place
- **Last resort**: Deploy on a higher-tier Streamlit Cloud instance

### Issue: "Charts Not Rendering"
- **Solution**: Clear cache and hard refresh
- **Command**: `streamlit cache clear` then reload browser

---

## 📊 Production Best Practices

### 1. **Monitoring**
- Set up alerting for errors
- Monitor app performance and load times
- Track user analytics

### 2. **Data Management**
- Consider connecting to real database instead of synthetic data
- Implement automatic data refresh (e.g., daily)
- Archive old reports

### 3. **Security**
- Use environment variables for API keys
- Enable HTTPS (automatic on Streamlit Cloud)
- Restrict access with authentication if needed

### 4. **Scaling**
- Monitor user growth
- Consider upgrade if slow performance
- Cache expensive computations

---

## 🔄 Continuous Deployment with GitHub Actions

Create `.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Test imports
        run: python -c "import streamlit; import app"
```

---

## 📈 Scaling to Production

### With Real Database
Replace synthetic data in `app.py`:
```python
import psycopg2
conn = psycopg2.connect("postgresql://user:password@localhost/retail")
sales_df = pd.read_sql("SELECT * FROM sales", conn)
```

### With API Integration
Connect to your retail system:
```python
import requests
response = requests.get("https://api.yourretail.com/sales")
sales_df = pd.DataFrame(response.json())
```

### With Cloud Storage
Use S3, Google Cloud Storage, or Azure Blob:
```python
import s3fs
df = pd.read_csv("s3://my-bucket/sales.csv")
```

---

## 💰 Cost Estimates

| Platform | Monthly Cost | Notes |
|----------|--------------|-------|
| **Streamlit Cloud** | $0-70 | Free tier available |
| **AWS ECS** | $20-200 | Depends on compute |
| **Google Cloud Run** | $0-50 | Pay per request |
| **Azure Container** | $30-150 | Always on |
| **Heroku** | $7-50 | Simple deployment |

---

## 🎓 Further Learning

- [Streamlit Cloud Deployment](https://docs.streamlit.io/streamlit-cloud/get-started)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions Guide](https://docs.github.com/en/actions)

---

**Your dashboard is now live and ready to drive retail insights!** 🎉

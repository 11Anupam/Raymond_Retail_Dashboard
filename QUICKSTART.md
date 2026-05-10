# ⚡ Quick Start - 5 Minutes to Dashboard

## 1️⃣ Clone & Install (1 min)
```bash
git clone https://github.com/yourusername/raymond-retail-intelligence.git
cd raymond-retail-intelligence
pip install -r requirements.txt
```

## 2️⃣ Run Dashboard (30 seconds)
```bash
streamlit run app.py
```

## 3️⃣ Open Browser (10 seconds)
Visit: **http://localhost:8501**

---

## 📊 Explore These Pages

### 🎯 Overview
- 5 KPI cards with live metrics
- Sales trend chart
- Top performers
- AI-generated insights

### 📈 Sales Analytics  
- Store comparison matrix
- Seasonal demand patterns
- Campaign ROI analysis

### 📦 Inventory Management
- Current stock levels
- Inventory turnover by store
- Critical alerts

### 👥 Customer Insights
- Customer segmentation (3D view)
- Purchase behavior analysis
- Lifetime value segments

### 🔮 Forecasting
- 30-day sales forecast
- Seasonal components
- Trend analysis

### 📋 Reports
- Download executive summary
- Export detailed analytics
- Download raw data

---

## 🎛️ Using Filters

**Left Sidebar:**
- 📅 Date Range: Select start and end dates
- 🏪 Stores: Pick one or multiple stores
- 🏷️ Categories: Choose product categories

Changes apply instantly to all charts!

---

## 📥 Export Your Data

1. Go to **Reports** tab
2. Choose **Data Export**
3. Select datasets
4. Download as CSV

---

## 🚀 Deploy to Cloud (2 minutes)

### Option A: Streamlit Cloud (Easiest)
1. Push to GitHub: `git push origin main`
2. Go to share.streamlit.io
3. Click "New app" → select your repo
4. Click "Deploy"
5. Share live link!

### Option B: Docker
```bash
docker build -t raymond-retail .
docker run -p 8501:8501 raymond-retail
```

### Option C: Heroku
```bash
heroku create your-app-name
git push heroku main
```

---

## 🎨 What You Get

✅ Professional dashboard with luxury aesthetic  
✅ Real-time KPI tracking  
✅ Interactive charts with hover/zoom  
✅ AI-powered business insights  
✅ Inventory alerts & recommendations  
✅ Customer segmentation analysis  
✅ 30-day sales forecasting  
✅ CSV/TXT report downloads  
✅ Fully synthetic data (ready for production)  
✅ Deployment-ready structure  

---

## 📚 Full Documentation

See **README.md** for:
- Detailed feature descriptions
- Deployment guides
- Architecture overview
- Troubleshooting

See **DEPLOYMENT.md** for:
- Cloud deployment steps
- Docker instructions
- CI/CD setup

---

## ❓ Common Questions

**Q: Is this real data?**  
A: No, it's realistic synthetic data generated on startup. Easy to swap with real data from your DB.

**Q: Can I customize colors/styling?**  
A: Yes! Edit the CSS in `app.py` or modify `color_palette` in `utils.py`.

**Q: How do I connect real data?**  
A: Replace the `load_data()` function in `app.py` with your database connection.

**Q: What are system requirements?**  
A: Python 3.8+, ~200MB RAM, no database needed (synthetic data included).

---

**Ready? Run `streamlit run app.py` and explore!** 🎉

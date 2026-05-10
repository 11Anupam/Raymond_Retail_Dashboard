# 📊 Data Dictionary - Raymond Retail Intelligence

## Sales Data (sales_df)

### Core Columns

| Column | Type | Description | Example | Range |
|--------|------|-------------|---------|-------|
| **date** | Date | Transaction date | 2023-01-15 | 365 days |
| **store_name** | String | Store identifier | "Store A" | 15 stores |
| **category** | String | Product category | "Menswear" | 5 categories |
| **sales** | Float | Revenue from transaction | 145.50 | $0 - $2000 |
| **profit** | Float | Net profit | 58.20 | 30-50% margin |
| **quantity** | Int | Units sold | 3 | 1-8 units |
| **price** | Float | Unit price | $48.50 | Category dependent |
| **stock** | Int | Current inventory | 85 | 5-200 units |
| **footfall** | Int | Store visitors that day | 47 | 10-100 visitors |
| **promotion_type** | String | Active promotion | "Discount" | 5 types |
| **cost** | Float | Cost of goods sold | 87.30 | Calculated |

---

## Categories

```
1. Menswear
   - Price Range: $50-200
   - Market Share: ~20%
   - Avg Profit Margin: 35%

2. Womenswear
   - Price Range: $60-250
   - Market Share: ~35%
   - Avg Profit Margin: 38%

3. Accessories
   - Price Range: $20-100
   - Market Share: ~15%
   - Avg Profit Margin: 45%

4. Footwear
   - Price Range: $80-250
   - Market Share: ~20%
   - Avg Profit Margin: 32%

5. Activewear
   - Price Range: $40-150
   - Market Share: ~10%
   - Avg Profit Margin: 40%
```

---

## Promotion Types

| Type | Frequency | Impact on Sales | Impact on Margin |
|------|-----------|-----------------|------------------|
| **None** | 50% | Baseline | Baseline |
| **Discount** | 20% | +25% volume | -10% margin |
| **BOGO** | 15% | +40% volume | -15% margin |
| **Seasonal Sale** | 10% | +60% volume | -8% margin |
| **Clearance** | 5% | +80% volume | -25% margin |

---

## Stores

### List of 15 Stores
```
1. Store A  (East Region)     → High traffic, Premium items
2. Store B  (East Region)     → Balanced mix
3. Store C  (East Region)     → Value-focused
4. Store D  (Central Region)  → High traffic, Premium items
5. Store E  (Central Region)  → Balanced mix
6. Store F  (Central Region)  → High volume
7. Store G  (Central Region)  → Balanced mix
8. Store H  (West Region)     → Premium items, High AOV
9. Store I  (West Region)     → Balanced mix
10. Store J (West Region)     → High footfall
11. Store K (South Region)    → Growing market
12. Store L (South Region)    → Emerging
13. Store M (South Region)    → Value segment
14. Store N (North Region)    → Premium positioning
15. Store O (North Region)    → High volume, Busy
```

---

## Customer Data (customer_df)

### Core Columns

| Column | Type | Description | Example | Range |
|--------|------|-------------|---------|-------|
| **customer_id** | String | Unique customer ID | C000001 | C000000 - C000999 |
| **segment** | String | Customer segment | "Premium" | 4 segments |
| **total_spend** | Float | Lifetime spend | $2,450.00 | $50 - $10,000 |
| **num_purchases** | Int | Purchase count | 15 | 1-100 |
| **avg_order_value** | Float | Average transaction | $163.33 | $30 - $400 |
| **days_since_purchase** | Int | Days since last buy | 25 | 0-365 |
| **return_rate** | Float | Product return % | 0.08 | 0-20% |
| **lifetime_value** | Float | CLV adjusted for returns | $2,254.00 | Calculated |
| **preferred_category** | String | Most purchased category | "Womenswear" | 5 categories |
| **signup_date** | Date | Customer registration | 2022-06-10 | Last 2 years |

---

## Customer Segments

### Premium Buyers
- **Size**: 15% of customer base
- **Avg Total Spend**: $3,500-$5,000
- **Avg Purchase Count**: 50-100
- **Avg Order Value**: $200-$400
- **Return Rate**: 0-5%
- **Churn Risk**: Low
- **Days Since Purchase**: 0-30
- **Lifetime Value**: $3,000-$5,000
- **Strategy**: VIP treatment, exclusive offers, personal shopper

### Frequent Shoppers
- **Size**: 50% of customer base
- **Avg Total Spend**: $1,200-$2,000
- **Avg Purchase Count**: 15-40
- **Avg Order Value**: $80-$150
- **Return Rate**: 5-10%
- **Churn Risk**: Medium
- **Days Since Purchase**: 10-60
- **Lifetime Value**: $1,000-$1,800
- **Strategy**: Loyalty rewards, frequent promotions, personalization

### Dormant Customers
- **Size**: 15% of customer base
- **Avg Total Spend**: $400-$800
- **Avg Purchase Count**: 3-10
- **Avg Order Value**: $60-$120
- **Return Rate**: 10-20%
- **Churn Risk**: Very High
- **Days Since Purchase**: 60-365
- **Lifetime Value**: $300-$650
- **Strategy**: Win-back campaigns, special incentives, re-engagement

### New Customers
- **Size**: 20% of customer base
- **Avg Total Spend**: $150-$400
- **Avg Purchase Count**: 1-4
- **Avg Order Value**: $50-$150
- **Return Rate**: 10-15%
- **Churn Risk**: High
- **Days Since Purchase**: 0-30
- **Lifetime Value**: $120-$350
- **Strategy**: Welcome series, onboarding, satisfaction focus

---

## Calculated Metrics

### At Transaction Level

```python
# Profit Margin %
profit_margin = (profit / sales) * 100

# Unit Economics
units_per_transaction = quantity
revenue_per_unit = sales / quantity

# Inventory Metrics
turnover_per_transaction = quantity / stock
```

### At Daily Level (Aggregated)

```python
# Daily Metrics
daily_sales = SUM(sales)
daily_profit = SUM(profit)
daily_footfall = SUM(footfall)
daily_transactions = COUNT(*)

# Efficiency
daily_conversion_rate = daily_sales / daily_footfall
daily_avg_transaction = daily_sales / daily_transactions
```

### At Store Level (Aggregated)

```python
# Store Performance
store_total_sales = SUM(sales)
store_total_profit = SUM(profit)
store_profit_margin = store_total_profit / store_total_sales
store_aov = store_total_sales / COUNT(*)
store_conversion = store_total_sales / SUM(footfall)
store_turnover = SUM(quantity) / AVG(stock)
```

### At Category Level (Aggregated)

```python
# Category Performance
category_sales = SUM(sales)
category_margin = SUM(profit) / category_sales
category_volume = SUM(quantity)
category_concentration = category_sales / total_sales
```

### At Customer Level

```python
# Customer Metrics
customer_clv = total_spend * (1 - return_rate)
customer_frequency = num_purchases / days_since_signup
customer_retention = (current_purchases / past_purchases) * 100
customer_churn_risk = HIGH if days_since_purchase > 90 else LOW
```

---

## Aggregation Levels

### Time-based Aggregation
```
Daily → Weekly → Monthly → Quarterly → Yearly
(All metrics can be aggregated across time)
```

### Geographic Aggregation
```
Store → Region → Country
(Store Level used in this dashboard)
```

### Product Aggregation
```
Individual Items → Category → Department → Company
(Category Level used in this dashboard)
```

### Customer Aggregation
```
Individual Customer → Segment → Cohort → Total
(Segment Level used in this dashboard)
```

---

## Statistical Properties

### Sales Data Distribution
```
Sales:
- Mean: $85.50
- Median: $75.00
- Std Dev: $120.00
- Skewness: 0.85 (right-skewed, high-value outliers)
- Kurtosis: 2.1

Quantity:
- Mean: 3.2 units
- Mode: 2 units
- Range: 1-8 units

Footfall:
- Mean: 52 visitors/day
- Median: 50 visitors/day
- Range: 10-100 visitors/day
```

### Customer Data Distribution
```
Total Spend:
- Mean: $1,200
- Median: $850
- Range: $50 - $10,000
- Skewness: Highly right-skewed (power law distribution)
- Pareto: 20% of customers = 80% of revenue

Purchase Count:
- Mean: 12 purchases
- Median: 8 purchases
- Range: 1-100 purchases

Days Since Purchase:
- Mean: 45 days
- Median: 30 days
- Range: 0-365 days
```

---

## Seasonal Patterns

### Monthly Adjustments to Sales

```
January:   -20% (Post-holiday, slow period)
February:  -10% (Gradual recovery)
March:     0% (Baseline)
April:     +10% (Spring boost)
May:       0% (Return to baseline)
June:      -10% (Pre-summer discount period)
July:      +20% (Summer peak)
August:    +30% (Summer peak)
September: +10% (Back-to-school)
October:   -5% (Mid-year slowdown)
November:  +40% (Black Friday, holiday prep)
December:  +50% (Holiday season, peak)
```

### Weekly Patterns
```
Monday:    100% (Baseline)
Tuesday:   95%
Wednesday: 98%
Thursday:  102%
Friday:    110% (Weekend prep)
Saturday:  125% (Peak weekend traffic)
Sunday:    105% (End of weekend)
```

---

## Data Quality Notes

### Completeness
- ✅ 100% of fields populated
- ✅ No missing values in synthetic data
- ✅ All transactions valid

### Consistency
- ✅ Sales = Quantity × Price
- ✅ Profit = Sales × Margin (30-50%)
- ✅ Dates within valid range
- ✅ Stock levels always positive

### Realism
- ✅ Follows retail industry benchmarks
- ✅ Incorporates seasonal patterns
- ✅ Includes promotion effects
- ✅ Customer segments realistic

### Variability
- ✅ Natural variation in daily sales
- ✅ Outliers included for real-world feel
- ✅ Multiple category performance profiles
- ✅ Diverse customer behaviors

---

## Using This Data

### For Analysis
- Use daily aggregations for trends
- Use store-level for benchmarking
- Use customer-level for segmentation

### For Forecasting
- Use historical sales for time series
- Account for seasonality (monthly factors)
- Consider promotion impact on baseline

### For Alerts
- Low stock: < 10 units
- Slow moving: < 1 unit/day turnover
- Overstocking: 10x+ above average
- Negative margins: Profit ≤ 0

### For Recommendations
- Focus on high-margin items
- Target at-risk customer segments
- Optimize inventory for top-sellers
- Expand best-performing categories

---

## Export Format Notes

### CSV Export
- Comma-separated values
- Date format: YYYY-MM-DD
- Currency: USD (numeric only, no $ symbol)
- Decimal separator: . (period)

### Report Format
- Markdown (.md)
- Markdown (.txt)
- PDF-ready structure

---

## Glossary

| Term | Definition |
|------|-----------|
| **AOV** | Average Order Value = Total Sales / Orders |
| **CLV** | Customer Lifetime Value = Total Spend × (1 - Return Rate) |
| **COGS** | Cost of Goods Sold = Sales - Profit |
| **Conversion Rate** | % of Visitors Who Made Purchase = Sales / Footfall |
| **Inventory Turnover** | How Many Times Stock Sold = Units Sold / Avg Stock |
| **Margin** | Profit Percentage = Profit / Sales |
| **Promotion ROI** | Return on Promotion Spend = Profit / Cost |
| **Seasonality** | Predictable Variation by Time of Year |
| **SKU** | Stock Keeping Unit (Product) |
| **Churn** | Customer Attrition / Non-Purchase |

---

**This data dictionary is a living document. Update as you integrate real data.** 📝

<img src="Snowflake_Logo.svg" width="200">

# Medallion Architecture

This project contains the a Sample data warehouse medallion architecture design for Snowflake, including Bronze (Raw), Silver (Refined), and Gold (Modeled) layers with integrated social media sentiment analysis.

## 📁 Project Files

### Core Application
- **`medallion_architecture_app.py`** - Streamlit app for viewing ER diagrams with zoom functionality
- **`requirements_local.txt`** - Python dependencies for the Streamlit app
- **`deployment_instructions_local.md`** - Step-by-step deployment guide for Snowflake

### ER Diagrams (SVG)
- **`bronze_layer_er_diagram.svg`** - Raw data layer diagram
- **`silver_layer_er_diagram.svg`** - Refined data layer diagram  
- **`gold_layer_er_diagram.svg`** - Modeled data layer diagram

### Source Files (Mermaid)
- **`bronze_layer_er_diagram.mmd`** - Source for Bronze layer
- **`silver_layer_er_diagram.mmd`** - Source for Silver layer
- **`gold_layer_er_diagram.mmd`** - Source for Gold layer

### Documentation
- **`Medallion_Architecture_Documentation.md`** - Comprehensive architecture documentation

## 🚀 Quick Start

### 1. Deploy to Snowflake
```bash
# Upload files to your Snowflake stage
PUT file://nasm_architecture_app.py @YOUR_APP_STAGE/;
PUT file://bronze_layer_er_diagram.svg @YOUR_APP_STAGE/;
PUT file://silver_layer_er_diagram.svg @YOUR_APP_STAGE/;
PUT file://gold_layer_er_diagram.svg @YOUR_APP_STAGE/;
PUT file://requirements_local.txt @YOUR_APP_STAGE/;
```

### 2. Create Streamlit App
```sql
CREATE OR REPLACE STREAMLIT MEDALLION_ARCHITECTURE_VIEWER
ROOT_LOCATION = '@YOUR_APP_STAGE/'
MAIN_FILE = 'medallion_architecture_app.py'
COMMENT = 'Medallion Architecture Viewer with Local SVG Files';
```

## ✨ Features

### Streamlit App
- **📊 Interactive ER Diagrams** - View Bronze, Silver, and Gold layer designs
- **🔍 Zoom Functionality** - Zoom in/out and reset (50% to 300%)
- **⬇️ Download SVG** - Export diagrams for external use
- **📱 Responsive Design** - Works well in Snowflake's Streamlit environment

### Architecture Layers
- **🥉 Bronze (Raw)** - Ingests sales data and social media feeds (Twitter, TikTok, Facebook)
- **🥈 Silver (Refined)** - Applies data quality rules, sentiment analysis, and standardization
- **🥇 Gold (Modeled)** - Star schema with fact tables optimized for analytics

## 🛠️ Regenerating Diagrams

If you need to modify the ER diagrams:

### 1. Install Mermaid CLI
```bash
npm install -g @mermaid-js/mermaid-cli
```

### 2. Convert Mermaid to SVG
```bash
mmdc -i bronze_layer_er_diagram.mmd -o bronze_layer_er_diagram.svg
mmdc -i silver_layer_er_diagram.mmd -o silver_layer_er_diagram.svg
mmdc -i gold_layer_er_diagram.mmd -o gold_layer_er_diagram.svg
```

### 3. Re-upload SVGs
```bash
PUT file://bronze_layer_er_diagram.svg @YOUR_APP_STAGE/;
PUT file://silver_layer_er_diagram.svg @YOUR_APP_STAGE/;
PUT file://gold_layer_er_diagram.svg @YOUR_APP_STAGE/;
```

## 📋 Architecture Overview

### Bronze Layer (Raw Data)
- **Sales transactions** with all original fields
- **Customer, product, service, certification, training** master data
- **Social media posts** from Twitter, TikTok, Facebook
- **Raw JSON** preservation for flexibility

### Silver Layer (Refined Data)
- **Data quality scoring** and cleansing
- **Sentiment analysis** on social media content
- **Standardized reference tables** for consistent values
- **Business key generation** and SCD implementation

### Gold Layer (Modeled Data)
- **Star schema design** optimized for analytics
- **Fact tables**: Sales, Social Sentiment, Customer Engagement
- **Dimension tables**: Customer, Product, Service, Certification, Training, Date, Geography, Sales Rep, Social Platform
- **Performance optimized** for BI tools and reporting

## 🎯 Key Business Value

- **360° Customer View** - Combines transactional and social media data
- **Sentiment-Driven Insights** - Rank services by customer feedback
- **Scalable Architecture** - Medallion pattern supports growth
- **Data Quality Focus** - Multiple validation and scoring layers
- **Analytics Ready** - Optimized for business intelligence tools

## 📞 Support

For questions about this architecture or deployment, refer to:
- `deployment_instructions_local.md` for setup guidance
- `Medallion_Architecture_Documentation.md` for detailed technical specifications 

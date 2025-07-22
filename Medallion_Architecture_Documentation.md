# NASM Medallion Architecture Documentation

## Overview

This document outlines the medallion architecture (Bronze → Silver → Gold) designed for the National Academy of Sports Medicine (NASM) data warehouse implementation on Snowflake. The architecture integrates sales data with social media sentiment analysis to provide comprehensive business intelligence capabilities.

## Architecture Layers

### Bronze Layer (Raw Data)
**Purpose**: Ingestion and storage of raw data in its original format with minimal transformation.

**Key Characteristics**:
- Data stored in original format with raw JSON for flexibility
- Minimal data validation and transformation
- Comprehensive audit trail with ingestion timestamps
- Source system tracking for data lineage
- Supports schema evolution and varying data formats

**Main Entities**:
- **Sales Transactions**: Core transactional data from sales systems
- **Customer Data**: Raw customer information from CRM and registration systems
- **Product Catalog**: Products, services, certifications, and training programs
- **Social Media Data**: Raw posts from Twitter, TikTok, Facebook, and other platforms
- **Social Media Mentions**: Brand and product mentions across platforms

**Data Sources**:
- Sales systems (CRM, e-commerce, POS)
- Social media APIs (Twitter, TikTok, Facebook, Instagram, LinkedIn)
- Customer registration systems
- Product and certification management systems
- Training management platforms

### Silver Layer (Refined Data)
**Purpose**: Cleaned, standardized, and enriched data ready for business logic application.

**Key Characteristics**:
- Data quality rules applied and scored
- Standardized formats and values
- Basic sentiment analysis on social media content
- Unified schemas across source systems
- Data deduplication and consolidation
- Business key generation for downstream consumption

**Transformations Applied**:
- **Data Cleansing**: Email validation, phone formatting, address standardization
- **Standardization**: Payment methods, sales channels, product categories
- **Enrichment**: Customer tiers, sentiment scores, engagement metrics
- **Validation**: Data quality scoring and flagging
- **Deduplication**: Customer and product record consolidation

**Key Enhancements**:
- Sentiment analysis using NLP services
- Customer segmentation and tiering
- Product categorization standardization
- Sales representative territory assignment
- Geographic data enrichment

### Gold Layer (Modeled Data)
**Purpose**: Business-ready dimensional model optimized for analytics and reporting.

**Key Characteristics**:
- Star schema design for optimal query performance
- Slowly Changing Dimensions (SCD) for historical analysis
- Pre-calculated metrics and KPIs
- Denormalized structure for fast aggregations
- Business-friendly naming conventions

**Fact Tables**:
1. **FACT_SALES**: Core sales transactions with all dimensional context
2. **FACT_SOCIAL_SENTIMENT**: Social media sentiment with product/service correlations
3. **FACT_CUSTOMER_ENGAGEMENT**: Aggregated customer engagement metrics

**Dimension Tables**:
1. **DIM_CUSTOMER**: Customer master with SCD Type 2 for historical tracking
2. **DIM_PRODUCT**: Product catalog with lifecycle management
3. **DIM_SERVICE**: Service offerings and pricing
4. **DIM_CERTIFICATION**: Certification programs and requirements
5. **DIM_TRAINING**: Training programs and delivery methods
6. **DIM_DATE**: Comprehensive date dimension with fiscal calendar
7. **DIM_SALES_REP**: Sales representative information and territories
8. **DIM_GEOGRAPHY**: Geographic hierarchy and market data
9. **DIM_SOCIAL_PLATFORM**: Social media platform characteristics

## Data Flow and Transformation Logic

### Bronze to Silver Transformation
```sql
-- Example: Customer data cleaning and standardization
INSERT INTO REFINED_CUSTOMERS
SELECT 
    GENERATE_UUID() as customer_key,
    customer_id,
    TRIM(UPPER(first_name)) as first_name_clean,
    TRIM(UPPER(last_name)) as last_name_clean,
    LOWER(TRIM(email)) as email_clean,
    REGEXP_REPLACE(phone, '[^0-9]', '') as phone_clean,
    -- Additional data quality and standardization logic
FROM RAW_CUSTOMERS
WHERE email_validation_score > 0.8;
```

### Silver to Gold Transformation
```sql
-- Example: Sales fact table population
INSERT INTO FACT_SALES
SELECT 
    GENERATE_UUID() as sales_fact_key,
    rst.transaction_id,
    dc.customer_key,
    dp.product_key,
    -- Dimensional keys and measures
FROM REFINED_SALES_FACTS rst
JOIN DIM_CUSTOMER dc ON rst.customer_key = dc.customer_id
JOIN DIM_PRODUCT dp ON rst.product_key = dp.product_id;
```

## Key Design Decisions

### 1. Social Media Integration Strategy
- **Sentiment Analysis**: Implemented at Silver layer using cloud-native NLP services
- **Brand Monitoring**: Keyword-based filtering for NASM, certification, and training mentions
- **Customer Attribution**: Linking social profiles to customer records where possible
- **Engagement Scoring**: Weighted scoring based on platform-specific engagement metrics

### 2. Customer Data Management
- **Master Data Management**: Customer golden record creation in Silver layer
- **Privacy Compliance**: PII handling with appropriate masking and retention policies
- **Slowly Changing Dimensions**: Type 2 SCD for customer attribute changes
- **Customer Segmentation**: Automated tier assignment based on purchase behavior

### 3. Product Hierarchy Design
- **Unified Catalog**: Consolidation of products, services, certifications, and training
- **Category Standardization**: Consistent taxonomy across all offering types
- **Pricing History**: Track price changes for trend analysis
- **Lifecycle Management**: Track product launch, modification, and retirement dates

### 4. Time Dimension Strategy
- **Fiscal Calendar**: NASM-specific fiscal year and period definitions
- **Multiple Date Types**: Transaction date, due date, completion date handling
- **Time Zone Standardization**: UTC storage with local time zone conversion views

## Snowflake Implementation Considerations

### 1. Storage and Compute
- **File Formats**: Use Parquet for Bronze layer efficiency
- **Clustering Keys**: Optimize clustering on date and customer dimensions
- **Materialized Views**: Implement for frequently accessed Silver layer aggregations
- **Warehouse Sizing**: Separate warehouses for ETL vs. BI workloads

### 2. Security and Governance
- **Role-Based Access**: Implement least privilege access model
- **Data Classification**: Tag PII and sensitive data appropriately
- **Audit Logging**: Enable query history and access monitoring
- **Encryption**: Leverage Snowflake's automatic encryption capabilities

### 3. Performance Optimization
- **Micro-Partitions**: Leverage automatic partitioning on date columns
- **Result Caching**: Utilize Snowflake's automatic result caching
- **Columnar Storage**: Optimize for analytical query patterns
- **Virtual Warehouses**: Size appropriately for workload requirements

### 4. Data Pipeline Architecture
- **Incremental Loading**: Implement change data capture where possible
- **Error Handling**: Robust error handling and data quality monitoring
- **Orchestration**: Use Snowflake Tasks or external orchestration tools
- **Monitoring**: Implement data quality and pipeline monitoring dashboards

## Business Value and Use Cases

### 1. Sales Analytics
- Revenue trend analysis by product, service, and certification
- Sales performance tracking and rep scorecards
- Customer lifetime value and churn analysis
- Geographic performance and market opportunity analysis

### 2. Social Media Intelligence
- Brand sentiment monitoring and trend analysis
- Product/service mention tracking and engagement metrics
- Influencer identification and partnership opportunities
- Crisis monitoring and reputation management

### 3. Customer Insights
- Customer journey analysis and touchpoint optimization
- Personalization and recommendation engines
- Customer segmentation and targeted marketing
- Social media influence on purchase behavior

### 4. Product Performance
- Product adoption and lifecycle analytics
- Certification completion rates and success factors
- Training effectiveness and customer satisfaction
- Cross-sell and upsell opportunity identification

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- Set up Snowflake environment and security
- Implement Bronze layer data ingestion
- Establish data governance framework
- Create initial data quality monitoring

### Phase 2: Refinement (Weeks 5-8)
- Develop Silver layer transformations
- Implement sentiment analysis pipeline
- Create data quality dashboards
- Establish master data management processes

### Phase 3: Analytics (Weeks 9-12)
- Build Gold layer dimensional model
- Create initial set of business dashboards
- Implement key performance indicators
- Train business users on new capabilities

### Phase 4: Advanced Analytics (Weeks 13-16)
- Develop predictive models
- Implement real-time social monitoring
- Create advanced customer segmentation
- Deploy recommendation engines

## Monitoring and Maintenance

### Data Quality Metrics
- **Completeness**: Percentage of required fields populated
- **Accuracy**: Data validation rule compliance
- **Consistency**: Cross-system data alignment
- **Timeliness**: Data freshness and latency monitoring

### Performance Metrics
- **Query Performance**: Average query execution times
- **Data Processing**: ETL job completion times and success rates
- **Storage Utilization**: Storage growth and optimization opportunities
- **User Adoption**: Dashboard usage and user engagement metrics

## Conclusion

This medallion architecture provides NASM with a scalable, maintainable, and business-focused data platform that integrates traditional sales analytics with modern social media intelligence. The layered approach ensures data quality while providing flexibility for future enhancements and use cases.

The architecture leverages Snowflake's cloud-native capabilities to deliver high performance, automatic scaling, and enterprise-grade security while minimizing operational overhead and maximizing business value. 
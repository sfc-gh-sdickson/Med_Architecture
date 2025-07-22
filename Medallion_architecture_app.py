import streamlit as st
from pathlib import Path
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="NASM Medallion Architecture",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .layer-description {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .svg-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #ddd;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .success-info {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    .error-info {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #dc3545;
        }
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
        padding: 10px;
        border-bottom: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

def read_svg(path: str) -> Optional[str]:
    """Safely read SVG files with enhanced error handling"""
    try:
        svg_path = Path(path)
        if not svg_path.exists() or not svg_path.is_file():
            logger.warning(f"SVG file not found: {path}")
            return None

        # Additional security check for file extension
        if svg_path.suffix.lower() != '.svg':
            logger.warning(f"File is not an SVG: {path}")
            return None

        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Basic SVG validation
            if not content.strip().startswith('<svg'):
                logger.warning(f"Invalid SVG content in file: {path}")
                return None
            return content

    except Exception as e:
        logger.error(f"Error reading SVG file {path}: {str(e)}")
        return None

# Main title
st.markdown('<h1 class="main-header">🏗️ NASM Medallion Architecture</h1>', unsafe_allow_html=True)

# Initialize session state for zoom
if 'zoom_level' not in st.session_state:
    st.session_state.zoom_level = 100  # Start at 100% to fill container width

# Sidebar for navigation
svg_content = read_svg("Snowflake_Logo.svg")
if svg_content:
    st.sidebar.image(svg_content, width=150)

st.sidebar.title("🗂️ Navigation")
selected_layer = st.sidebar.selectbox(
    "Select Architecture Layer:",
    ["Bronze Layer (Raw Data)", "Silver Layer (Refined Data)", "Gold Layer (Modeled Data)"]
)

# Layer descriptions
layer_descriptions = {
    "Bronze Layer (Raw Data)": {
        "description": "**Raw Data Ingestion**: Stores data in its original format with minimal transformation. Includes sales transactions, customer data, products, services, certifications, training programs, and social media data from Twitter, TikTok, and Facebook.",
        "color": "#8B4513",
        "file": "bronze_layer_er_diagram.mmd",
        "svg_file": "bronze_layer_er_diagram.svg"
    },
    "Silver Layer (Refined Data)": {
        "description": "**Cleaned & Standardized**: Data quality rules applied, sentiment analysis on social media content, unified schemas, and business key generation. Reference tables for standardized values and data quality scoring.",
        "color": "#C0C0C0",
        "file": "silver_layer_er_diagram.mmd",
        "svg_file": "silver_layer_er_diagram.svg"
    },
    "Gold Layer (Modeled Data)": {
        "description": "**Analytics-Ready**: Dimensional model (star schema) with fact tables for Sales, Social Sentiment, and Customer Engagement. Comprehensive dimension tables optimized for business intelligence and reporting.",
        "color": "#FFD700",
        "file": "gold_layer_er_diagram.mmd",
        "svg_file": "gold_layer_er_diagram.svg"
    }
}

# Display selected layer info
layer_info = layer_descriptions[selected_layer]
st.markdown(f'<div class="layer-description" style="border-left: 4px solid {layer_info["color"]};">{layer_info["description"]}</div>', unsafe_allow_html=True)

# Mermaid diagram content for each layer
mermaid_diagrams = {
    "bronze_layer_er_diagram.mmd": '''erDiagram
    RAW_SALES_TRANSACTIONS {
        string transaction_id PK
        string customer_id FK
        string product_id FK
        string service_id FK
        string certification_id FK
        string training_id FK
        decimal amount
        datetime transaction_date
        string payment_method
        string sales_channel
        string sales_rep_id
        string raw_data_json
        datetime ingested_at
        string source_system
    }
    
    RAW_CUSTOMERS {
        string customer_id PK
        string first_name
        string last_name
        string email
        string phone
        string address_line1
        string address_line2
        string city
        string state
        string zip_code
        string country
        datetime registration_date
        string customer_type
        string raw_data_json
        datetime ingested_at
        string source_system
    }
    
    RAW_PRODUCTS {
        string product_id PK
        string product_name
        string product_category
        string product_subcategory
        decimal price
        string description
        string status
        datetime created_date
        string raw_data_json
        datetime ingested_at
        string source_system
    }
    
    RAW_SERVICES {
        string service_id PK
        string service_name
        string service_type
        string service_category
        decimal price
        string duration
        string description
        string status
        string raw_data_json
        datetime ingested_at
        string source_system
    }
    
    RAW_CERTIFICATIONS {
        string certification_id PK
        string certification_name
        string certification_level
        string certification_type
        decimal price
        string requirements
        string validity_period
        string status
        string raw_data_json
        datetime ingested_at
        string source_system
    }
    
    RAW_TRAINING_PROGRAMS {
        string training_id PK
        string training_name
        string training_type
        string training_category
        decimal price
        string duration
        string format
        string description
        string status
        string raw_data_json
        datetime ingested_at
        string source_system
    }
    
    RAW_TWITTER_POSTS {
        string tweet_id PK
        string user_id
        string username
        string tweet_text
        int retweet_count
        int like_count
        int reply_count
        datetime created_at
        string hashtags
        string mentions
        string raw_data_json
        datetime ingested_at
        string source_api
    }
    
    RAW_TIKTOK_VIDEOS {
        string video_id PK
        string user_id
        string username
        string video_description
        int view_count
        int like_count
        int comment_count
        int share_count
        datetime created_at
        string hashtags
        string effects
        string raw_data_json
        datetime ingested_at
        string source_api
    }
    
    RAW_FACEBOOK_POSTS {
        string post_id PK
        string page_id
        string page_name
        string post_content
        string post_type
        int like_count
        int comment_count
        int share_count
        datetime created_at
        string raw_data_json
        datetime ingested_at
        string source_api
    }
    
    RAW_SOCIAL_MEDIA_MENTIONS {
        string mention_id PK
        string platform
        string post_id
        string mention_text
        string sentiment_raw
        string brand_keywords
        datetime mention_date
        string user_id
        string raw_data_json
        datetime ingested_at
        string source_system
    }
    
    RAW_SALES_TRANSACTIONS ||--o{ RAW_CUSTOMERS : "customer_id"
    RAW_SALES_TRANSACTIONS ||--o{ RAW_PRODUCTS : "product_id"
    RAW_SALES_TRANSACTIONS ||--o{ RAW_SERVICES : "service_id"
    RAW_SALES_TRANSACTIONS ||--o{ RAW_CERTIFICATIONS : "certification_id"
    RAW_SALES_TRANSACTIONS ||--o{ RAW_TRAINING_PROGRAMS : "training_id"''',

    "silver_layer_er_diagram.mmd": '''erDiagram
    REFINED_SALES_FACTS {
        string sales_fact_id PK
        string transaction_id UK
        string customer_key FK
        string product_key FK
        string service_key FK
        string certification_key FK
        string training_key FK
        decimal gross_amount
        decimal discount_amount
        decimal net_amount
        decimal tax_amount
        date transaction_date
        string payment_method_std
        string sales_channel_std
        string sales_rep_key FK
        string currency_code
        boolean is_refunded
        datetime created_timestamp
        datetime modified_timestamp
        string data_quality_score
    }
    
    REFINED_CUSTOMERS {
        string customer_key PK
        string customer_id UK
        string first_name_clean
        string last_name_clean
        string email_clean
        string phone_clean
        string full_address
        string city_clean
        string state_code
        string zip_code_clean
        string country_code
        date registration_date
        string customer_type_std
        string customer_tier
        boolean is_active
        datetime created_timestamp
        datetime modified_timestamp
        string data_quality_score
    }
    
    REFINED_PRODUCTS {
        string product_key PK
        string product_id UK
        string product_name_clean
        string product_category_std
        string product_subcategory_std
        decimal current_price
        string description_clean
        string status_std
        date effective_start_date
        date effective_end_date
        boolean is_current
        datetime created_timestamp
        datetime modified_timestamp
    }
    
    REFINED_SERVICES {
        string service_key PK
        string service_id UK
        string service_name_clean
        string service_type_std
        string service_category_std
        decimal current_price
        int duration_minutes
        string description_clean
        string status_std
        date effective_start_date
        date effective_end_date
        boolean is_current
        datetime created_timestamp
        datetime modified_timestamp
    }
    
    REFINED_CERTIFICATIONS {
        string certification_key PK
        string certification_id UK
        string certification_name_clean
        string certification_level_std
        string certification_type_std
        decimal current_price
        string requirements_clean
        int validity_days
        string status_std
        date effective_start_date
        date effective_end_date
        boolean is_current
        datetime created_timestamp
        datetime modified_timestamp
    }
    
    REFINED_TRAINING_PROGRAMS {
        string training_key PK
        string training_id UK
        string training_name_clean
        string training_type_std
        string training_category_std
        decimal current_price
        int duration_hours
        string format_std
        string description_clean
        string status_std
        date effective_start_date
        date effective_end_date
        boolean is_current
        datetime created_timestamp
        datetime modified_timestamp
    }
    
    REFINED_SOCIAL_MEDIA_POSTS {
        string post_key PK
        string platform_std
        string original_post_id
        string user_id_clean
        string username_clean
        string content_clean
        string content_language
        int engagement_score
        datetime post_timestamp
        string sentiment_score
        string sentiment_category
        decimal sentiment_confidence
        string brand_mention_type
        boolean contains_nasm_keywords
        datetime created_timestamp
        datetime modified_timestamp
    }
    
    REFINED_SENTIMENT_ANALYSIS {
        string sentiment_key PK
        string post_key FK
        string sentiment_engine
        decimal positive_score
        decimal negative_score
        decimal neutral_score
        string overall_sentiment
        decimal confidence_score
        string keywords_extracted
        string topics_identified
        datetime analysis_timestamp
        datetime created_timestamp
    }
    
    REFINED_SALES_REPS {
        string sales_rep_key PK
        string sales_rep_id UK
        string first_name
        string last_name
        string email
        string territory
        string role
        date hire_date
        boolean is_active
        datetime created_timestamp
        datetime modified_timestamp
    }
    
    REF_PAYMENT_METHODS {
        string payment_method_code PK
        string payment_method_name
        string payment_type
        boolean is_active
    }
    
    REF_SALES_CHANNELS {
        string channel_code PK
        string channel_name
        string channel_type
        boolean is_active
    }
    
    REF_SENTIMENT_CATEGORIES {
        string sentiment_code PK
        string sentiment_name
        string sentiment_description
        decimal min_score
        decimal max_score
    }
    
    REFINED_SALES_FACTS ||--|| REFINED_CUSTOMERS : "customer_key"
    REFINED_SALES_FACTS ||--o| REFINED_PRODUCTS : "product_key"
    REFINED_SALES_FACTS ||--o| REFINED_SERVICES : "service_key"
    REFINED_SALES_FACTS ||--o| REFINED_CERTIFICATIONS : "certification_key"
    REFINED_SALES_FACTS ||--o| REFINED_TRAINING_PROGRAMS : "training_key"
    REFINED_SALES_FACTS ||--|| REFINED_SALES_REPS : "sales_rep_key"
    REFINED_SOCIAL_MEDIA_POSTS ||--|| REFINED_SENTIMENT_ANALYSIS : "post_key"''',

    "gold_layer_er_diagram.mmd": '''erDiagram
    FACT_SALES {
        string sales_fact_key PK
        string transaction_id UK
        int customer_key FK
        int product_key FK
        int service_key FK
        int certification_key FK
        int training_key FK
        int sales_rep_key FK
        int transaction_date_key FK
        int geography_key FK
        decimal gross_amount
        decimal discount_amount
        decimal net_amount
        decimal tax_amount
        decimal cost_amount
        decimal profit_amount
        int quantity
        string payment_method
        string sales_channel
        string transaction_type
        boolean is_refunded
        decimal refund_amount
        datetime transaction_timestamp
        datetime created_date
        datetime modified_date
    }
    
    FACT_SOCIAL_SENTIMENT {
        string sentiment_fact_key PK
        int customer_key FK
        int product_key FK
        int service_key FK
        int certification_key FK
        int training_key FK
        int post_date_key FK
        int platform_key FK
        string post_id
        decimal sentiment_score
        string sentiment_category
        decimal sentiment_confidence
        int engagement_count
        int reach_count
        int share_count
        boolean mentions_nasm
        string brand_mention_type
        string content_category
        datetime post_timestamp
        datetime created_date
    }
    
    FACT_CUSTOMER_ENGAGEMENT {
        string engagement_fact_key PK
        int customer_key FK
        int date_key FK
        int product_purchases
        int service_purchases
        int certification_purchases
        int training_purchases
        decimal total_revenue
        decimal average_order_value
        int social_mentions
        decimal avg_sentiment_score
        int days_since_last_purchase
        string engagement_tier
        datetime created_date
    }
    
    DIM_CUSTOMER {
        int customer_key PK
        string customer_id UK
        string first_name
        string last_name
        string full_name
        string email
        string phone
        date birth_date
        int age
        string age_group
        string gender
        string customer_type
        string customer_tier
        string acquisition_channel
        date registration_date
        int days_as_customer
        string lifecycle_stage
        boolean is_active
        date effective_start_date
        date effective_end_date
        boolean is_current
        int version_number
        datetime created_date
        datetime modified_date
    }
    
    DIM_PRODUCT {
        int product_key PK
        string product_id UK
        string product_name
        string product_code
        string product_category
        string product_subcategory
        string product_line
        string brand
        decimal list_price
        decimal cost
        string product_status
        string product_description
        date launch_date
        date discontinue_date
        boolean is_active
        datetime created_date
        datetime modified_date
    }
    
    DIM_SERVICE {
        int service_key PK
        string service_id UK
        string service_name
        string service_code
        string service_type
        string service_category
        string delivery_method
        int duration_hours
        decimal list_price
        decimal cost
        string service_status
        string service_description
        date launch_date
        date discontinue_date
        boolean is_active
        datetime created_date
        datetime modified_date
    }
    
    DIM_CERTIFICATION {
        int certification_key PK
        string certification_id UK
        string certification_name
        string certification_code
        string certification_level
        string certification_type
        string specialization_area
        int validity_years
        string prerequisites
        decimal list_price
        decimal cost
        string certification_status
        date launch_date
        date discontinue_date
        boolean is_active
        datetime created_date
        datetime modified_date
    }
    
    DIM_TRAINING {
        int training_key PK
        string training_id UK
        string training_name
        string training_code
        string training_type
        string training_category
        string format
        string delivery_method
        int duration_hours
        string difficulty_level
        decimal list_price
        decimal cost
        string training_status
        date launch_date
        date discontinue_date
        boolean is_active
        datetime created_date
        datetime modified_date
    }
    
    DIM_DATE {
        int date_key PK
        date full_date UK
        int year
        int quarter
        int month
        int week
        int day
        string month_name
        string day_name
        string quarter_name
        int day_of_year
        int week_of_year
        boolean is_weekend
        boolean is_holiday
        string holiday_name
        string fiscal_year
        string fiscal_quarter
        string fiscal_period
        boolean is_last_day_of_month
        boolean is_first_day_of_month
    }
    
    DIM_SALES_REP {
        int sales_rep_key PK
        string sales_rep_id UK
        string first_name
        string last_name
        string full_name
        string email
        string territory
        string region
        string role
        string manager_name
        date hire_date
        int years_of_service
        string performance_tier
        boolean is_active
        datetime created_date
        datetime modified_date
    }
    
    DIM_GEOGRAPHY {
        int geography_key PK
        string zip_code
        string city
        string county
        string state_code
        string state_name
        string country_code
        string country_name
        string region
        string time_zone
        decimal latitude
        decimal longitude
        int population
        string market_size
        datetime created_date
        datetime modified_date
    }
    
    DIM_SOCIAL_PLATFORM {
        int platform_key PK
        string platform_name UK
        string platform_category
        string platform_type
        string target_audience
        int max_post_length
        boolean supports_video
        boolean supports_images
        string api_version
        boolean is_active
        datetime created_date
        datetime modified_date
    }
    
    FACT_SALES ||--|| DIM_CUSTOMER : "customer_key"
    FACT_SALES ||--o| DIM_PRODUCT : "product_key"
    FACT_SALES ||--o| DIM_SERVICE : "service_key"
    FACT_SALES ||--o| DIM_CERTIFICATION : "certification_key"
    FACT_SALES ||--o| DIM_TRAINING : "training_key"
    FACT_SALES ||--|| DIM_SALES_REP : "sales_rep_key"
    FACT_SALES ||--|| DIM_DATE : "transaction_date_key"
    FACT_SALES ||--|| DIM_GEOGRAPHY : "geography_key"
    
    FACT_SOCIAL_SENTIMENT ||--o| DIM_CUSTOMER : "customer_key"
    FACT_SOCIAL_SENTIMENT ||--o| DIM_PRODUCT : "product_key"
    FACT_SOCIAL_SENTIMENT ||--o| DIM_SERVICE : "service_key"
    FACT_SOCIAL_SENTIMENT ||--o| DIM_CERTIFICATION : "certification_key"
    FACT_SOCIAL_SENTIMENT ||--o| DIM_TRAINING : "training_key"
    FACT_SOCIAL_SENTIMENT ||--|| DIM_DATE : "post_date_key"
    FACT_SOCIAL_SENTIMENT ||--|| DIM_SOCIAL_PLATFORM : "platform_key"
    
    FACT_CUSTOMER_ENGAGEMENT ||--|| DIM_CUSTOMER : "customer_key"
    FACT_CUSTOMER_ENGAGEMENT ||--|| DIM_DATE : "date_key"'''
}

# Get the current diagram content
current_file = layer_info["file"]
current_svg_file = layer_info["svg_file"]
current_diagram = mermaid_diagrams[current_file]

# Create tabs
tab1, tab2 = st.tabs(["📝 Mermaid Source Code", "📊 SVG Diagram"])

with tab1:
    st.subheader(f"📝 {selected_layer} - Mermaid Source")
    st.markdown("**File:** `" + current_file + "`")
    
    # Display the source code with syntax highlighting
    st.code(current_diagram, language="text")
    
    # Download button for the .mmd file
    st.download_button(
        label=f"⬇️ Download {current_file}",
        data=current_diagram,
        file_name=current_file,
        mime="text/plain"
    )

with tab2:
    st.subheader(f"📊 {selected_layer} - SVG Diagram")
    
    # Show what file we're looking for
    st.markdown(f"**Looking for:** `{current_svg_file}` in application directory")
    
    # Try to read the SVG file using your working method
    svg_content = read_svg(current_svg_file)
    
    if svg_content:
        st.markdown(f'<div class="success-info">', unsafe_allow_html=True)
        st.markdown(f"✅ **Successfully loaded SVG content** ({len(svg_content)} characters)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Zoom and Download controls
        st.markdown("**Diagram Controls:**")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        
        with col1:
            if st.button("🔍+ Zoom In", key=f"zoom_in_{current_svg_file}"):
                if st.session_state.zoom_level < 300:
                    st.session_state.zoom_level += 25
                    st.rerun()
        
        with col2:
            if st.button("🔍- Zoom Out", key=f"zoom_out_{current_svg_file}"):
                if st.session_state.zoom_level > 50:
                    st.session_state.zoom_level -= 25
                    st.rerun()
        
        with col3:
            if st.button("🔄 Reset", key=f"zoom_reset_{current_svg_file}"):
                st.session_state.zoom_level = 100  # Reset to fill container width
                st.rerun()
        
        with col4:
            st.markdown(f"**Zoom:** {st.session_state.zoom_level}%")
        
        with col5:
            st.download_button(
                label=f"⬇️ Download",
                data=svg_content,
                file_name=current_svg_file,
                mime="image/svg+xml"
            )

        # Display the SVG with zoom applied
        st.markdown("---")
        
        # Calculate zoom factor
        zoom_factor = st.session_state.zoom_level / 100
        
        # Display SVG directly with markdown to avoid JavaScript errors
        # Modify SVG to fill container width
        if svg_content.startswith('<svg'):
            # Force SVG to fill container width
            svg_modified = svg_content.replace('<svg', '<svg width="100%" height="auto"', 1)
        else:
            svg_modified = svg_content
            
        svg_display_html = f"""
        <div style="background: white; padding: 20px; border-radius: 8px; border: 2px solid #1f77b4; overflow: auto; height: 1500px; width: 100%; position: relative;">
            <div style="transform: scale({zoom_factor}); transform-origin: left top; display: inline-block; min-width: 100%;">
                {svg_modified}
            </div>
        </div>
        """
        
        st.markdown(svg_display_html, unsafe_allow_html=True)
        
    else:
        st.markdown(f'<div class="error-info">', unsafe_allow_html=True)
        st.markdown(f"❌ **Could not load:** `{current_svg_file}`")
        
        # Show debugging info
        st.markdown("**Debug Info:**")
        
        # Check if file exists
        svg_path = Path(current_svg_file)
        st.write(f"• File exists: {svg_path.exists()}")
        st.write(f"• Is file: {svg_path.is_file() if svg_path.exists() else 'N/A'}")
        st.write(f"• File suffix: {svg_path.suffix}")
        
        # List files in current directory
        try:
            current_dir = Path(".")
            files_in_dir = list(current_dir.iterdir())
            st.markdown("**Files in current directory:**")
            for file_path in files_in_dir:
                if file_path.is_file():
                    st.write(f"• `{file_path.name}` ({file_path.stat().st_size} bytes)")
        except Exception as e:
            st.write(f"Error listing directory: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 📁 Upload Instructions")
        st.markdown("""
        **To use this app, upload the SVG files to the same stage as the application:**
        
        1. Upload these files to your Streamlit app stage:
           - `bronze_layer_er_diagram.svg`
           - `silver_layer_er_diagram.svg`
           - `gold_layer_er_diagram.svg`
           
        2. Use SnowSQL or Snowflake Web UI:
        ```bash
        PUT file://bronze_layer_er_diagram.svg @YOUR_APP_STAGE/;
        PUT file://silver_layer_er_diagram.svg @YOUR_APP_STAGE/;
        PUT file://gold_layer_er_diagram.svg @YOUR_APP_STAGE/;
        ```
        
        3. Refresh the app
        """)

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Legend")
st.sidebar.markdown("""
- **PK**: Primary Key
- **FK**: Foreign Key
- **UK**: Unique Key
""")



# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    🏗️ NASM Medallion Architecture | Local File Approach
</div>
""", unsafe_allow_html=True) 
# Simple Deployment - Local SVG Files

## Overview
This approach treats SVG files as local files deployed alongside the Streamlit app, which is much simpler and more reliable than stage-based approaches.

## Steps

### 1. Upload All Files to Your App Stage
Upload these files to the same stage where your Streamlit app is deployed:

**Required Files:**
- `nasm_architecture_app.py` (main app)
- `bronze_layer_er_diagram.svg`
- `silver_layer_er_diagram.svg`
- `gold_layer_er_diagram.svg`
- `requirements_local.txt`

### 2. Using SnowSQL
```bash
# Navigate to your project directory
cd /path/to/NASM_Architecture

# Upload all files to your app stage
PUT file://nasm_architecture_app.py @YOUR_APP_STAGE/;
PUT file://bronze_layer_er_diagram.svg @YOUR_APP_STAGE/;
PUT file://silver_layer_er_diagram.svg @YOUR_APP_STAGE/;
PUT file://gold_layer_er_diagram.svg @YOUR_APP_STAGE/;
PUT file://requirements_local.txt @YOUR_APP_STAGE/;
```

### 3. Using Snowflake Web UI
1. Navigate to **Data** > **Databases** > **[YOUR_DATABASE]** > **[YOUR_SCHEMA]** > **Stages**
2. Select your app stage
3. Upload all 5 files:
   - `nasm_architecture_app.py`
   - `bronze_layer_er_diagram.svg`
   - `silver_layer_er_diagram.svg`
   - `gold_layer_er_diagram.svg`
   - `requirements_local.txt`

### 4. Create/Update Streamlit App
```sql
CREATE OR REPLACE STREAMLIT NASM_ARCHITECTURE_VIEWER
ROOT_LOCATION = '@YOUR_APP_STAGE/'
MAIN_FILE = 'nasm_architecture_app.py'
COMMENT = 'NASM Architecture Viewer with Local SVG Files';
```

### 5. Verify Files
The app includes debugging features to verify files are uploaded correctly:
- Check the sidebar "File Debug" section
- Use "📁 List Local Files" button
- Use "🔍 Check SVG Files" button

## How It Works
- SVG files are deployed alongside the Python app
- App reads SVG files using standard `Path()` and `open()` operations
- No complex stage queries or presigned URLs needed
- Simple, reliable, and fast

## Troubleshooting

### Files Not Found
1. Verify all files uploaded to the same stage
2. Check file names match exactly (case sensitive)
3. Use the debug buttons in the app sidebar

### Permission Issues
- Ensure your role has access to the app stage
- Files should be uploaded to the same stage as the app

### File Content Issues
- SVG files should start with `<svg`
- Files should be valid UTF-8 encoded
- File extensions should be `.svg`

## Benefits of This Approach
✅ **Simple**: Uses standard file operations  
✅ **Reliable**: No dependency on external services  
✅ **Fast**: Files are local to the app  
✅ **Debuggable**: Easy to verify what files exist  
✅ **Secure**: Files stay within Snowflake environment 
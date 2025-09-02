# 🕰️ Time Capsule - Aerial View Generator

A powerful web application that generates AI-enhanced aerial landscape photographs for any location across different time periods, creating stunning timelapses that show how places might have looked in the past or could look in the future.

## ✨ Features

- **🌍 Interactive Coordinate Input**: Enter latitude, longitude, and altitude for any location worldwide
- **📅 Multi-Year Processing**: Generate images for multiple time periods (1850, 1950, 2000, 2020, 2050)
- **🤖 AI-Enhanced Imagery**: Uses Google's Gemini 2.5 Flash to transform satellite imagery into realistic aerial landscape photographs
- **🎬 Timelapse Creation**: Automatically creates MP4 timelapse videos from generated images
- **📱 Modern Web Interface**: Beautiful, responsive UI with year slider for easy navigation
- **⚡ Parallel Processing**: Efficient batch processing using Daft framework for high performance
- **📥 Download Support**: Direct download of individual images and timelapse videos

## 🏗️ Architecture

The project consists of several key components:

- **Flask Web Server** (`app.py`): Main web application with REST API endpoints
- **AI Image Pipeline** (`pipeline.py`): Parallel processing pipeline using Daft framework
- **Timelapse Generator** (`timelapse.py`): MP4 video creation from image sequences
- **FastAPI Server** (`main.py`): Alternative API server for direct image generation
- **Web Templates**: Modern HTML/CSS/JS frontend with interactive controls

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google AI Studio API key (Gemini)
- Mapbox access token

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd time-capsule
   ```

2. **Install dependencies**:

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:

   ```env
   # Gemini API Configuration (Google AI Studio)
   GEMINI_API_KEY=your-gemini-api-key-here

   # Mapbox Configuration
   MAPBOX_ACCESS_TOKEN=your-mapbox-access-token
   ```

4. **Run the application**:

   ```bash
   python app.py
   ```

5. **Open your browser** to `http://localhost:5001`

## 🔑 API Keys Setup

### Google AI Studio (Gemini API)

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new project or select an existing one
3. Generate an API key for Gemini 2.5 Flash
4. Add the key to your `.env` file as `GEMINI_API_KEY`

### Mapbox

1. Sign up at [Mapbox](https://www.mapbox.com/)
2. Go to your account dashboard
3. Create a new access token with public scopes
4. Add the token to your `.env` file as `MAPBOX_ACCESS_TOKEN`

## 📖 Usage

### Web Interface

1. **Enter Coordinates**: Input latitude, longitude, and altitude for your desired location
2. **Process Location**: Click "Generate Time Series" to create images for all time periods
3. **Explore Timeline**: Use the year slider to navigate through different time periods
4. **Create Timelapse**: Click "Create MP4 Timelapse" to generate a video
5. **Download Content**: Download individual images or the complete timelapse video

### API Endpoints

#### Web Application (Flask - Port 5001)

- `GET /` - Main web interface
- `POST /process` - Process coordinates for multiple years
- `GET /results/<batch_id>` - View results with year slider
- `GET /api/get_image/<batch_id>/<year>` - Get specific year image
- `GET /api/create_timelapse/<batch_id>` - Create MP4 timelapse
- `GET /download/<path:filename>` - Download generated files

#### Direct API (FastAPI - Port 8000)

- `POST /get-aerial-view` - Get basic satellite image
- `POST /generate-enhanced-aerial-view` - Generate AI-enhanced aerial view
- `GET /health` - API health check

### Example API Usage

```python
import requests

# Generate enhanced aerial view
response = requests.post("http://localhost:8000/generate-enhanced-aerial-view", json={
    "latitude": 37.7749,
    "longitude": -122.4194,
    "year": 2020,
    "altitude": 1000,
    "zoom": 15,
    "width": 512,
    "height": 512
})

# Save the image
with open("aerial_view.jpg", "wb") as f:
    f.write(response.content)
```

## 🏃‍♂️ Running Different Servers

### Web Application (Recommended)

```bash
python app.py
# Access at http://localhost:5001
```

### Direct API Server

```bash
python main.py
# Access at http://localhost:8000
```

### Pipeline Testing

```bash
python pipeline.py
# Runs sample data through the processing pipeline
```

## 📁 Project Structure

```
time-capsule/
├── app.py                 # Main Flask web application
├── main.py               # FastAPI server for direct API access
├── pipeline.py           # Daft-based parallel processing pipeline
├── timelapse.py          # MP4 video generation utilities
├── ui.py                 # Additional UI utilities (placeholder)
├── templates/            # HTML templates
│   ├── index.html        # Main coordinate input page
│   └── results.html      # Results viewer with year slider
├── output/               # Generated images and videos (gitignored)
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project configuration
├── uv.lock              # UV lock file
├── .env.example         # Environment variables template
└── .gitignore           # Git ignore rules
```

## 🛠️ Technical Details

### Image Processing Pipeline

1. **Satellite Image Retrieval**: Fetches high-resolution satellite imagery from Mapbox
2. **AI Enhancement**: Uses Google's Gemini 2.5 Flash to transform satellite images into realistic aerial landscape photographs
3. **Batch Processing**: Processes multiple years in parallel using the Daft framework
4. **File Management**: Organizes outputs by batch ID for easy retrieval

### Timelapse Generation

- **Format**: MP4 videos with H.264 encoding
- **Frame Rate**: 1 FPS with 2-second duration per image
- **Overlays**: Year labels added to each frame
- **Quality**: High-quality output suitable for presentations

### Performance Features

- **Parallel Processing**: Utilizes multiple CPU cores via Daft framework
- **Efficient Caching**: Batch-based organization prevents duplicate processing
- **Streaming Downloads**: Large files served efficiently
- **Error Handling**: Graceful fallbacks for failed image generation

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google AI Studio API key
- `MAPBOX_ACCESS_TOKEN`: Your Mapbox access token

### Customizable Parameters

- **Years**: Modify the years list in `app.py` (default: 1850, 1950, 2000, 2020, 2050)
- **Image Size**: Adjust width/height in pipeline (default: 512x512)
- **Video Settings**: Modify FPS and duration in `timelapse.py`
- **Zoom Level**: Change Mapbox zoom level (default: 14-15)

## 🚨 Troubleshooting

### Common Issues

1. **API Key Errors**:

   - Ensure your `.env` file contains valid API keys
   - Check that Gemini API key has sufficient quota
   - Verify Mapbox token has required scopes

2. **Image Generation Failures**:

   - Check API quotas and rate limits
   - Verify coordinates are valid (latitude: -90 to 90, longitude: -180 to 180)
   - Review server logs for detailed error messages

3. **Video Creation Issues**:

   - Ensure OpenCV is properly installed
   - Check that all required images exist in the batch directory
   - Verify sufficient disk space for video output

4. **Performance Issues**:
   - Monitor system resources during batch processing
   - Consider reducing batch sizes for memory-constrained systems
   - Check network connectivity for API calls

### Debug Mode

Run with debug logging:

```bash
export FLASK_DEBUG=1
python app.py
```

## 📊 Dependencies

### Core Frameworks

- **Flask**: Web application framework
- **FastAPI**: Alternative API framework
- **Daft**: High-performance dataframe library for parallel processing
- **Pandas**: Data manipulation and analysis

### AI & Image Processing

- **google-generativeai**: Google's Gemini API client
- **Pillow**: Python Imaging Library
- **OpenCV**: Computer vision and video processing
- **imageio**: Image and video I/O

### Web & Networking

- **requests**: HTTP library
- **uvicorn**: ASGI server
- **python-multipart**: Form data parsing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI Studio** for providing the Gemini 2.5 Flash API
- **Mapbox** for high-quality satellite imagery
- **Daft Framework** for efficient parallel processing
- **OpenCV** for video processing capabilities

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review the server logs for error details
3. Ensure all API keys are properly configured
4. Verify your internet connection for API calls

---

**Made with ❤️ for exploring the world across time**

# 🚀 Project Evaluation MVP

A modern web application that uses **Azure OpenAI GPT-4o** for intelligent document analysis and project evaluation. Upload project documents (images) and get AI-powered evaluation scores with detailed feedback.

## ✨ Features

- 📄 **Smart OCR**: Extract text from images using GPT-4o vision capabilities
- 🤖 **AI Project Evaluation**: Get scores for Innovation, Feasibility, and Market Potential
- 📊 **Detailed Analysis**: Receive justifications and actionable feedback for each score
- 🎨 **Modern UI**: Clean, responsive interface with drag-and-drop file upload
- ⚡ **Fast Processing**: Optimized for quick analysis and results

## 🎯 Live Demo

🌐 **Try it now**: [Live Demo Link](https://your-app-url-here.com) *(No setup required!)*

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python) with async support
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI Services**: Azure OpenAI GPT-4o (Vision + Chat Completion)
- **File Processing**: Supports JPEG, PNG, GIF, BMP, TIFF images

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed on your system
- **Azure OpenAI account** with GPT-4o deployment
- **Git** for cloning the repository

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/project-evaluation-mvp.git
   cd project-evaluation-mvp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env with your Azure OpenAI credentials
   # Use your favorite text editor (nano, vim, code, etc.)
   nano .env
   ```

4. **Add your Azure OpenAI credentials to .env:**
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_KEY=your-actual-api-key
   DEPLOYMENT_NAME=gpt-4o
   API_VERSION=2024-02-15-preview
   ```

5. **Run the application**
   ```bash
   python backend/main.py
   ```

6. **Access the application**
   
   Open your browser and navigate to: `http://localhost:8000`

## 🔧 Azure OpenAI Setup

### Step 1: Create Azure OpenAI Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new **Azure OpenAI** resource
3. Choose your preferred region and pricing tier

### Step 2: Deploy GPT-4o Model

1. Open **Azure OpenAI Studio**
2. Go to **Deployments** → **Create new deployment**
3. Select **GPT-4o** model
4. Name your deployment (e.g., "gpt-4o")
5. Deploy the model

### Step 3: Get Credentials

1. In Azure Portal, go to your OpenAI resource
2. Navigate to **Keys and Endpoint**
3. Copy the **Endpoint** and **Key 1**
4. Note your **deployment name** from Azure OpenAI Studio

## 📁 Project Structure

```
project-evaluation-mvp/
├── 📁 backend/
│   └── main.py              # FastAPI application with OCR and evaluation logic
├── 📁 frontend/
│   └── index.html           # Single-page application with modern UI
├── 📄 requirements.txt      # Python dependencies
├── 📄 env.example          # Environment variables template
├── 📄 .gitignore           # Git ignore rules (protects sensitive files)
├── 📄 README.md            # This file
└── 📄 .env                 # Your credentials (not included in repo)
```

## 🎯 How It Works

1. **Upload**: Drag and drop or select an image containing project details
2. **OCR Processing**: GPT-4o vision model extracts text from the image
3. **AI Analysis**: GPT-4o evaluates the project across three dimensions:
   - 💡 **Innovation** (0-10): Uniqueness and novelty of the idea
   - ⚙️ **Feasibility** (0-10): Technical and practical viability
   - 📈 **Market Potential** (0-10): Commercial opportunity and demand
4. **Results**: View detailed scores, justifications, and overall feedback

## 🔒 Security & Privacy

- ✅ Environment variables protect your API keys
- ✅ Temporary file processing (files deleted after analysis)
- ✅ No data storage or logging of sensitive information
- ✅ CORS configuration for secure client-server communication

## 🚨 Important Notes

### Cost Management
- Each image analysis uses Azure OpenAI tokens
- Monitor your Azure OpenAI usage in the Azure Portal
- Consider setting up billing alerts

### File Requirements
- **Supported formats**: JPEG, PNG, GIF, BMP, TIFF
- **Maximum file size**: 10MB
- **Image quality**: Higher quality images = better OCR results

### Limitations
- PDF support is planned for future releases
- Current implementation optimized for English text
- Requires stable internet connection for API calls

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the frontend application |
| `/upload-and-evaluate` | POST | Main endpoint for file upload and analysis |
| `/health` | GET | Health check endpoint |

## 🐛 Troubleshooting

### Common Issues

**"Failed to process file"**
- Check your Azure OpenAI credentials in `.env`
- Ensure your endpoint has a trailing slash (`/`)
- Verify your GPT-4o deployment is active

**"CORS Error"**
- Make sure you're accessing via `http://localhost:8000`
- Check that the backend is running

**"No text extracted"**
- Ensure image contains readable text
- Try higher quality/resolution images
- Check that text is in a supported language

### Debug Mode

Run with detailed logging:
```bash
python backend/main.py
```
Check console output for detailed error messages.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload for development
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Azure OpenAI** for providing powerful AI capabilities
- **FastAPI** for the excellent web framework
- **OpenAI** for the GPT-4o model architecture

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/project-evaluation-mvp/issues) page
2. Create a new issue with detailed description
3. Include error messages and environment details

---

## 🌟 Star this repository if you find it useful!

**Made with ❤️ using Azure OpenAI GPT-4o** 
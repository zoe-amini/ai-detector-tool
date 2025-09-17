# Candidate Submission Analysis Tool

A minimal HTTP server that allows users to upload job candidate submissions and automatically analyzes the contents for readability, AI detection, and automated evaluation. The server uses only Python standard library modules, making it suitable for environments without access to external packages.

## Quick Start

### Prerequisites
- Python 3.6 or higher
- (Optional) `pdftotext` utility for PDF analysis

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd candidate_tool
   ```

2. **Install optional PDF support** (recommended)
   ```bash
   # macOS
   brew install poppler
   
   # Ubuntu/Debian
   sudo apt-get install poppler-utils
   
   # CentOS/RHEL
   sudo yum install poppler-utils
   ```

3. **Run the application**
   ```bash
   python3 app.py
   ```

4. **Access the web interface**
   Open your browser and navigate to: `http://localhost:8000`

## Features

### Text Analysis
- **Readability Metrics**: Flesch Reading Ease score calculation
- **Lexical Analysis**: Word count, unique word ratio, sentence statistics
- **Syllable Counting**: Advanced syllable estimation using linguistic rules
- **AI Detection**: Dual-layer AI content detection using:
  - Simple heuristic based on lexical diversity and readability
  - Rigorous analysis using n-gram patterns, function word usage, and stylistic features

### File Support
- **Text Files**: `.txt`, `.md`, `.py`, `.java`, `.js`, `.c`, `.cpp`, `.json`
- **PDF Files**: `.pdf` (requires `pdftotext` utility)
- **Automatic Detection**: File type recognition and appropriate processing

### Automated Evaluation
- **Python Autopilot**: Automatic testing of Python submissions
- **Test Framework**: Built-in test cases for candidate solutions
- **Safe Execution**: Controlled environment for code evaluation
- **Detailed Feedback**: Comprehensive test results and error reporting

### Web Interface
- **File Upload**: Drag-and-drop or browse file selection
- **Real-time Analysis**: Instant processing and results display
- **Responsive Design**: Works on desktop and mobile devices
- **Results Dashboard**: Comprehensive metrics visualization

## Technical Details

### Architecture
- **Pure Python**: No external dependencies required
- **Standard Library**: Uses only built-in Python modules
- **HTTP Server**: Built-in `http.server` for web interface
- **Modular Design**: Separate analysis logic in `utils.py`

### Security Features
- **File Validation**: Safe filename handling and path sanitization
- **Sandboxed Execution**: Controlled environment for code evaluation
- **Error Handling**: Comprehensive exception management
- **Resource Limits**: Memory-efficient file processing

### Performance
- **Chunked Processing**: Large file handling without memory issues
- **Efficient Algorithms**: Optimized text analysis algorithms
- **Minimal Overhead**: Lightweight server implementation

## Potential Roadmap

### Short Term (v1.1)
- [ ] **Enhanced File Support**
  - Microsoft Word documents (`.docx`)
  - Rich Text Format (`.rtf`)
  - Markdown with syntax highlighting
- [ ] **Improved UI/UX**
  - Better responsive design
  - Progress indicators for large files
  - Dark mode support
- [ ] **Export Features**
  - PDF report generation
  - CSV data export
  - JSON API endpoints

### Medium Term (v1.2)
- [ ] **Advanced AI Detection**
  - Integration with external AI detection APIs
  - Machine learning model training
  - Confidence scoring improvements
- [ ] **Batch Processing**
  - Multiple file upload
  - Bulk analysis capabilities
  - Queue management system
- [ ] **User Management**
  - Authentication system
  - User profiles and history
  - Role-based access control

### Long Term (v2.0)
- [ ] **Cloud Deployment**
  - Docker containerization
  - Kubernetes deployment
  - Auto-scaling capabilities
- [ ] **Advanced Analytics**
  - Historical trend analysis
  - Comparative benchmarking
  - Custom metric definitions
- [ ] **Integration APIs**
  - RESTful API for external systems
  - Webhook notifications
  - Third-party service integrations

## Configuration

### Environment Variables
```bash
# Server configuration
export SERVER_HOST=0.0.0.0
export SERVER_PORT=8000

# File upload limits
export MAX_FILE_SIZE=10485760  # 10MB
export UPLOAD_DIR=./uploads

# Analysis settings
export ENABLE_PDF_ANALYSIS=true
export ENABLE_AUTOPILOT=true
```

### Customization
- Modify `utils.py` for custom analysis algorithms
- Update `templates/` for UI customization
- Configure server settings in `app.py`

## Troubleshooting

### Common Issues

**Port already in use**
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
```

**PDF analysis not working**
```bash
# Verify pdftotext installation
which pdftotext
# Should return: /opt/homebrew/bin/pdftotext (or similar)
```

**Permission errors**
```bash
# Ensure uploads directory is writable
chmod 755 uploads/
```

### Error Messages
- `TypeError: Cannot be converted to bool.` - Fixed in current version
- `No file uploaded.` - Check file selection and form submission
- `File type not supported` - Verify file extension is supported

## API Reference

### Endpoints
- `GET /` - Main upload interface
- `POST /upload` - File upload and analysis
- `GET /uploads/<filename>` - Download uploaded files
- `GET /static/<file>` - Static assets

### Response Format
```json
{
  "filename": "submission.txt",
  "word_count": 150,
  "unique_word_count": 120,
  "unique_ratio": 0.80,
  "sentence_count": 8,
  "avg_sentence_length": 18.75,
  "syllable_count": 225,
  "flesch_reading_ease": 65.5,
  "ai_likelihood": 0.15,
  "ai_rigorous_score": 0.12,
  "autopilot_result": "All tests passed successfully."
}
```

## Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd candidate_tool

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run tests
python3 -m pytest tests/

# Run with debug mode
python3 app.py --debug
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- Commercial use
- Modification
- Distribution
- Private use
- No warranty or liability

## Credits

### Author
Zoe C.

### Acknowledgments
- **Flesch Reading Ease Formula** - Rudolf Flesch (1948)
- **Syllable Counting Algorithm** - Based on linguistic research and standard methods
- **AI Detection Heuristics** - Inspired by academic research on machine-generated text detection
- **Python Standard Library** - For providing robust, dependency-free functionality

### Open Source Libraries
This project intentionally uses only Python standard library modules to ensure:
- Zero external dependencies
- Maximum compatibility
- Easy deployment
- Reduced security surface

### Research References
- Flesch, R. (1948). "A new readability yardstick." Journal of Applied Psychology
- Linguistic syllable counting methods and vowel cluster analysis
- Academic papers on AI-generated text detection and analysis

## Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check this README and inline code comments
- **Community**: Join discussions in GitHub Discussions

---

**Made with care for the developer community**

*This tool is designed to be simple, reliable, and dependency-free. Perfect for technical interviews, code reviews, and educational purposes.*

# CodeSensei 🥋 - Smart Learning IDE

An AI-powered Python learning IDE that detects performance issues, explains errors in beginner-friendly language, and teaches optimization techniques through interactive examples.

![CodeSensei Banner](https://img.shields.io/badge/Python-Learning%20IDE-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-Sandboxed-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Hackathon%20Ready-orange?style=for-the-badge)

## 🌟 Features

### 🔒 **Secure Sandboxed Execution**
- RestrictedPython-based sandbox prevents malicious code
- No file system access or dangerous imports
- Safe for educational environments

### 🧠 **Intelligent Code Analysis**
- **Nested Loop Detection**: Identifies O(n²) and higher complexity
- **List Lookup Optimization**: Suggests converting lists to sets
- **String Concatenation**: Recommends efficient join() operations
- **List Comprehensions**: Suggests Pythonic alternatives to loops
- **Recursion Safety**: Warns about potential stack overflow

### 💬 **Beginner-Friendly Error Messages**
- Translates cryptic Python errors into plain English
- Shows exact line numbers
- Provides actionable suggestions
- Advanced mode for experienced developers

### ⚡ **Real-Time Performance Feedback**
- Before/after code examples
- Time complexity explanations
- Best practice recommendations
- Visual severity indicators

### 🎨 **Modern UI/UX**
- Monaco Editor (VSCode engine)
- Responsive design
- Dark theme optimized for coding
- Keyboard shortcuts (Ctrl+Enter to run)
- Loading states and animations

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
Modern web browser
```

### Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install Flask flask-cors RestrictedPython
```

2. **Start Backend Server**
```bash
python backend.py
```

You should see:
```
🚀 Smart Learning IDE Backend Starting...
⚠️  This is a sandboxed environment for educational purposes
📍 Running on http://127.0.0.1:5000
```

3. **Open Frontend**
```bash
# Simply open index.html in your browser
# Or use a local server:
python -m http.server 8000
# Then visit: http://localhost:8000
```

## 📖 Usage Guide

### Running Code
1. Write Python code in the editor
2. Click **"Run Code"** or press `Ctrl+Enter`
3. View output in the console

### Analyzing Performance
1. Write or paste Python code
2. Click **"Analyze Performance"**
3. Review suggestions with examples
4. Toggle **Advanced Mode** for technical details

### Example: Finding Duplicates
```python
# CodeSensei will detect this inefficient code:
def find_duplicates(data):
    duplicates = []
    for item in data:
        if data.count(item) > 1:  # O(n²) - Slow!
            if item not in duplicates:
                duplicates.append(item)
    return duplicates

# And suggest this optimized version:
def find_duplicates_fast(data):
    seen = set()
    duplicates = set()
    for item in data:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

## 🏗️ Architecture

### Backend (`backend.py`)
- **Flask API**: RESTful endpoints for code execution and analysis
- **RestrictedPython**: Sandboxed execution environment
- **AST Analysis**: Deep code parsing for performance detection
- **Error Handler**: Intelligent error categorization

### Frontend (`index.html`)
- **Monaco Editor**: Professional code editor
- **Responsive UI**: Modern, accessible interface
- **Real-time Updates**: Async API communication
- **Error Recovery**: Graceful fallbacks

## 🔐 Security Features

### What's Protected
✅ File system access blocked  
✅ Network operations disabled  
✅ Dangerous imports prevented (os, subprocess, sys)  
✅ eval/exec usage restricted  
✅ Input validation and sanitization  
✅ Execution timeout (3 seconds)  
✅ Code length limits (10,000 chars)  

### What's Allowed
✅ Basic Python syntax  
✅ Data structures (lists, dicts, sets)  
✅ Math operations  
✅ String manipulation  
✅ Control flow (loops, conditionals)  
✅ Function definitions  

## 🎯 Hackathon Presentation Tips

### Demo Flow (5 minutes)
1. **Introduction** (30s)
   - "We built CodeSensei to help students learn efficient Python programming"
   
2. **Problem Statement** (30s)
   - "Students often write working code that's inefficient"
   - "Error messages are confusing for beginners"
   
3. **Live Demo** (3 minutes)
   - Show nested loop detection
   - Demonstrate error explanation
   - Run before/after performance comparison
   - Toggle Advanced Mode
   
4. **Technical Highlights** (1 minute)
   - Sandboxed execution
   - AST-based analysis
   - Real-time feedback
   
5. **Future Vision** (30s)
   - Integration with online learning platforms
   - Support for more languages
   - AI-powered personalized hints

### Key Talking Points
- **Educational Value**: Teaches optimization, not just syntax
- **Safety First**: Secure sandbox for classroom use
- **User Experience**: Beginner-friendly with expert mode
- **Scalability**: API-based architecture for easy integration

### Demo Code Examples

**Example 1: Nested Loops**
```python
# This will trigger optimization suggestions
numbers = [1, 2, 3, 4, 5]
squares = [6, 7, 8, 9, 10]

for num in numbers:
    for sq in squares:
        if num * num == sq:
            print(f"{num}² = {sq}")
```

**Example 2: List Lookup**
```python
# Shows list vs. set performance
search_items = ['apple', 'banana', 'orange']
inventory = ['apple', 'grape', 'banana', 'kiwi']

for item in inventory:
    if item in search_items:  # Inefficient!
        print(f"Found: {item}")
```

**Example 3: Error Handling**
```python
# Shows beginner-friendly error messages
numbers = [1, 2, 3]
print(numbers[5])  # IndexError explained clearly
```

## 🛠️ API Reference

### POST `/run`
Execute Python code in sandbox.

**Request:**
```json
{
  "code": "print('Hello, World!')"
}
```

**Response (Success):**
```json
{
  "success": true,
  "output": "Hello, World!\n"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error_type": "NameError",
  "message": "You're using a variable that hasn't been defined yet.",
  "line": 3
}
```

### POST `/analyze`
Analyze code for performance issues.

**Request:**
```json
{
  "code": "for i in range(10):\n    for j in range(10):\n        print(i, j)"
}
```

**Response:**
```json
{
  "status": "optimization_possible",
  "issue": {
    "type": "nested_loops",
    "severity": "high",
    "title": "Deeply Nested Loops Detected",
    "description": "Your code has 2 nested loops...",
    "explanation": "Nested loops increase time complexity...",
    "suggestion": "Consider using data structures..."
  },
  "examples": {
    "before": "...",
    "after": "..."
  }
}
```

## 📊 Technical Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask (Python) |
| Security | RestrictedPython |
| Code Analysis | Python AST |
| Editor | Monaco Editor |
| Frontend | HTML5, CSS3, Vanilla JS |
| API | RESTful JSON |

## 🔄 Future Enhancements

- [ ] Support for more languages (JavaScript, Java, C++)
- [ ] Integration with LMS platforms (Canvas, Moodle)
- [ ] Code complexity visualization graphs
- [ ] Student progress tracking
- [ ] Teacher dashboard
- [ ] Custom test case creation
- [ ] Code sharing and collaboration
- [ ] Mobile app version
- [ ] AI-powered hint system
- [ ] Gamification (badges, leaderboards)

## 🐛 Known Limitations

- **Execution Time**: Limited to 3 seconds (configurable)
- **Code Size**: Max 10,000 characters
- **Libraries**: Only built-in Python modules
- **Concurrency**: Single-threaded execution
- **Storage**: No persistent data storage

## 📝 License

MIT License - Feel free to use for educational purposes!

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 👥 Team

Built with ❤️ for computer science education

## 🙏 Acknowledgments

- Monaco Editor team for the amazing code editor
- Flask community for excellent documentation
- RestrictedPython for secure execution
- All the educators who inspired this project

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Email: your-email@example.com
- Discord: YourServer

---

**Made for Tech Hackathon 2026** 🚀

*"Making Python learning smarter, safer, and more fun!"*

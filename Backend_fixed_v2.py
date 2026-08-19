from flask import Flask, request, jsonify
import ast
import io
import sys
import traceback
from contextlib import redirect_stdout, redirect_stderr
import time
import re
import json
import os
import datetime

app = Flask(__name__)

# Simple CORS handling
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# ==================== CONSTANTS ====================
MAX_CODE_LENGTH = 10000
MAX_NESTED_LOOPS = 2
MAX_EXECUTION_TIME = 10  # Increased to allow performance comparisons

# ==================== SAFE EXECUTION ====================

def execute_code_safely(code: str) -> dict:
    """Execute Python code with basic safety measures"""
    
    # Block dangerous patterns
    dangerous = ['import os', 'import subprocess', 'import sys',
                 'eval(', 'exec(', 'compile(', 'open(', 'file(']
    
    code_lower = code.lower()
    for pattern in dangerous:
        if pattern in code_lower:
            return {
                "success": False,
                "error_type": "SecurityError",
                "message": f"For security, '{pattern}' is not allowed",
                "line": None
            }
    
    # Capture output
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()
    
    try:
        # Create restricted globals with safe modules
        import time as time_module
        import math as math_module
        import random as random_module
        
        # Safe import function that only allows specific modules
        def safe_import(name, *args, **kwargs):
            allowed_modules = {'time', 'math', 'random', 'itertools', 'collections', 'functools'}
            if name in allowed_modules:
                return __import__(name, *args, **kwargs)
            raise ImportError(f"Module '{name}' is not allowed for security reasons")
        
        safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'bool': bool,
                'min': min,
                'max': max,
                'sum': sum,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'all': all,
                'any': any,
                'True': True,
                'False': False,
                'None': None,
                '__import__': safe_import,
            },
            'time': time_module,
            'math': math_module,
            'random': random_module,
        }
        
        start_time = time.time()
        
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            exec(code, safe_globals)
            
            if time.time() - start_time > MAX_EXECUTION_TIME:
                return {
                    "success": False,
                    "error_type": "TimeoutError",
                    "message": "Code took too long to run (>10 seconds)",
                    "line": None
                }
        
        output = output_buffer.getvalue()
        errors = error_buffer.getvalue()
        
        if errors:
            return {
                "success": False,
                "error_type": "RuntimeError",
                "message": errors,
                "line": None
            }
        
        return {
            "success": True,
            "output": output or "✓ Program completed (no output)"
        }
        
    except Exception as e:
        return parse_runtime_error(traceback.format_exc(), str(e))

def parse_runtime_error(tb: str, error_msg: str) -> dict:
    """Parse runtime errors"""
    line_num = None
    
    # Extract line number
    for line in tb.split('\n'):
        match = re.search(r'line (\d+)', line)
        if match:
            line_num = int(match.group(1))
            break
    
    # Categorize error
    if "NameError" in error_msg:
        error_type = "NameError"
        friendly = "You're using a variable that hasn't been defined."
    elif "TypeError" in error_msg:
        error_type = "TypeError"
        friendly = "There's a type mismatch (e.g., adding string + number)."
    elif "IndexError" in error_msg:
        error_type = "IndexError"
        friendly = "You're accessing an index that doesn't exist."
    elif "ZeroDivisionError" in error_msg:
        error_type = "ZeroDivisionError"
        friendly = "You're dividing by zero."
    elif "KeyError" in error_msg:
        error_type = "KeyError"
        friendly = "Dictionary key doesn't exist."
    elif "ValueError" in error_msg:
        error_type = "ValueError"
        friendly = "Invalid value for the operation."
    elif "AttributeError" in error_msg:
        error_type = "AttributeError"
        friendly = "Object doesn't have that attribute/method."
    else:
        error_type = "RuntimeError"
        friendly = error_msg
    
    return {
        "success": False,
        "error_type": error_type,
        "message": friendly,
        "line": line_num,
        "raw_error": error_msg
    }

# ==================== CODE ANALYZER ====================

class PerformanceAnalyzer(ast.NodeVisitor):
    """Analyze code for performance issues"""
    
    def __init__(self):
        self.loop_depth = 0
        self.max_loop_depth = 0
        self.list_lookups = []
        self.string_concats = []
        self.list_appends = []
        self.recursion = []
        self.current_function = None
        self.function_calls = {}
    
    def visit_For(self, node):
        self.loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.loop_depth)
        self.generic_visit(node)
        self.loop_depth -= 1
    
    def visit_While(self, node):
        self.visit_For(node)
    
    def visit_Compare(self, node):
        if self.loop_depth > 0:
            for op in node.ops:
                if isinstance(op, ast.In):
                    self.list_lookups.append({"line": node.lineno})
        self.generic_visit(node)
    
    def visit_AugAssign(self, node):
        if self.loop_depth > 0 and isinstance(node.op, ast.Add):
            self.string_concats.append({"line": node.lineno})
        self.generic_visit(node)
    
    def visit_Expr(self, node):
        if self.loop_depth > 0 and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if node.value.func.attr == 'append':
                    self.list_appends.append({"line": node.lineno})
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        old_func = self.current_function
        self.current_function = node.name
        self.function_calls[node.name] = []
        self.generic_visit(node)
        
        if node.name in self.function_calls[node.name]:
            self.recursion.append({"name": node.name, "line": node.lineno})
        
        self.current_function = old_func
    
    def visit_Call(self, node):
        if self.current_function and isinstance(node.func, ast.Name):
            self.function_calls[self.current_function].append(node.func.id)
        self.generic_visit(node)

def analyze_code_performance(code: str) -> dict:
    """Analyze code for performance"""
    try:
        tree = ast.parse(code)
        analyzer = PerformanceAnalyzer()
        analyzer.visit(tree)
        
        # Find primary issue
        if analyzer.max_loop_depth >= MAX_NESTED_LOOPS:
            issue = {
                "type": "nested_loops",
                "severity": "high",
                "line": None,
                "title": "Deeply Nested Loops Detected",
                "description": f"Your code has {analyzer.max_loop_depth} nested loops.",
                "explanation": "Nested loops multiply operations. Two nested loops = O(n²) complexity, which gets slow with large data.",
                "suggestion": "Try using sets, dictionaries, or restructure your algorithm to avoid nesting."
            }
            examples = {
                "before": "# Slow: O(n²)\nfor item in list1:\n    for check in list2:\n        if item == check:\n            print(item)",
                "after": "# Fast: O(n)\nset2 = set(list2)\nfor item in list1:\n    if item in set2:\n        print(item)"
            }
        elif analyzer.list_lookups:
            issue = {
                "type": "list_lookup",
                "severity": "medium",
                "line": analyzer.list_lookups[0]["line"],
                "title": "Inefficient List Membership Check",
                "description": "Checking 'if item in list' inside a loop is slow.",
                "explanation": "List lookups are O(n). In a loop, this becomes O(n²) or worse.",
                "suggestion": "Convert your list to a set before the loop. Sets have O(1) lookups!"
            }
            examples = {
                "before": "# Slow\nsearch_list = [1, 2, 3]\nfor item in data:\n    if item in search_list:\n        print(item)",
                "after": "# Fast\nsearch_set = {1, 2, 3}\nfor item in data:\n    if item in search_set:\n        print(item)"
            }
        elif analyzer.string_concats:
            issue = {
                "type": "string_concat",
                "severity": "low",
                "line": analyzer.string_concats[0]["line"],
                "title": "Repeated String Concatenation",
                "description": "Building strings with += creates unnecessary copies.",
                "explanation": "Each += creates a new string in memory.",
                "suggestion": "Use a list and join: ''.join(string_list)"
            }
            examples = {
                "before": "# Inefficient\nresult = ''\nfor word in words:\n    result += word + ' '",
                "after": "# Efficient\nresult = ' '.join(words)"
            }
        elif analyzer.list_appends:
            issue = {
                "type": "list_append",
                "severity": "low",
                "line": analyzer.list_appends[0]["line"],
                "title": "Loop with List Append",
                "description": "Consider using a list comprehension.",
                "explanation": "List comprehensions are faster and more Pythonic.",
                "suggestion": "Try: result = [transform(x) for x in items]"
            }
            examples = {
                "before": "# Traditional\nresult = []\nfor x in items:\n    result.append(x * 2)",
                "after": "# List comprehension\nresult = [x * 2 for x in items]"
            }
        elif analyzer.recursion:
            issue = {
                "type": "recursion",
                "severity": "medium",
                "line": analyzer.recursion[0]["line"],
                "title": "Recursive Function Detected",
                "description": f"Function '{analyzer.recursion[0]['name']}' calls itself.",
                "explanation": "Recursion can cause stack overflow without a proper base case.",
                "suggestion": "Verify your base case is reachable."
            }
            examples = {
                "before": "# Recursive\ndef factorial(n):\n    return n * factorial(n-1)",
                "after": "# Iterative\ndef factorial(n):\n    result = 1\n    for i in range(1, n+1):\n        result *= i\n    return result"
            }
        else:
            return {
                "status": "looks_good",
                "message": "No obvious performance issues detected!"
            }
        
        return {
            "status": "optimization_possible",
            "issue": issue,
            "examples": examples
        }
        
    except SyntaxError as e:
        return {
            "status": "error",
            "error_type": "SyntaxError",
            "message": "Syntax error in your code. Check colons, brackets, indentation.",
            "line": e.lineno
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": "AnalysisError",
            "message": f"Could not analyze: {str(e)}",
            "line": None
        }

# ==================== COMMUNITY DATA ====================
COMMUNITY_FILE = 'community_snippets.json'

def load_community_snippets():
    if not os.path.exists(COMMUNITY_FILE):
        return []
    try:
        with open(COMMUNITY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_community_snippet(snippet):
    snippets = load_community_snippets()
    # Add timestamp and id
    snippet['id'] = len(snippets) + 1
    snippet['timestamp'] = datetime.datetime.now().isoformat()
    snippets.insert(0, snippet) # Add to top
    # Keep last 50
    snippets = snippets[:50]

    with open(COMMUNITY_FILE, 'w', encoding='utf-8') as f:
        json.dump(snippets, f, indent=2)
    return snippet

@app.route("/format", methods=["POST", "OPTIONS"])
def format_code():
    if request.method == "OPTIONS":
        return "", 204

    code = request.json.get("code", "")

    if not code.strip():
        return jsonify({"error": "Empty code"}), 400

    try:
        # Use AST to parse and unparse (auto-format)
        parsed = ast.parse(code)
        formatted = ast.unparse(parsed)
        return jsonify({"success": True, "code": formatted})
    except SyntaxError as e:
        return jsonify({
            "success": False,
            "error": "Syntax Error",
            "message": "Cannot format invalid code. Please fix syntax errors first."
        }), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/community", methods=["GET", "POST", "OPTIONS"])
def community():
    if request.method == "OPTIONS":
        return "", 204

    if request.method == "GET":
        return jsonify(load_community_snippets())

    if request.method == "POST":
        data = request.json
        if not data.get("title") or not data.get("code"):
            return jsonify({"error": "Missing title or code"}), 400

        snippet = {
            "title": data["title"],
            "code": data["code"],
            "author": data.get("author", "Anonymous"),
            "description": data.get("description", "")
        }
        saved = save_community_snippet(snippet)
        return jsonify({"success": True, "snippet": saved})

@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return "", 204
    
    code = request.json.get("code", "")
    
    if not code.strip():
        return jsonify({"error": "Empty code"}), 400
    
    if len(code) > MAX_CODE_LENGTH:
        return jsonify({"error": "Code too long"}), 400
    
    result = analyze_code_performance(code)
    return jsonify(result)

@app.route("/run", methods=["POST", "OPTIONS"])
def run():
    if request.method == "OPTIONS":
        return "", 204
    
    code = request.json.get("code", "")
    
    if not code.strip():
        return jsonify({"error": "Empty code"}), 400
    
    if len(code) > MAX_CODE_LENGTH:
        return jsonify({"error": "Code too long"}), 400
    
    result = execute_code_safely(code)
    return jsonify(result)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "version": "2.0"})

@app.route("/", methods=["GET"])
def home():
    """Serve the main HTML page for desktop app"""
    import os
    
    # Try to find and serve HTML file
    html_files = ['index_final.html', 'index_enhanced.html', 'index.html']
    for html_file in html_files:
        if os.path.exists(html_file):
            print(f'📄 Serving: {html_file}')
            with open(html_file, 'r', encoding='utf-8') as f:
                return f.read()
    
    # Return API info if no HTML found
    return jsonify({
        "message": "CodeSensei Backend API",
        "endpoints": ["/run", "/analyze", "/health"]
    })

# ==================== MAIN ====================

if __name__ == "__main__":
    print("=" * 50)
    print("CodeSensei Backend Starting...")
    print("=" * 50)
    print("Server running on: http://127.0.0.1:5000")
    print("CORS enabled for all origins")
    print("Sandboxed environment (educational use)")
    print("=" * 50)
    print("\nEndpoints:")
    print("  POST /run      - Execute Python code")
    print("  POST /analyze  - Analyze performance")
    print("  GET  /health   - Health check")
    print("\nPress Ctrl+C to stop")
    print("=" * 50)

    app.run(debug=True, host='127.0.0.1', port=5000)
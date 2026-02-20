import os
import sqlite3
from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 1. Gemini AI Setup (Key hum Render ke environment variables mein dalenge)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. SQLite Database Setup
def init_db():
    conn = sqlite3.connect('tasks.db')
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, content TEXT)')
    conn.close()

init_db()

# 3. Frontend Template (Professional Dark UI)
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <title>AI Smart Manager</title>
</head>
<body class="bg-gray-900 text-white min-h-screen flex items-center justify-center">
    <div class="w-full max-w-md p-8 bg-gray-800 rounded-2xl shadow-2xl border border-gray-700">
        <h1 class="text-3xl font-bold text-blue-400 mb-6 text-center">Smart AI Tasks</h1>
        <div class="flex gap-2 mb-6">
            <input type="text" id="taskInput" placeholder="What's on your mind?" 
                   class="flex-1 p-3 rounded-lg bg-gray-700 border-none focus:ring-2 focus:ring-blue-500">
            <button onclick="addTask()" class="bg-blue-600 px-6 py-3 rounded-lg font-bold hover:bg-blue-700">Add</button>
        </div>
        <ul id="taskList" class="space-y-3"></ul>
    </div>
    <script>
        async function loadTasks() {
            const res = await fetch('/get-tasks');
            const data = await res.json();
            document.getElementById('taskList').innerHTML = data.map(t => 
                `<li class="p-3 bg-gray-700 rounded-lg border-l-4 border-blue-500">${t.content}</li>`
            ).join('');
        }
        async function addTask() {
            const content = document.getElementById('taskInput').value;
            if(!content) return;
            await fetch('/add-task', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({content})
            });
            document.getElementById('taskInput').value = '';
            loadTasks();
        }
        loadTasks();
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/get-tasks')
def get():
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('SELECT content FROM tasks')
    tasks = [{'content': row[0]} for row in cur.fetchall()]
    conn.close()
    return jsonify(tasks)

@app.route('/add-task', methods=['POST'])
def add():
    content = request.json['content']
    # Bonus: AI checking (Optional - AI se thora feedback le sakte hain)
    conn = sqlite3.connect('tasks.db')
    conn.execute('INSERT INTO tasks (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
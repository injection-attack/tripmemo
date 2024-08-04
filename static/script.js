const API_URL = '/api/todos';
const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');

function fetchTodos() {
    fetch(API_URL)
        .then(response => response.json())
        .then(todos => {
            renderTodos(todos);
        })
        .catch(error => console.error('Fetch error:', error));
}


function renderTodos(todos) {
    todoList.innerHTML = '';
    todos.forEach((todo, index) => {
        const li = document.createElement('li');
        li.className = 'todo-item';
        li.innerHTML = `
            <span class="todo-text ${todo.completed ? 'completed' : ''}">${todo.title}</span>
            <button onclick="toggleTodo(${index})">${todo.completed ? 'Undo' : 'Complete'}</button>
            <button onclick="deleteTodo(${index})">Delete</button>
        `;
        todoList.appendChild(li);
    });
}

todoForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const title = todoInput.value;
    fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    })
    .then(response => response.json())
    .then(() => {
        todoInput.value = '';
        fetchTodos();
    })
    .catch(error => console.error('Add todo error:', error));
});

function toggleTodo(index) {
    fetch(`${API_URL}/${index}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: true })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(`HTTP error! status: ${response.status}, message: ${text}`);
            });
        }
        return response.json();
    })
    .then(updatedTodo => {
        console.log('Server response:', updatedTodo);
        fetchTodos();
    })
    .catch(error => {
        console.error('Toggle todo error:', error);
        // 사용자에게 오류 메시지 표시
        alert('Failed to update todo. Please try again.');
    });
}

function deleteTodo(index) {
    fetch(`${API_URL}/${index}`, { method: 'DELETE' })
        .then(() => fetchTodos())
        .catch(error => console.error('Delete todo error:', error));
}

fetchTodos();

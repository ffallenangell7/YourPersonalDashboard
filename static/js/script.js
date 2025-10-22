// Update date and time
function updateDateTime() {
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    document.getElementById('datetime').textContent = now.toLocaleDateString('en-US', options);
}

setInterval(updateDateTime, 1000);
updateDateTime();

// Fetch weather data
async function fetchWeather() {
    try {
        const response = await fetch('/api/weather');
        const data = await response.json();
        
        if (data.error) throw new Error(data.error);
        
        const weatherHTML = `
            <div class="weather-temp">${Math.round(data.temperature)}°C</div>
            <div class="weather-icon">${data.icon}</div>
            <div class="weather-desc">${data.description}</div>
            <div class="weather-city">${data.city}</div>
            <div class="weather-details">
                <div class="weather-detail">
                    <span>💧 Humidity</span>
                    <div class="value">${data.humidity}%</div>
                </div>
                <div class="weather-detail">
                    <span>💨 Wind</span>
                    <div class="value">${data.wind_speed} km/h</div>
                </div>
            </div>
        `;
        
        document.getElementById('weather-content').innerHTML = weatherHTML;
    } catch (error) {
        document.getElementById('weather-content').innerHTML = 
            '<div class="error">Failed to load weather</div>';
        console.error('Weather error:', error);
    }
}

// Fetch news data
async function fetchNews() {
    try {
        const response = await fetch('/api/news');
        const articles = await response.json();
        
        if (articles.error) throw new Error(articles.error);
        
        let newsHTML = '';
        articles.forEach(article => {
            newsHTML += `
                <div class="news-item">
                    <a href="${article.url}" target="_blank" class="news-title">${article.title}</a>
                    <div class="news-source">${article.source?.name || 'Unknown'}</div>
                </div>
            `;
        });
        
        document.getElementById('news-content').innerHTML = newsHTML;
    } catch (error) {
        document.getElementById('news-content').innerHTML = 
            '<div class="error">Failed to load news</div>';
        console.error('News error:', error);
    }
}

// Fetch quote
async function fetchQuote() {
    try {
        const response = await fetch('/api/quote');
        const quote = await response.json();
        
        if (quote.error) throw new Error(quote.error);
        
        const quoteHTML = `
            <div class="quote-text">"${quote.content}"</div>
            <div class="quote-author">- ${quote.author}</div>
        `;
        
        document.getElementById('quote-content').innerHTML = quoteHTML;
    } catch (error) {
        document.getElementById('quote-content').innerHTML = 
            '<div class="error">Failed to load quote</div>';
        console.error('Quote error:', error);
    }
}

// Task Management Functions
function loadTasks() {
    const tasks = JSON.parse(localStorage.getItem('dashboardTasks')) || [];
    const tasksList = document.getElementById('tasks-list');
    
    if (tasks.length === 0) {
        tasksList.innerHTML = '<div class="loading">No tasks yet. Add one above!</div>';
        return;
    }
    
    let tasksHTML = '';
    tasks.forEach((task, index) => {
        tasksHTML += `
            <div class="task-item">
                <input type="checkbox" onchange="toggleTask(${index})" ${task.completed ? 'checked' : ''}>
                <span class="task-text ${task.completed ? 'task-completed' : ''}">${task.text}</span>
                <button class="delete-btn" onclick="deleteTask(${index})">Delete</button>
            </div>
        `;
    });
    
    tasksList.innerHTML = tasksHTML;
}

function addTask() {
    const taskInput = document.getElementById('task-input');
    const text = taskInput.value.trim();
    
    if (text === '') return;
    
    const tasks = JSON.parse(localStorage.getItem('dashboardTasks')) || [];
    tasks.push({ text, completed: false });
    localStorage.setItem('dashboardTasks', JSON.stringify(tasks));
    
    taskInput.value = '';
    loadTasks();
}

function toggleTask(index) {
    const tasks = JSON.parse(localStorage.getItem('dashboardTasks')) || [];
    tasks[index].completed = !tasks[index].completed;
    localStorage.setItem('dashboardTasks', JSON.stringify(tasks));
    loadTasks();
}

function deleteTask(index) {
    const tasks = JSON.parse(localStorage.getItem('dashboardTasks')) || [];
    tasks.splice(index, 1);
    localStorage.setItem('dashboardTasks', JSON.stringify(tasks));
    loadTasks();
}

// Handle Enter key in task input
document.getElementById('task-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTask();
    }
});

// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', function() {
    fetchWeather();
    fetchNews();
    fetchQuote();
    loadTasks();
    
    // Refresh data every 10 minutes
    setInterval(() => {
        fetchWeather();
        fetchNews();
        fetchQuote();
    }, 600000);
});
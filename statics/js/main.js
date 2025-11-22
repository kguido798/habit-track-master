// Load habits
async function loadHabits() {
    const res = await fetch("/api/habits");
    const habits = await res.json();
    const tbody = document.querySelector("#habitTable tbody");
    tbody.innerHTML = "";

    habits.forEach(h => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${h.name}</td>
            <td>${h.frequency}</td>
            <td>${h.streak}</td>
            <td>
                <button onclick="updateStreak(${h.id}, ${h.streak}, '${h.name}', '${h.frequency}')">+1 Streak</button>
                <button onclick="deleteHabit(${h.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Add habit
async function addHabit() {
    const name = document.getElementById("habitName").value.trim();
    const frequency = document.getElementById("frequency").value;

    if (!name) {
        alert("Enter a habit name");
        return;
    }

    await fetch("/api/habits", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, frequency })
    });

    document.getElementById("habitName").value = "";
    loadHabits();
}

// Update streak
async function updateStreak(id, streak, name, frequency) {
    await fetch("/api/habits", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id,
            name,
            frequency,
            streak: streak + 1
        })
    });

    loadHabits();
}

// Delete habit
async function deleteHabit(id) {
    await fetch("/api/habits", {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    });

    loadHabits();
}

// Load quote
async function loadQuote() {
    const res = await fetch("/api/quote");
    const data = await res.json();
    document.getElementById("quote").textContent = `"${data.quote}"`;
    document.getElementById("quoteAuthor").textContent = `- ${data.author}`;
}

// First load
loadHabits();
loadQuote();

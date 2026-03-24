// Base API
const API = "";

// ---------------- ALERT UTILITY ----------------
function showAlert(message, type = "success") {
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = "alert";
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.querySelector("main").prepend(alertDiv);
    setTimeout(() => alertDiv.remove(), 5000);
}

// ---------------- DYNAMIC TABLE ----------------
function populateTable(id, data, columns) {
    let tableHTML = `<table class="table table-striped table-hover"><thead><tr>`;
    columns.forEach(col => tableHTML += `<th>${col}</th>`);
    tableHTML += `</tr></thead><tbody>`;
    data.forEach(row => {
        tableHTML += `<tr>`;
        columns.forEach(col => tableHTML += `<td>${row[col] !== undefined ? row[col] : ""}</td>`);
        tableHTML += `</tr>`;
    });
    tableHTML += `</tbody></table>`;
    document.getElementById(id).innerHTML = tableHTML;
}

// ---------------- STUDENTS ----------------
function addStudent() {
    const id = document.getElementById("studentId").value;
    const name = document.getElementById("studentName").value;

    fetch(`${API}/add_student`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id: parseInt(id), name})
    })
    .then(res => res.json())
    .then(data => {
        showAlert(data.message, "success");
        viewStudents();
    })
    .catch(() => showAlert("Error adding student", "danger"));
}

function viewStudents() {
    fetch(`${API}/all_students`)
    .then(res => res.json())
    .then(data => {
        populateTable("studentsResult", data.students, ["id", "name"]);
    })
    .catch(() => showAlert("Error fetching students", "danger"));
}

// ---------------- COURSES ----------------
function addCourse() {
    const name = document.getElementById("courseName").value;
    const capacity = document.getElementById("capacity").value;

    fetch(`${API}/add_course`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, capacity: parseInt(capacity)})
    })
    .then(res => res.json())
    .then(data => {
        showAlert(data.message, "success");
        viewCourses();
    })
    .catch(() => showAlert("Error adding course", "danger"));
}

function viewCourses() {
    fetch(`${API}/get_courses`)
    .then(res => res.json())
    .then(data => populateTable("result", data.courses, ["name","capacity","enrolled"]))
    .catch(() => showAlert("Error fetching courses", "danger"));
}

function registerCourse() {
    const course = document.getElementById("courseReg").value;
    const student = document.getElementById("studentReg").value;

    fetch(`${API}/register_course`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({course, student})
    })
    .then(res => res.json())
    .then(data => showAlert(data.message, "success"))
    .catch(() => showAlert("Error registering student", "danger"));
}

function allocate() {
    const course = document.getElementById("courseAlloc").value;

    fetch(`${API}/allocate/${course}`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
        populateTable("result", data.enrolled.map(s => ({id:s.id,name:s.name})), ["id","name"]);
        showAlert("Allocation complete", "success");
    })
    .catch(() => showAlert("Error allocating students", "danger"));
}

// ---------------- FEES ----------------
function addFee() {
    const student = document.getElementById("feeStudent").value;
    const amount = document.getElementById("feeAmount").value;

    fetch(`${API}/add_fee`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ student, amount: parseInt(amount) })
    })
    .then(res => res.json())
    .then(data => {
        showAlert(data.message, "success");
        viewFees();
    })
    .catch(() => showAlert("Error adding payment", "danger"));
}

function viewFees() {
    fetch(`${API}/get_fees`)
    .then(res => res.json())
    .then(data => populateTable("feesResult", data.fees, ["student","amount"]))
    .catch(() => showAlert("Error fetching fees", "danger"));
}

// ---------------- LIBRARY ----------------
function addBook() {
    const isbn = document.getElementById("bookISBN").value;
    const title = document.getElementById("bookTitle").value;

    fetch(`${API}/add_book`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({isbn,title})
    })
    .then(res => res.json())
    .then(data => {
        showAlert(data.message, "success");
        viewBooks();
    })
    .catch(() => showAlert("Error adding book", "danger"));
}

function viewBooks() {
    fetch(`${API}/get_books`)
    .then(res => res.json())
    .then(data => populateTable("libraryResult", data.books, ["isbn","title","status"]))
    .catch(() => showAlert("Error fetching books", "danger"));
}

function borrowBook() {
    const isbn = document.getElementById("borrowISBN").value;

    fetch(`${API}/borrow_book`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ isbn })
    })
    .then(res => res.json())
    .then(data => {
        showAlert(data.message, "success");
        viewBooks();
    })
    .catch(() => showAlert("Error borrowing book", "danger"));
}

function returnBook() {
    fetch(`${API}/return_book`, { method: "POST" })
    .then(res => res.json())
    .then(data => {
        showAlert(data.message, "success");
        viewBooks();
    })
    .catch(() => showAlert("Error returning book", "danger"));
}

// ---------------- PERFORMANCE ----------------
function addScore() {
    const student = document.getElementById("perfStudent").value;
    const score = document.getElementById("perfScore").value;

    fetch(`${API}/add_score`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({student, score: parseInt(score)})
    })
    .then(res => res.json())
    .then(data => {
        showAlert(data.message, "success");
        viewPerformance();
    })
    .catch(() => showAlert("Error adding score", "danger"));
}

function topStudent() {
    fetch(`${API}/top_student`)
    .then(res => res.json())
    .then(data => populateTable("performanceResult", [data.top], ["id","name","score"]))
    .catch(() => showAlert("Error fetching top student", "danger"));
}

function allStudents() {
    fetch(`${API}/all_students`)
    .then(res => res.json())
    .then(data => populateTable("performanceResult", data.students, ["id","name","score"]))
    .catch(() => showAlert("Error fetching students", "danger"));
}

// ---------------- INITIAL LOAD ----------------
viewStudents();
viewCourses();
viewFees();
viewBooks();
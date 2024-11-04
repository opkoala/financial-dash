// Citation for DOM manipulation //
// Date Nov/02/2024
//  https://www.youtube.com/watch?v=y17RuWkWdn8 //
// https://www.youtube.com/watch?v=SrSBhuuuIsg //
// https://www.w3schools.com/jsref/prop_html_innerhtml.asp //
//https://www.w3schools.com/jsref/met_node_appendchild.asp //
 

// Function to add a new revenue entry
function addRevenue() {
    let div = document.createElement('div');
    div.className = 'revenue-entry'; 
    div.innerHTML = `<input type="text" name="revenues[]" placeholder="Revenue name" required>
        <input type="number" name="revenue_amounts[]" placeholder="Amount" step="0.01" required>
        <button type="button" onclick="removeEntry(this)">Delete</button>
        <br>`;
    document.getElementById('revenues').appendChild(div);
}

// Function to add a new expense entry
function addExpense() {
    let div = document.createElement('div');
    div.className = 'expense-entry'; 
    div.innerHTML = `<input type="text" name="expenses[]" placeholder="Expense name" required>
        <input type="number" name="expense_amounts[]" placeholder="Amount" step="0.01" required>
        <button type="button" onclick="removeEntry(this)">Delete</button>
        <br>`;
    document.getElementById('expenses').appendChild(div);
}

// Function to remove an entry 
function removeEntry(button) {
    let confirmRemove = confirm("Are you sure you want to delete this entry?");
    if (confirmRemove) {
        button.parentElement.remove();
    }
}

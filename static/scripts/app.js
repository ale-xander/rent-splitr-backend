console.log('app.js is connected')

const BASE_URL = '/expenses';

const ExpenseFormOne = document.getElementById('ExpenseFormOne');
const ExpenseFormTwo = document.getElementById('ExpenseFormTwo');
const ExpenseFormThree = document.getElementById('ExpenseFormThree');
const expenseSection = document.getElementById('ExpenseListOne');

const allExpensesSuccess = (response) => {
    const {data} = response;
    expenseSection.innerHTML = '';
    response.forEach(expense => {
        const template = expenseTemplate(expense);
        expenseSection.insertAdjacentHTML('afterbegin', template)
    });
};

const getAllExpenses = () => {
    fetch(BASE_URL)
    .then((res) => res.json())
    .then(json => allExpensesSuccess(json))
    .catch((err) => console.log(err))
};
getAllExpenses();

const expenseTemplate = (expense) => {
    return `
    <div class="line-item">
        <p class="description"> ${expense.description}</p>
        <p class="amount">${expense.amount}</p>
        <button class="delete-button">delete</button>
        <button class="edit-button">edit</button>
    </div>
    `;
}
const addNewExpense = (event) => {
    event.preventDefault();
    const description = document.getElementById('ExpenseDescriptionOne');
    const amount = document.getElementById('ExpenseAmountOne');
    const newExpense = { amount: ExpenseAmountOne.value, description: ExpenseDescriptionOne.value, member: 'me' };
    fetch(BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newExpense)
    })
        .then((res) => res.json())
        .then((data) => {
        amount.value = '';
        description.value = '';
        description.focus();
        getAllExpenses();
        })
        .catch((err) => console.log(err))
}

const deleteExpense = (event) => {
    console.log(event);
    const expense_id = event.target.parentNode.id;
    
    fetch(`${BASE_URL}/${expense_id}`, {
        method: 'DELETE',
    })
    .then((res) => res.json())
    .then(data => getAllExpenses())
    .catch((err) => console.log(err));
}



const handleExpenseSectionClick = (event) => {
    event.preventDefault();
    if (event.target.classList.contains('edit-button')) {
      editExpense(event);
    } else if (event.target.classList.contains('submit-edit')) {
      updateExpense(event);
    } else if (event.target.classList.contains('cancel-edit')) {
      getAllExpenses();
    } else if (event.target.classList.contains('delete-button')) {
      deleteExpense(event);
    }
  }
  






  const editExpense = (event) => {
    console.log(event)
    const description = event.target.parentNode.children[0].innerText;
    const amount = event.target.parentNode.children[1].innerText;
    event.target.parentNode.innerHTML = `
        <h4>Edit Expense</h4>
        <form>
        <div>
            <label style="display: block;" for="description">Description</label>
            <input type="text" id="editDescription" name="description" value="${description}" />
        </div> 
        <div>
            <label style="display: block;" for="amount">Amount</label>
            <input type="text" id="editAmount" name="name" value="${amount}" />
        </div>
        
        <button type="button" class="cancel-edit">Cancel</button>
        <button class="submit-edit">Submit</button>
        </form>
    `;
}
  
  
  const updateExpense = (event) => {
      console.log(event)
    const expense_id = event.target.parentNode.parentNode.id;
    const amount = document.getElementById('editAmount').value;
    const description = document.getElementById('editDescription').value;
    const updatedExpense = { amount: amount, description: description };
    fetch(`${BASE_URL}/${expense_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedExpense),
    })
        .then((res) => res.json())
        .then((data) => getAllExpenses())
        .catch((err) => console.log(err));
}
ExpenseFormOne.addEventListener('submit', addNewExpense);
// ExpenseFormTwo.addEventListener('submit', addNewExpense);
// ExpenseFormThree.addEventListener('submit', addNewExpense);
expenseSection.addEventListener('click', handleExpenseSectionClick)
// ExpenseListTwo.addEventListener('click', handleExpenseSectionClick)
// ExpenseListThree.addEventListener('click', handleExpenseSectionClick)
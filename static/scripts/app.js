console.log('app.js is connected')

const BASE_URL = '/expenses'

const ExpenseFormOne = document.getElementById('ExpenseFormOne')
const ExpenseFormTwo = document.getElementById('ExpenseFormTwo')
const ExpenseFormThree = document.getElementById('ExpenseFormThree')
const expenseSection = document.getElementById('ExpenseListOne')


const handleExpenseSectionClick = event => {
  event.preventDefault()
  if (event.target.classList.contains('edit-button')) {
    console.log('edit')
    editExpense(event)
  } else if (event.target.classList.contains('submit-edit')) {
    updateExpense(event)
  } else if (event.target.classList.contains('cancel-edit')) {
    getAllExpenses()
  } 
}

const editExpense = event => {
  const description = event.target.parentNode.children[0].innerText
  const amount = event.target.parentNode.children[1].innerText
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
        <button class="submit-edit">Submit</button>
        </form>
    `
}

const updateExpense = event => {
  const expense_id = event.target.parentNode.parentNode.id
  const amount = document.getElementById('editAmount').value
  const description = document.getElementById('editDescription').value
  const updatedExpense = { amount: amount, description: description }
  fetch(`${BASE_URL}/${expense_id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updatedExpense)
  })
    .then(res => window.location.reload())
    .catch(err => console.log(err))
}

expenseSection.addEventListener('click', handleExpenseSectionClick)
// ExpenseListTwo.addEventListener('click', handleExpenseSectionClick)
// ExpenseListThree.addEventListener('click', handleExpenseSectionClick)

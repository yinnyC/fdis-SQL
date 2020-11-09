const startAddEvent = document.getElementById('start-add-event')
const addEventForm = document.getElementById('add-event-form')

const addEventHandler = () => {
  addEventForm.style.display = 'flex'
}

startAddEvent.addEventListener('click', addEventHandler)

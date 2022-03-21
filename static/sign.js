// 跳出登入註冊視窗
const signButton = document.querySelectorAll('[data-modal-target]')
const closeButton = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')



signButton.forEach(button => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalTarget)
        openModal(modal)
    })
    button.addEventListener('click', () => {
        const modal = button.closest('[data-sign]')
        closeModal(modal)
        overlay.classList.add('active')
    })
})

overlay.addEventListener('click', () => {
    const modals = document.querySelectorAll('[data-sign]')
    modals.forEach(modal => {
        closeModal(modal)
    } )
})

closeButton.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('[data-sign]')
        closeModal(modal)
    })
})


function openModal(modal) {
    if (modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
  }
  
  function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
  }

// 登入註冊
//function
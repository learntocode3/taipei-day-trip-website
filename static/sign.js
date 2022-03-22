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

// 登入、註冊、登出
//const signin=document.querySelector('#signin')
//signin.addEventListener('submit', memberSignin)

function memberSignin(){
    // 從前端拿到input資料換成json格式
    let email = document.getElementById('email-1')
    let password = document.getElementById('password-1')
    const data={
        'email': email.value,
        'password': password.value 
    };

    // 把資料裝在body發送request到後端api
    fetch ("http://127.0.0.1:3000/api/user",{
        method: "PATCH",
        credentials: "include",
        body: JSON.stringify(data),
        cache:"no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })
    })
    .then(function(response){

        if(response.status !==200){
            console.log(`Response status was not 200: ${response.status}`);
            return ;
        }
        response.json()
    .then(function(data){
        console.log(data.ok);
        if(data.ok === false){
            document.getElementById("status").innerText="fail";
        } else {
            document.getElementById("status").innerText="success";
            window.location.reload();
        }
    })
 })
}

function memberSignUp(){
    // 從前端拿到input資料換成json格式
    let name = document.getElementById('name-2')
    let email = document.getElementById('email-2')
    let password = document.getElementById('password-2')
    const data={
        'name' : name.value,
        'email': email.value,
        'password': password.value 
    };

    // 把資料裝在body發送request到後端api
    fetch ("http://127.0.0.1:3000/api/user",{
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache:"no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })
    })
    .then(function(response){

        if(response.status !==200){
            console.log(`Response status was not 200: ${response.status}`);
            return ;
        }
        response.json()
    .then(function(data){
        //console.log(data.ok);
        if(data.error === true){
            document.getElementById("status-2").innerText=data.message;
        } else {
            document.getElementById("status-2").innerText="success";
            //window.location.reload();
        }
    })
 })
}
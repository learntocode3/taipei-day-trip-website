//const BASE_URL = "http://127.0.0.1:3000";
const BASE_URL = "http://52.87.119.150:3000";


let data;
const id = document.URL.split("/").slice(-1)
//console.log(id)
const url = `${BASE_URL}/api/attraction/` + id
//console.log(url)

function changePrice(){
    const morning = document.querySelector('input[value="morning"]') 
    const afternoon = document.querySelector('input[value="afternoon"]')
    const price = document.querySelector('#price')

    morning.addEventListener('click',()=>{
        price.innerHTML = 2000;
    })
    afternoon.addEventListener('click',()=>{
        price.innerHTML = 2500;
    })
}    
   
    
    
    
function fetchAttractions(){
fetch(url).then((response)=>{
    return response.json();
}).then((result)=>{
    data = result.data;
    console.log(data);
    let imgLen = data.images.length
    //確認有幾個圖片 console.log(imgLen)
    let slider = document.querySelector("#slider")
    let dotContain = document.createElement('ul');
    dotContain.setAttribute("id", "dotContain");
    for(let i=0; i<imgLen; i++){
        let li = document.createElement('li');
        let dot = document.createElement('li');
        

        let imgs = document.createElement('img');


        imgs.classList.add('imgAttractions');
        imgs.src = data.images[i];
        li.classList.add('slide');
        dot.classList.add('dot');

        if(i===0){
            li.setAttribute("data-active","");
            dot.setAttribute("data-active","")
        };
        li.appendChild(imgs);
        slider.appendChild(li);
        dotContain.appendChild(dot);
    }
    const couresel = document.querySelector(".carousel")
    couresel.appendChild(dotContain);
    //slider

    let name = document.querySelector("#name");
    name.innerHTML = data.name;
    let categoryMrt = document.querySelector("#categoryMrt")
    categoryMrt.innerHTML = data.category +" at "+data.mrt;
    let info =document.querySelector("#info")
    info.innerHTML = data.description;
    let address = document.querySelector("#address")
    address.innerHTML = data.address;
    let transport = document.querySelector("#transport")
    transport.innerHTML = data.transport;
    
})
};

const buttons = document.querySelectorAll("[data-carousel-button]")

buttons.forEach(button => {
    button.addEventListener("click", () => {
    const offset = button.dataset.carouselButton === "next" ? 1 : -1
    const slides = button
        .closest("[data-carousel]")
        .querySelector("[data-slides]")

    const activeSlide = slides.querySelector("[data-active]")
    let newIndex = [...slides.children].indexOf(activeSlide) + offset
    if (newIndex < 0) newIndex = slides.children.length - 1
    if (newIndex >= slides.children.length) newIndex = 0

    slides.children[newIndex].dataset.active = true
    delete activeSlide.dataset.active

    })
})

buttons.forEach(button => {
    button.addEventListener("click", () => {
    const offset = button.dataset.carouselButton === "next" ? 1 : -1
    const slides = button
        .closest("[data-carousel]")
        .querySelector("#dotContain")

    const activeSlide = slides.querySelector("[data-active]")
    let newIndex = [...slides.children].indexOf(activeSlide) + offset
    if (newIndex < 0) newIndex = slides.children.length - 1
    if (newIndex >= slides.children.length) newIndex = 0

    slides.children[newIndex].dataset.active = true
    delete activeSlide.dataset.active

    })
})

function startBooking(){
    fetch(userAPI)
    .then(res => res.json())
    .then(function(data){
        if (data.data != null){
            location.replace("booking")
        } else {
            document.getElementById("login").click();
        }
    })
}

// 透過前端取得資料送到後端放到booking的table
function booking(){

        bookingTop();

        const bookingData={
            "attractionId":id[0],
            "date":document.querySelector('input[name="date"]').value,
            "time":document.querySelector('input[name="time"]:checked').value,
            "price":document.querySelector('#price').innerHTML
        }
        //console.log(bookingData)

        fetch (`${BASE_URL}/api/booking`,{
            method: "POST",
            credentials: "include",
            body: JSON.stringify(bookingData),
            cache:"no-cache",
            headers: new Headers({
                "content-type":"application/json"
            })
        })
        .then(res => res.json())
        .then(function(data){
            console.log(data.ok)
        })
    }




// Main
fetchAttractions();
changePrice();
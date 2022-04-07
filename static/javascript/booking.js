//const BASE_URL = "http://127.0.0.1:3000/";
const BASE_URL = "http://52.87.119.150:3000/";
const bookingAPI  = `${BASE_URL}api/booking`;
const userAPI_url =   `${BASE_URL}api/user`;
const orderAPI_url = `${BASE_URL}api/order`;
let orderUserTotalPrice;
let orderUserAttraction;
let orderUserAttractionID;
let orderUserAttractionAddress;
let orderUserAttractionImage;
let orderTripDate;
let orderTripTime;

function getBookingInfo(){
    fetch(bookingAPI)
    .then(res => res.json())
    .then(function(data){
        //console.log(data)


        if (data.data === "noData"){
            //change to no booking data
            document.body.querySelector("#bookingInfo").innerHTML = "目前沒有任何待預訂的行程";
            document.body.querySelector("#seperator-1").style = "display:none";
            document.body.querySelector("#seperator-2").style = "display:none";
            document.body.querySelector("#seperator-3").style = "display:none";
            document.body.querySelector("#userContactInfo").innerHTML = "";
            document.body.querySelector(".credit-card").innerHTML = "";
            document.body.querySelector(".orderSubmit").innerHTML = "";
            document.body.querySelector(".footer").style = "height:80%;";
            


        } else if (data != null){
            console.log(data.data)
            orderUserTotalPrice = data.data.price;
            orderUserAttraction = data.data.attraction.name;
            orderUserAttractionID = data.data.attraction.id;
            orderUserAttractionAddress = data.data.attraction.address;
            orderUserAttractionImage = data.data.attraction.image;
            orderTripDate = data.data.date;
            orderTripTime = data.data.time;
            let bookingPic = document.getElementById("bookingPic");
            let bookingImage = document.createElement('img');
            bookingImage.src = data.data.attraction.image;
            bookingImage.classList.add('bookImg'); 
            bookingPic.appendChild(bookingImage)
    
            let attractionName = document.querySelector("#attractionName");
            attractionName.innerText = data.data.attraction.name;
    
            let bookingDate = document.querySelector("#bookingDate");
            bookDate=document.createElement('span');
            bookDate.innerText = data.data.date;
            bookingDate.appendChild(bookDate)
    
            let bookingTime = document.querySelector("#bookingTime");
            bookTime=document.createElement('span');
            bookTime.innerText = data.data.time;
            bookingTime.appendChild(bookTime)
    
            let bookingFee = document.querySelector("#bookingFee");
            bookFee=document.createElement('span');
            bookFee.innerText = data.data.price;
            bookingFee.appendChild(bookFee)
    
            let bookingPlace = document.querySelector("#bookingPlace");
            bookPlace=document.createElement('span');
            bookPlace.innerText = data.data.attraction.address;
            bookingPlace.appendChild(bookPlace)

            document.body.querySelector("#order-totalPrice").innerText = data.data.price;
    
        }


    })
}

function getUser(){
    const signinBtn=document.getElementById('login')
    const logoutBtn=document.getElementById('logout')
    fetch(userAPI_url)
    .then(res => res.json())
    .then(function(data){
        if(data.data != null){
            document.getElementById('greetName').innerText = data.data.name
        } else {
            location.replace(BASE_URL)
        }       
    })
}

function deleteBooking(){
    fetch (bookingAPI, {method:"DELETE"})
    .then(res => res.json())
    .then(function(data){
        if (data.ok === true){
            window.location.reload();
        } else if (data.error === true) {
            location.replace(BASE_URL)
        }
    })

}


getUser();
getBookingInfo();

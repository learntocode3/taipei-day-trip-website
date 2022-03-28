const BASE_URL = "http://127.0.0.1:3000";
//const BASE_URL = "http://52.87.119.150:3000";
const bookingAPI  = `${BASE_URL}/api/booking`;
const userAPI_url =   `${BASE_URL}/api/user`;


function getBookingInfo(){
    fetch(bookingAPI)
    .then(res => res.json())
    .then(function(data){
        console.log(data)
        console.log(data.data.date)
        let bookingPic = document.getElementById("bookingPic");
        let bookingImage = document.createElement('img');
        bookingImage.src = data.data.attraction.image;
        bookingPic.appendChild(bookingImage)

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
        bookPlace.innerText = data.data.attraction.name;
        bookingPlace.appendChild(bookPlace)


    })
}

getBookingInfo();

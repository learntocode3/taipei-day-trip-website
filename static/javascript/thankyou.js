const BASE_URL = "http://127.0.0.1:3000/";
//const BASE_URL = "http://52.87.119.150:3000/";

const orderId = document.URL.split("=").slice(-1)
//console.log(orderId)
const thankYouUrl = `${BASE_URL}api/order/`+ orderId
//console.log(thankYouUrl)

function renderThankYouPage(){
    fetch(thankYouUrl)
    .then(response => response.json())
    .then(function(data){
        //console.log(data.orderID)
        document.getElementById('orderID').innerHTML = data.orderID
    })
}

renderThankYouPage();
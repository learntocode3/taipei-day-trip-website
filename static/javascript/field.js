TPDirect.setupSDK(123973, 'app_LhgynzZTeGWlcousyWdjL85xGDTh2rIMtCkMVdALfdKi3Hk768WvkNTjOTRl', 'sandbox')

// Display ccv field
let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
}

TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // Styling ccv field
        'input.ccv': {
            'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            'font-size': '16px'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        }
    }
})

const submitButton=document.querySelector('order-btn')

TPDirect.card.onUpdate(function (update) {
    // update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        submitButton.removeAttribute('disabled')
    } else {
        // Disable submit Button to get prime.
        submitButton.setAttribute('disabled', true)
        }
    })

function onSubmit(event) {
    event.preventDefault()

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('can not get prime')
        return
    }

   // Get prime
   TPDirect.card.getPrime(function (result) {
    if (result.status !== 0) {
        alert('get prime error ' + result.msg)
        return
    }
    console.log(result.card.prime)
    const orderData={
        'prime': result.card.prime,
        'order': {
            'price':orderUserTotalPrice,
            'trip':{
                'attraction':{
                    'id':orderUserAttractionID,
                    'name':orderUserAttraction,
                    'address':orderUserAttractionAddress,
                    'image':orderUserAttractionImage
                },
                'date':orderTripDate,
                'time':orderTripTime
            },
            'contact':{
                'name':document.querySelector('input[name="orderName"]').value,
                'email':document.querySelector('input[name="orderEmail"]').value,
                'phone':document.querySelector('input[name="orderPhone"]').value
            }
        }
    }
    fetch(orderAPI_url,{
        method:'POST',
        body: JSON.stringify(orderData),
        headers: new Headers({
    "content-type":"application/json"
        })
    })
    .then(res => res.json())
    .then(function(data){
        if (data.data.payment.status===0){
            location.replace(`${BASE_URL}thankyou?number=${data.data.number}`)
        } else {
            alert('交易失敗，請再試一次');
            return
        }
    })
    
})
}

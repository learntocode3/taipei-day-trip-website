function handleScroll(){
    if (!canFetchAttractions) return;
    
    const bottomSpaceLeftToScroll = (
        document.documentElement.scrollHeight - window.innerHeight
        /*
        window.scrollHeight -
        window.scrollTop - 
        window.clientHeight*/
    );
    const scrolled = window.scrollY;

    if (bottomSpaceLeftToScroll > scrolled) return;
    PAGE_SIZE ++;
    fetchAndAppendAttractions();
    
}

function fetchAndAppendAttractions(){
    canFetchAttractions = false;
    const url = createAttractionsUrl();
    fetch(url)
    .then(res => res.json())
    .then(({data, nextPage}) =>{
        //console.log(data.images)
        const fragment = document.createDocumentFragment();
        //const test = document.createElement('div');
        
        
        
        if (nextPage){
        
        data.forEach(({images, name, mrt, category}) => {
            let twelve = document.createElement("div");
            twelve.className = "twelve";
            twelve.appendChild(createAttractionImg(images));
            twelve.appendChild(createAttractionText(name));
            let mrtCat = document.createElement('div')
            mrtCat.className = 'mrtCat';
            mrtCat.appendChild(createAttractionMrt(mrt));
            mrtCat.appendChild(createAttractionCategory(category));
            twelve.appendChild(mrtCat)

            //twelve.appendChild(createAttractionMrt(mrt));
            //twelve.appendChild(createAttractionCategory(category));
            fragment.appendChild(twelve)
            });

        //data.forEach(({name}) => {
            //  fragment.appendChild(createAttractionText(name));
        //});

        attractionContainer.appendChild(fragment);

            //PAGE_SIZE ++;
        } else {
            window.removeEventListener('scroll', handleScroll);
        }
        
        canFetchAttractions = true;



    });
}

function createAttractionImg(images){
    const attractionElement = document.createElement('img');
    attractionElement.classList.add('attractions');
    //console.log(images)
    attractionElement.src = images[0];
    return attractionElement
}

function createAttractionText(name){
    const attractionElement = document.createElement('div');
    attractionElement.classList.add('attractionText');
    attractionElement.textContent = name;
    return attractionElement
}

function createAttractionMrt(mrt){
    const attractionElement = document.createElement('div');
    attractionElement.classList.add('attractionMrt');
    attractionElement.textContent = mrt;
    return attractionElement
}

function createAttractionCategory(category){
    const attractionElement = document.createElement('div');
    attractionElement.classList.add('attractionCategory');
    attractionElement.textContent = category;
    return attractionElement
}



function createAttractionsUrl(){
    //const url = new URL(API_BASE_URL);
    //url.searchParams.set('page', PAGE_SIZE);
    //PAGE_SIZE ++;
    let url = API_BASE_URL + '?page=' + PAGE_SIZE

    return url;
}

/*
function getKeyword(){
    let search = document.getElementById("abc")
    //console.log(search.value)
    
    attractionContainer.innerHTML ='';
    window.removeEventListener('scroll', handleScroll);
    fetch(API_BASE_URL+`?page=0&keyword=${search.value}`)
    .then(res => res.json())
    .then(({data, nextPage}) =>{
        const fragment = document.createDocumentFragment();
        if (nextPage){
            data.forEach(({images, name, mrt, category}) => {
            let twelve = document.createElement("div");
            twelve.className = "twelve";
            twelve.appendChild(createAttractionImg(images));
            twelve.appendChild(createAttractionText(name));
            let mrtCat = document.createElement('div')
            mrtCat.className = 'mrtCat';
            mrtCat.appendChild(createAttractionMrt(mrt));
            mrtCat.appendChild(createAttractionCategory(category));
            twelve.appendChild(mrtCat)
            fragment.appendChild(twelve)
            });

        attractionContainer.appendChild(fragment);
        } else {
            //attractionContainer.innerHTML ='no info';
            window.removeEventListener('scroll', handleScroll);
        }       
        canFetchAttractions = true;
    });
}*/

function getKeyword(evt){
    //canFetchAttractions = false;
    //let search = document.getElementById('abc')
    //console.log(search.value)
    

    let search = document.getElementById("abc")
    console.log(search.value)
    console.log('test')
    
   
    attractionContainer.innerHTML ='';
    fetch(`http://52.87.119.150:3000/api/attractions?keyword=${search.value}`)
    .then(res => res.json())
    .then(({data, nextPage}) =>{
        const fragment = document.createDocumentFragment();
        if (data){
            window.removeEventListener('scroll', handleScroll);
            data.forEach(({images, name, mrt, category}) => {
            let twelve = document.createElement("div");
            twelve.className = "twelve";
            twelve.appendChild(createAttractionImg(images));
            twelve.appendChild(createAttractionText(name));
            let mrtCat = document.createElement('div')
            mrtCat.className = 'mrtCat';
            mrtCat.appendChild(createAttractionMrt(mrt));
            mrtCat.appendChild(createAttractionCategory(category));
            twelve.appendChild(mrtCat)
            fragment.appendChild(twelve)
            });

        attractionContainer.appendChild(fragment);
        } else {
            attractionContainer.innerHTML ='沒有資料';
            window.removeEventListener('scroll', handleScroll);
        }       
        canFetchAttractions = true;
    });
}



//attractionContainer.innerHTML = "無此資料";
// 主程式
const API_BASE_URL = "http://52.87.119.150:3000/api/attractions";
        
let PAGE_SIZE = 0;
let canFetchAttractions = true; 

const attractionContainer = document.getElementById('attractions');
window.addEventListener('scroll', handleScroll);

fetchAndAppendAttractions();
//fetchAndAppendAttractions();
// 主程式
//const BASE_URL = "http://127.0.0.1:3000"
const BASE_URL = "http://52.87.119.150:3000"
const API_BASE_URL = `${BASE_URL}/api/attractions`;        

let PAGE_SIZE = 0;
let keyword = '';
let canFetchAttractions = true; 

const attractionContainer = document.getElementById('attractions');
window.addEventListener('scroll', handleScroll);

fetchAndAppendAttractions();
//---------------------------------------------------------------------------------

function handleScroll(){
    if (!canFetchAttractions) return;
    const bottomSpaceLeftToScroll = (
        document.documentElement.scrollHeight - window.innerHeight
    );
    const scrolled = window.scrollY;

    if (bottomSpaceLeftToScroll > scrolled) return;
    PAGE_SIZE ++;
    fetchAndAppendAttractions();   
}

function createAttractionsUrl(){
    let url;
    if(keyword === ""){
        url = API_BASE_URL + '?page=' + PAGE_SIZE;
    } else { 
        url = API_BASE_URL + '?page=' + PAGE_SIZE + '&keyword=' + keyword;
    }   
    return url;
}

function fetchAndAppendAttractions(){
    canFetchAttractions = false;
    const url = createAttractionsUrl();
    fetch(url)
    .then(res => res.json())
    .then(({data, nextPage}) =>{
        const fragment = document.createDocumentFragment(); 
        if (data){
            data.forEach(({images, name, mrt, category, id}) => {
                let twelve = document.createElement("div");
                let link = document.createElement('a');
                link.setAttribute("href",`${BASE_URL}/attraction/${id}`);
                link.className = "link";
                //console.log(`http://127.0.0.1:3000/attraction/${id}`)
                twelve.className = "twelve";

                link.appendChild(createAttractionImg(images));
                link.appendChild(createAttractionText(name));

                let mrtCat = document.createElement('div')
                mrtCat.className = 'mrtCat';
                mrtCat.appendChild(createAttractionMrt(mrt));
                mrtCat.appendChild(createAttractionCategory(category));

                link.appendChild(mrtCat);
                twelve.appendChild(link);

                fragment.appendChild(twelve)
            });
            attractionContainer.appendChild(fragment);
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


function getKeyword(evt){

    let search = document.getElementById("abc")
    console.log(search.value)
    console.log('test')
    
   
    attractionContainer.innerHTML ='';
    fetch(`${API_BASE_URL}?page=0&keyword=${search.value}`)
    .then(res => res.json())
    .then(({data, nextPage}) =>{
        const fragment = document.createDocumentFragment();
        if (data){
            keyword = search.value;
            PAGE_SIZE = 0;
            //window.removeEventListener('scroll', handleScroll);
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
            //window.removeEventListener('scroll', handleScroll);
        }       
        canFetchAttractions = true;
    });
}




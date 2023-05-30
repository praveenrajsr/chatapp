function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

// Checking User
const authTokens = localStorage.getItem('authTokens')

if(authTokens && window.location.pathname =='/login/'){
    window.location.replace(`http://${window.location.host}/dashboard/`)
} 

if(authTokens === null && window.location.pathname !='/login/'){
    window.location.replace(`http://${window.location.host}/dashboard/`)
}

let logoutUser = () =>{
    localStorage.removeItem('authTokens')
    window.location.replace(`http://${window.location.host}/login/`);
}
document.querySelector('#logout')?.addEventListener('click', ()=>{
    logoutUser();
})
let updateToken = async () =>{
    const authRefrehToken = JSON.parse(authTokens).refresh

    let response = await fetch('http://localhost:8000/api/token/refresh/', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
        },
        body:JSON.stringify({'refresh': authRefrehToken})
    })
    let data = await response.json()
    if(response.status === 200){
        console.log(parseJwt(data.access))
        localStorage.setItem('authTokens', JSON.stringify(data))
    }else{
        logoutUser()
    }
}

window.onload = function(){
    // resfreshin the token
    let fourMinutes = 1000 * 60 * 4
    let interval = setInterval(()=>{
        if(authTokens){
            updateToken()
        }
    }, fourMinutes)

    // Login function
    const login_form = document.querySelector('#login-form');
    if (login_form){
        login_form.addEventListener('submit', (e)=>{
            e.preventDefault()
            loginUser(e)
        })
    }
}

async function loginUser(e) {
    
    console.log(JSON.stringify({'phone': e.target.mobile.value, 'password': e.target.password.value}))
    let response = await fetch('http://localhost:8000/api/token/', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
        },
        body:JSON.stringify({'phone': e.target.mobile.value, 'password': e.target.password.value})
    })
    let data = await response.json()
    if (response.status === 200){
        localStorage.setItem('authTokens', JSON.stringify(data))
        window.location.replace(`http://${window.location.host}/dashboard/`);
    }
}
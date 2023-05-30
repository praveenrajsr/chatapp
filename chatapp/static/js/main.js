function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

const authTokens = localStorage.getItem('authTokens')
const authDetails = parseJwt(authTokens)
const id = new URLSearchParams(window.location.search).get('id');

let url = `ws://${window.location.host}/ws/socket-server/`

const chatSocket = new WebSocket(`${url}`)

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    console.log('Data:', data)

    if (data.type === 'chat') {
        let messages = document.getElementById('messages')

        messages.insertAdjacentHTML('beforeend', `<div class="each_message">
                                    </b></span>${data.message}</p>
                                </div>`)
    }
}

let form = document.getElementById('form')
if(form){
    form.addEventListener('submit', (e) => {
        e.preventDefault()
        let message = e.target.message.value
        chatSocket.send(JSON.stringify({
            'message': message
        }))
        form.reset()
    })
}
function message(content) {
    // Select element
    const element = document.querySelector('.message');
    
    // Fill text content of the element
    element.innerHTML = content;
    // set playstate to running
    element.style.animationPlayState = 'running';
    // remove and add class to restart animation
    element.classList.remove("message");
    setTimeout(function(){
        element.classList.add("message");
    }, 50);
}




// Load event listeners when Dom content is loaded


document.addEventListener('DOMContentLoaded', () => {
    
    // Add Event Listener to the textarea
    const element = document.querySelector('#newPost');

    // Add multiple event listeners to the the textarea
    ['keyup', 'keydown', 'keypress'].forEach(evt => {
        element.addEventListener(evt, () => {
            
            let value = element.value.length;
            document.querySelector('#count').innerHTML = `${value}/150`;
            if (value > 135) {
                document.querySelector('#count').style.color = 'red';
            } else {
                document.querySelector('#count').style.color = 'initial';
            }
        }) 
        
    });

    // submit new post 
    document.querySelector('#newpostForm').onsubmit = () => {
        
        fetch('/newPost', {
            method: 'POST',
            body: JSON.stringify({
                content: element.value
            })
        })
        .then(response => response.json())
        .then(result => {
            // print result
            console.log(result.message);
            element.value = "";
            document.querySelector('#count').innerHTML = `0/150`;
            document.querySelector('#count').style.color = 'initial';
            message(result.message);
            setTimeout(function(){
                location.reload();
            }, 900);
        });

        
        return false;
    }
});


function get_user_id() {
    // Get user id from localstorage
    const user_id = parseInt(localStorage.getItem("user_id"));

    return user_id;
}
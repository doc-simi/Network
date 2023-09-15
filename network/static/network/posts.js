// Default start of the post to show 
let start = 0;
let end = 9;
const diff = 10;
let EOF;

function check_pags(arg) {
    if (arg === "n") {
        if (end > EOF) {
            return false;
        } else {
            return true;
        }
    } else if (arg === "p") {
        if (start - diff < 0) {
            return false;
        } else {
            return true;
        }
    }
}

function check_btns(arg) {
    if (arg === "p") {
        if (start <= 0) {
            previous_btn.classList.add("disabled");
        }
        else {
            previous_btn.classList.remove("disabled");
        }
        next_btn.classList.remove("disabled");
    } else if (arg === "n") {
        if (end >= EOF) {
            next_btn.classList.add("disabled");
        }
        else {
            next_btn.classList.remove("disabled");
        }
        previous_btn.classList.remove("disabled");
    }
}

function next() {
    if (check_pags('n')) {
        start += diff;
        end += diff;
    }
    check_btns('n');
    load_posts();
}

function previous() {
    if (check_pags('p')) {
        start -= diff;
        end -= diff;
    }
    check_btns('p');
    load_posts();
}


document.addEventListener('DOMContentLoaded', () => {
    // load posts
    fetch(`/posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(result => {
        create_elements(result.posts, document.querySelector(".block_body"));
        EOF = result.posts_count;
        
        previous_btn.classList.add("disabled");
        if (end >= EOF) {
            next_btn.classList.add("disabled");
        }
    });
    
    next_btn.onclick = next;
    previous_btn.onclick = previous;
    
});

function load_posts() {
    fetch(`/posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(result => {
        create_elements(result.posts, document.querySelector(".block_body"));
        EOF = result.posts_count;
        
    });
}


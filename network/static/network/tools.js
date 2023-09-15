// Get user id from localstorage
const user_id = get_user_id();


    
const next_btn = document.querySelector("#next").parentElement;
const previous_btn = document.querySelector("#previous").parentElement;


function create_elements(info, append_to) {
    append_to.innerHTML = "";
    const comment1 = document.createComment("This is the main container of every post");
    append_to.append(comment1);
    const main_div = document.createElement("div");
    main_div.className = "post_contents";
    info.forEach(x => {
        const postDiv = document.createElement("div");
        const comment2 = document.createComment(`This is the container of every post. So this is post ${x.id}'s div`);
        postDiv.className = "post";
        
        main_div.append(comment2);
        main_div.append(postDiv);


        const section1 = document.createElement("div");
        const comment3 = document.createComment("This is section 1. It contains the body of the post, \
        It also contains a collpase textarea but it is only viewable to post owners");

        const p1 = document.createElement("p");
        p1.className = "content";
        p1.innerHTML = x.body;
        p1.setAttribute("id", `post-content${x.id}`)
        section1.append(p1);
        
        const section1div = document.createElement("div");
        section1div.className = "collapse";
        section1div.setAttribute("id", `editpost${x.id}`)
        
            const textarea = document.createElement("textarea");
            textarea.setAttribute("id", `editpost_textarea${x.id}`);
            textarea.setAttribute("rows", "2");
            textarea.setAttribute("maxlength", "150");
        section1div.append(textarea);

        section1div.innerHTML += `<button class="badge badge-secondary" data-id="${x.id}"
        onclick="editpost(this)">Save</button>`;
        section1.append(section1div);

        postDiv.append(comment3);
        postDiv.append(section1);
        

        const section2 = document.createElement("div");
        const comment4 = document.createComment("This is section 2. It contains the like and add comment \
        buttons, also the likes and comments count. Then also contains the link that expands the edit textarea \
        in section 1");


        const commentHTML = (x.comments > 1) ? `${x.comments} comments`:`${x.comments} comment`;
        const liketHTML = (x.likes > 1) ? `${x.likes} likes`:`${x.likes} like`;
        const likeclass = (x.liked_by.includes(user_id)) ? `<i class="fas fa-heart like red" 
        data-postid="${x.id}" onclick="likePost(this)"></i>`:
        `<i class="far fa-heart like" data-postid="${x.id}" onclick="likePost(this)"></i>`;
        if (user_id && user_id === x.user_id) {
            var ahtml = `<a data-toggle="collapse" href="#editpost${x.id}" role="button" aria-expanded="false" 
            aria-controls="editpost${x.id}" data-id="${x.id}" data-status="false" onclick="fill(this)">Show Edit Post</a>`;
        } else {
            var ahtml = "";
        }
        section2.innerHTML = `${likeclass} <i class="text-muted add_comment" 
        data-toggle="collapse" data-target="#commentCollapse${x.id}" aria-expanded="false" 
        aria-controls="commentCollapse${x.id}">Add comment <i class="far fa-comment"></i></i>
        ${ahtml}
        <h6><span id="likecount${x.id}">${liketHTML}</span>, 
        <span id="commentcount${x.id}">${commentHTML}</span></h6>`;
        
        
        postDiv.append(comment4);
        postDiv.append(section2);
        
        const section3 = document.createElement("div");
        const comment5 = document.createComment("This is section3. This just contains the comment textarea \
        which is already collapsed");
        
        section3.className = "collapse";
        section3.setAttribute("id", `commentCollapse${x.id}`);
        const section3textarea = document.createElement("textarea");
        section3textarea.setAttribute("id", `add_comment${x.id}`);
        section3textarea.setAttribute("rows", "2");
        section3textarea.setAttribute("maxlength", "100");
        section3.append(section3textarea);
        section3.innerHTML += `<button class="badge badge-secondary" data-target_id="${x.id}"
        onclick="postcomment(this)">Add comment</button>`;
        
        postDiv.append(comment5);
        postDiv.append(section3);
        
        postDiv.append(document.createElement("hr"));
        
        const section4 = document.createElement("div");
        const comment6 = document.createComment("This is section 4. Section 4 contains the user avatar, \
        the username, date joined and the button that expands the collapsed comment's div");
        section4.innerHTML = `<img src="https://i.ibb.co/ZfN7ypd/user.png" alt="user">`;
        section4.innerHTML += `<p class="user"><a href="/user/${x.user_id}">${x.user}</a></p> <p class="timestamp text-muted">${x.timestamp}</p>`
        section4.innerHTML += `<button class="babge badge-secondary badge-pill btn-badge" data-toggle="collapse" 
        data-target="#showComments${x.id}" aria-expanded="false" aria-controls="showComments${x.id}">
        View comments</button>`
        
        postDiv.append(comment6);
        postDiv.append(section4);
        
        const section5 = document.createElement("div");
        section5.className = "comments collapse";
        section5.setAttribute("id", `showComments${x.id}`);
        const comment7 = document.createComment("This is section 5, that contains the entire comments of \
        this post. It is already collapsed");

        createPostDivs(x.allcomments, section5);
        
        postDiv.append(comment7);
        postDiv.append(section5);
        
    });

    append_to.append(main_div);
}


function createPostDivs(element, section5) {
    section5.innerHTML = "";
    element.forEach(y => {
        const comment8 = document.createComment("This div contains the each comment with it's like button \
        counts. Also contains the username and date joined");
        section5.append(comment8);

        const section5div = document.createElement("div");
        section5div.innerHTML = `<p class="comment" id="comment${y.id}">${y.comment}</p>`;
        const yliketHTML = (y.likes > 1) ? `${y.likes} likes`:`${y.likes} like`;
        const ylikeclass = (y.liked_by.includes(user_id)) ? `<i class="fas fa-heart red" 
        data-commentid="${y.id}" onclick="likeComment(this)"></i>`:
        `<i class="far fa-heart" data-commentid="${y.id}" onclick="likeComment(this)"></i>`;
        section5div.innerHTML += ylikeclass;
        section5div.innerHTML += `<h6>${yliketHTML}</h6>`;
        const p2 = document.createElement("p");
        p2.className = "user";
        p2.innerHTML = `<a href="/user/${y.user_id}">${y.user}</a>`;
        const p3 = document.createElement("p");
        p3.className = "timestamp text-muted";
        p3.innerHTML = y.timestamp;
        section5div.append(p2);
        section5div.append(p3);
        section5.append(comment8);
        section5.append(section5div);
    });
}


function likePost(element) {
    fetch('/like-post', {
        method: 'PUT',
        body: JSON.stringify({
            post: element.dataset.postid,
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status) {
            message(result.message);
            throw new Error("Login in please");
        }
        if (result.liked) {
            element.className = "fas fa-heart like red";
        } else {
            element.className = "far fa-heart like";
        }
        const likeHTML = document.querySelector(`#likecount${element.dataset.postid}`);
        likeHTML.innerHTML = (result.no_likes > 1) ? `${result.no_likes} likes`: `${result.no_likes} like`; 
    });
    
}

function likeComment(element) {
    fetch('/like-comment', {
        method: 'PUT',
        body: JSON.stringify({
            comment: element.dataset.commentid,
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status) {
            message(result.message);
            throw new Error("Login in please");
        }
        if (result.liked) {
            element.className = "fas fa-heart like red";
        } else {
            element.className = "far fa-heart like";
        }
        const likeHTML = element.parentElement.getElementsByTagName('h6')[0];
        likeHTML.innerHTML = (result.no_likes > 1) ? `${result.no_likes} likes`: `${result.no_likes} like`; 
    });
}


function postcomment(element) {
    const id = element.dataset.target_id;
    const textarea = document.querySelector(`#add_comment${id}`);
    const value = textarea.value;
    textarea.value = "";
    const section5 = document.querySelector(`#showComments${id}`);
    fetch('/post-comment', {
        method: 'POST',
        body: JSON.stringify({
            comment: value,
            post: id
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status) {
            message(result.message);
        }
        else {
            createPostDivs(result.comments, section5);
            
            const count = result.comments[0].comments_count;
            const commentHTML = (count > 1) ? `${count} comments`:`${count} comment`;
            document.querySelector(`#commentcount${id}`).innerHTML = commentHTML;
        }
        
    });
}


function editpost(element) {
    const id = element.dataset.id;
    const new_post = document.querySelector(`#editpost_textarea${id}`).value;

    fetch('/edit-post', {
        method: 'POST',
        body: JSON.stringify({
            content: new_post,
            id: id,
            user_id: user_id
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status) {
            message(result.message);
            throw new Error("System detects malicious actions");
        }
        document.querySelector(`#editpost_textarea${id}`).value = "";
        document.querySelector(`#post-content${id}`).innerHTML = result.post;

        message(result.message);
    });
    

}

function fill(element) {
    const id = element.dataset.id;
    const status = element.dataset.status;
    document.querySelector(`#editpost_textarea${id}`).value = 
    document.querySelector(`#post-content${id}`).innerText;
    element.innerText = (status === "false") ? "Hide Edit post": "Show Edit post";
    element.dataset.status = (status === "true") ? false: true;

}







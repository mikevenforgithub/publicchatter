document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#allposts').addEventListener('click', () => load_tweetbox('alltweets'));
  document.querySelector('#allfollowing').addEventListener('click', () => load_tweetbox('following'));
  

  // By default, load the inbox
  
});


function compose_email() {

  // Show both views
  document.querySelector('#alltweets').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'block';
  

  // Clear out body field
  document.querySelector('#compose-body').value = '';
}


//  POSTING TWEET

function send_tweet() {

    let body = document.querySelector('#compose-body').value;

    //FETCHING TAKEN FROM COURSE SPECIFICS
    fetch('/tweets', {
      method: 'POST',
      body: JSON.stringify({
          body: (body)
      })
    })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
        });
  
}


function edit_tweet(id) {
    document.getElementById(`editbutton${id}`).onclick = null;
    var body = document.querySelector(`#bodyoftweet${id}`);
    body.style.display = "none";
    var tweetedit = document.createElement("input");
    tweetedit.setAttribute('type', 'text');
    tweetedit.setAttribute('value', `${body.innerHTML}`);
    tweetedit.setAttribute('id', 'newcomment');
    var container = document.querySelector(`#postbodycontainer${id}`);
    container.appendChild(tweetedit);
    var save = document.createElement("button");
    save.innerHTML = ("Save");
    container.appendChild(save);

    
    save.addEventListener('click', () => {
      fetch(`/edit/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              body: tweetedit.value
          })
        });
      
        tweetedit.style.display = 'none';
        save.style.display = 'none';
        body.style.display = "block";
        document.querySelector(`#bodyoftweet${id}`).innerHTML = tweetedit.value;
  });
  

}




function like_tweet(id){

  var likebutton = document.querySelector(`#like-btn-${id}`);
  var numberlikes = document.querySelector(`#like-count-${id}`);

  
    if ( likebutton.innerText == "Like") {
      fetch(`/like/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like: true
        })
      })
      numberlikes.innerText = parseInt(numberlikes.innerText) + 1;
      likebutton.innerText = 'Unlike';

      fetch(`/like/${id}`)
      .then(response => response.json())
      .then(tweet => {
          numberlikes = tweet.likes;
      });
        

    } else { 
      fetch(`/like/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like: false
        })
      })
      numberlikes.innerText = parseInt(numberlikes.innerText) - 1;
      likebutton.innerText = 'Like';

      fetch(`/like/${id}`)
      .then(response => response.json())
      .then(tweet => {
          numberlikes = tweet.likes;
      });
      
    }
    return false; 
  
}






document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#alltweetsbutton').addEventListener('click', () => load_tweetbox('alltweets'));
    document.querySelector('#allfollowingbutton').addEventListener('click', () => load_tweetbox('following'));
  
    // By default, load the inbox
    load_tweetbox('alltweets');
});


//  WRITING TWEET

 
function send_tweet() {

    var body = document.querySelector('#compose-body').value;

    //FETCHING TAKEN FROM COURSE SPECIFICS
    fetch('/tweets', {
      method: 'POST',
      body: JSON.stringify({
          body: (body),
      })
    })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
        });
  
}


function load_tweetbox(tweetbox) {

  // SHOWING ONLY WHAT WE WANT TO SEE
  var alltweets_view = document.querySelector('#alltweets');
  var compose_view = document.querySelector('#compose-view');

  alltweets_view.style.display = "none";
  compose_view.style.display = "none";
  
  alltweets_view.style.display = "block";
  compose_view.style.display = "block";

  alltweets_view.innerHTML = '';


  //GET REQUEST
  fetch(`/tweets/${tweetbox}`)
    .then(response => response.json())
    .then(tweets => {

      if (tweets.length == 0) {
        alltweets_view.innerHTML = '<p style = "font-size: large; font-weight: bold;">This Tweetbox is Empty</p>';
      }
      else {
        for (tweet in tweets) {

          //SETTING VIEW PARAMETERS


          var twt = document.createElement("div");
          var twtinnertop = document.createElement("div");
          var twtinnerbottom = document.createElement("div");
          var commentsection = document.createElement("div");
          var likesection = document.createElement("div");
          var body = document.createElement('h3');
          var writer = document.createElement('h2');
          var time = document.createElement('p');
          var id = document.createElement('p');
          var commentlist = document.createElement('ul');

          twtinnertop.setAttribute('id', 'innertop');
          twtinnerbottom.setAttribute('id', 'innerbottom');
          likesection.setAttribute('id', 'likesection');
          commentsection.setAttribute('id', 'commentsection');

          var comment = document.createElement("input");
          comment.setAttribute('type', 'text');
          comment.setAttribute('value', '');
          comment.setAttribute('id', 'comment');
          var commentbutton = document.createElement("button");
          commentbutton.innerHTML = "Comment";
          var followbutton = document.createElement("button");
          followbutton.innerHTML = "Follow";
          var likebutton = document.createElement("button");
          likebutton.innerHTML = "Like";

          twtinnertop.style.height = '25px';
          twtinnertop.style.marginBottom = '25px';
          body.innerHTML = tweets[tweet]['body']
          writer.innerHTML = tweets[tweet]['user']
          
          id.innerHTML = tweets[tweet]['id'];
          id.style.display = 'none';

          time.innerHTML = tweets[tweet]['timestamp'];

          twt.style.borderStyle = 'solid';
          twt.style.borderColor = 'black';
          twt.style.borderWidth = '1px';
          twt.style.marginBottom = '10px';
          
          twt.classList.add('container');
          twt.classList.add('tweet');


          //STYLE
          body.style.display = 'inline-block';
          
          writer.style.display = 'inline-block';
          writer.style.margin = '5px';
          time.style.display = 'inline-block';
          time.style.margin = '10px';
          time.style.float = 'right';
          time.style.color = 'blue';


          //INSERTING
          alltweets_view.appendChild(twt);
          twt.appendChild(twtinnertop);
          twt.appendChild(twtinnerbottom);
          twt.appendChild(commentsection);
          twt.appendChild(likesection);
          twt.appendChild(id);
          twtinnertop.appendChild(writer);
          twtinnertop.appendChild(followbutton);
          twtinnertop.appendChild(time);
          twtinnerbottom.appendChild(body);
          twtinnerbottom.appendChild(commentsection);
          twtinnerbottom.appendChild(likesection);
          commentsection.appendChild(commentlist);
          commentsection.appendChild(comment);
          commentsection.appendChild(commentbutton);
          likesection.appendChild(likebutton);
              

          //CLICK ON Comment
          commentbutton.addEventListener('click', () => add_comment());
          
        }
      }
    }
    );
}

 

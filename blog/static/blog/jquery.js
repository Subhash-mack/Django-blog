  $('.like-form').submit(function (e) {
    e.preventDefault()
    const post_id = $(this).attr('id')
    const liketest = $(`.like-btn${post_id}`).text()
    const trim = $.trim(liketest)
    const url = $(this).attr('action')
    let res;
    const likes = $(`.like-count${post_id}`).text()
    const trimcount = parseInt(likes)
    console.log(trim)

    $.ajax({
      type: 'POST',
      url: url,
      data: {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'post_id': post_id,
      },
      success: function (response) {
        if (trim === 'Dislike') {
          $(`.like-btn${post_id}`).text('Like')
          $(`.like-btn${post_id}`).removeClass('btn btn-danger')
          $(`.like-btn${post_id}`).addClass('btn btn-primary')
          res = trimcount - 1
        } else {
          $(`.like-btn${post_id}`).text('Dislike')
          $(`.like-btn${post_id}`).addClass('btn btn-danger')
          res = trimcount + 1
        }
        $(`.like-count${post_id}`).text(res)
      },
      error: function (response) {
        console.log('error', response);
      }
    })

  });

  function showNotifications() {
    const container=document.getElementById('notification-container');
    if(container.classList.contains('d-none')){
      container.classList.remove('d-none');
    }
    else{
      container.classList.add('d-none');
    }
    
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function removeNotifications(removeNotificationURL,redirectURL) {

  // element=document.getElementsByClassName('dropdown-item-close');
  // for (var i = 0 ; i < element.length; i++) {
  //   console.log(element[i]);
  //   element[i].addEventListener("click" ,function(e){
  //   e.preventDefault();
    const csrftoken = getCookie('csrftoken');
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {
           if (xmlhttp.status == 200) {
              window.location.replace(redirectURL);
            console.log("success");

           }
           else {
              alert('There was an error.');
           }
        }
    };

    xmlhttp.open("DELETE", removeNotificationURL, true);
    xmlhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xmlhttp.send();

  }

  $('.notification-badge').click(function(){
    if($.trim(this.textContent)>0){
      $('.notification-badge').text('.')
    }
  }

  )

// $(function () {
//     var availableTags = [{
//         %
//         for obj in object_list %
//       }
//       "{{ obj.title }}",
//       {
//         % endfor %
//       }
//     ];
//     $("#query").autocomplete({
//       source: availableTags
//     });
//   });

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
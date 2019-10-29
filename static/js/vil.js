$(document).ready(function() {

    $(".vil-page-add").click(function() {
        var categoryid = $(this).attr('data-categoryid');
        var title = $(this).attr('data-title');
        var url = $(this).attr('data-url');
        var clickedButton = $(this);
        
        $.get('/vil/search_add_page/',
              {'category_id': categoryid, 'title': title, 'url': url},
              function(data) {
                  $('#page-listing').html(data);
                  clickedButton.hide();
      });

    });
});

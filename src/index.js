function load_players() {
    $.ajax({
        url: 'http://localhost:5000/load_players',
        context: this,
        method: "get",
        dataType: "json"
    }).done(function(data, status) {
        if (data.success) {
            html_string = '';
            for (player of data.result) {
                html_string += '<div class="row">';
                html_string += '<div class="col-2">' + player.ranking + '</div>';
                // html_string += '<div class="col-3"><img src=' + player.country_img + ' alt=' + player.country + '></img></div>';
                html_string += '<div class="col-3">' + player.country + '</div>';
                html_string += '<div class="col-5">' + player.name + '</div>';
                html_string += '<div class="col-2">' + get_rating_badge(player.rating) + '</div>';
                html_string += '</div>'
            }
            $('#players').html(html_string);
        }
    });
}

function get_player_rating() {
    rating = $('#player_name').val()
    $.ajax({
        url: 'http://localhost:5000/get_player_rating?p=' + rating,
        context: this,
        method: "get",
        dataType: "json"
    }).done(function(data, status) {
        print(data)
    });
}

function get_rating_badge(rating) {
    if (rating > 7) {
        return '<span class="badge badge-success">' + rating + '</span>';
    } else if (rating > 3) {
        return '<span class="badge badge-warning">' + rating + '</span>';
    } else {
        return '<span class="badge badge-danger">' + rating + '</span>';
    }
}
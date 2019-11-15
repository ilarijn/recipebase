$(document).ready(function () {

    $(function () {
        $('button[name="add_button"]').click(function () {

            var add = $(this).parent().parent();
            obj = {};
            $cells = $(add).children();
            $cells.each(function (cell) {
                if ($(this).attr('class') == "amount") {
                    obj[$(this).attr('class')] = $(this).children('input').val();
                    $(this).children('input').val("");
                } else {
                    obj[$(this).attr('class')] = $(this).text().trim();
                }
            });
            obj['id'] = $(add).attr('id');

            $("#added_ingredients").find('tbody')
                .append($('<tr>')
                    .attr('class', 'ingredient')
                    .attr('id', obj['id'])
                    .append($('<td>')
                        .attr('class', 'name')
                        .html(obj['name']))
                    .append($('<td>')
                        .attr('class', 'amount')
                        .html(obj['amount']))
                    .append($('<td>')
                        .attr('class', 'unit')
                        .html(obj['unit']))
                    .append($('<td>')
                        .append($('<button>')
                            .attr('name', 'remove_button')
                            .html("Remove"))
                    ))
        })
    });

    $(document).on('click', 'button[name="remove_button"]', function () {
        $(this).parent().parent().remove();
    });

    $(document).on('click', 'button[name="create_button"]', function () {
        var id_list = []
        $("#added_ingredients tr.ingredient").each(function () {
            var ingredients_list = [];
            obj = {}
            $cells = $(this).children();
            $cells.each(function (cell) {
                var attr = $(this).attr('class');
                if (attr !== typeof undefined && attr !== false) {
                    obj[$(this).attr('class')] = $(this).text().trim();
                }
            });
            obj['id'] = $(this).attr('id');
            id_list.push(obj);

        });
        $.ajax({
            url: "/recipes/create/",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                name: $("#namefield").val(),
                instructions: $("#instrfield").val(),
                ingredients: id_list
            }),
            type: 'POST',
            success: function (response) {
                $("#main").children().remove();
                $("#main").append("<p>Recipe created!</p>");
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

});


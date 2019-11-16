$(document).ready(function () {

    $(document).on('click', 'button[name="remove_button"]', function () {
        $(this).parent().parent().remove();
    });

    $(document).on('click', 'button[name="save_button"]', function () {
        var recipe_id = $('table[name="recipe"]').attr('id');
        console.log(recipe_id);
        var id_list = [];
        $("#added_ingredients tr.ingredient").each(function () {
            var ingredients_list = [];
            obj = {};
            $cells = $(this).children();
            $cells.each(function (cell) {
                var attr = $(this).attr('class');
                if (attr !== typeof undefined && attr !== false) {
                    if ($(this).attr('class') == "amount") {
                        obj[$(this).attr('class')] = $(this).children('input').val();
                    } else {
                        obj[$(this).attr('class')] = $(this).text().trim();
                    }
                }
            });
            obj['id'] = $(this).attr('id');
            id_list.push(obj);
        });

        $.ajax({
            url: "/recipes/" + recipe_id + "/save/",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                name: $("#namefield").val(),
                instructions: $("#instrfield").val(),
                ingredients: id_list
            }),
            type: 'POST',
            success: function (response) {
                $("#main").children().remove();
                $("#main").append("<p>Changes saved!</p>");
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

});
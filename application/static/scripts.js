$(document).ready(function () {

    $('input[name="add_button"]').click(function () {
        $('input[name="hidden_name"]').val($('#namefield').val());
        $('input[name="hidden_instructions"]').val($('#instrfield').val());
    }
    );

    $('input[name="remove_button"]').click(function () {
        $('input[name="hidden_name"]').val($('#namefield').val());
        $('input[name="hidden_instructions"]').val($('#instrfield').val());

    }
    );

    $(function () {
        $('button[name="remove_button"]').click(function () {
            var remove_id = $(this).parent().parent().attr('id');
            var id_list = []
            $("#new_recipe tr.ingredient").each(function () {
                if ($(this).attr('id') != remove_id) {
                    obj = {}
                    $cells = $(this).children();
                    $cells.each(function (cell) {
                        obj[$(this).attr('class')] = $(this).text().trim();
                    });
                    obj['id'] = $(this).attr('id');
                    id_list.push(obj);
                }
            });
            $.ajax({
                url: "/recipes/clear",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({
                    name: $("#namefield").val(),
                    instructions: $("#instrfield").val(),
                    ingredients: id_list
                }),
                type: 'POST',
                success: function (response) {
                    console.log(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        });
    });

    $(function () {
        $('button[name="add_button"]').click(function () {
            var id_list = [];
            $("#new_recipe tr.ingredient").each(function () {
                obj = {};
                $cells = $(this).children();
                $cells.each(function (cell) {
                    obj[$(this).attr('class')] = $(this).text().trim();
                });
                obj['id'] = $(this).attr('id');
                id_list.push(obj);
            });
            var add = $(this).parent().parent();
            console.log($(add).attr('id'));
            obj = {};
            $cells = $(add).children();
            $cells.each(function (cell) {
                if ($(this).attr('class') == "amount") {
                    obj[$(this).attr('class')] = $(this).children('input').val();
                } else {
                    obj[$(this).attr('class')] = $(this).text().trim();
                }
            });
            obj['id'] = $(add).attr('id');
            id_list.push(obj);

            $.ajax({
                url: "/recipes/new/",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({
                    name: $("#namefield").val(),
                    instructions: $("#instrfield").val(),
                    ingredients: id_list
                }),
                type: 'POST',
                success: function (response) {
                    document.write(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        });
    });

});
$(document).ready(function () {


    $(function () {
        var ingredients = [];
        $.ajax({
            url: "/ingredients/list/",
            dataType: "json",
            type: 'GET',
            async: false,
            success: function (response) {
                ingredients = response;
            },
            error: function (error) {
                console.log(error);
            }
        });
        $("#new_ingredient").autocomplete({
            minLength: 0,
            source: ingredients,
            messages: {
                noResults: '0 search results',
                results: function (amount) {
                    return amount + ' search results'
                }
            },
            focus: function (event, ui) {
                $("#new_ingredient").val(ui.item.name);
                return false;
            },
            select: function (event, ui) {
                $("#new_ingredient").val(ui.item.name);
                $("#new_ingredient").attr('readonly', true);
                $("#ingredient_id").val(ui.item.id);
                $("#ingredient_unit").val(ui.item.unit);
                $("#ingredient_unit").attr('readonly', true);
                $("#ingredient_category").val(ui.item.category);
                $("#ingredient_category").attr('readonly', true);
                $("#ingredient_kcal").val(ui.item.kcal);
                $("#ingredient_kcal").attr('readonly', true);
                return false;
            }
        })
            .autocomplete("instance")._renderItem = function (ul, item) {
                return $('<li class="autocomplete">')
                    .append("<div>" + item.name + "<br><font size='1'>" + item.unit + "</font></div>")
                    .appendTo(ul);

            };
        $.ui.autocomplete.filter = function (array, term) {
            var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(term), "i");
            return $.grep(array, function (value) {
                return matcher.test(value.name);
            });
        };
    });


    $(function () {
        $('button[name="add_button"]').click(function () {
            var add = $(this).parent().parent();
            obj = {};
            $cells = $(add).children();
            $cells.each(function (cell) {
                obj[$(this).attr('class')] = $(this).children('input').val();
                $(this).children('input').val("");
            });
            $("#added_ingredients").find('tbody')
                .append($('<tr>')
                    .attr('class', 'ingredient')
                    .append($('<td style="display:none;">')
                        .attr('class', 'id')
                        .html(obj['id']))
                    .append($('<td>')
                        .attr('class', 'amount')
                        .html(obj['amount']))
                    .append($('<td>')
                        .attr('class', 'unit')
                        .html(obj['unit']))
                    .append($('<td>')
                        .attr('class', 'name')
                        .html(obj['name']))
                    .append($('<td style="display:none;">')
                        .attr('class', 'kcal')
                        .html(obj['kcal']))
                    .append($('<td style="display:none;">')
                        .attr('class', 'category')
                        .html(obj['category']))
                    .append($('<td>')
                        .append($('<button>')
                            .attr('name', 'remove_button')
                            .html("Remove"))
                    ))
            $.fn.clearReadOnly();
        })
    });

    $(document).on('click', 'button[name="remove_button"]', function () {
        $(this).parent().parent().remove();
    });

    $(document).on('click', 'button[name="create_button"], button[name="save_button"]', function () {
        var recipe_id;
        var post_url;
        var success_message;

        if ($(this).is('button[name="create_button"]')) {
            post_url = "/recipes/create/";
            success_message = "<p>Recipe created!</p>";
        } else if ($(this).is('button[name="save_button"]')) {
            recipe_id = $('table[name="recipe"]').attr('id');
            post_url = "/recipes/" + recipe_id + "/save/";
            success_message = "<p>Changes saved!</p>";
        }

        var recipe_name = $("#namefield").val();
        var instructions = $("#instrfield").val();
        var ingredients = [];

        if (recipe_name == '') {
            $("#error").children().remove();
            $("#error").append('<p><font color="red" size="1">Enter a name for your recipe.</font></p>');
            return;
        }

        $("#added_ingredients tr.ingredient").each(function () {
            obj = {};
            $cells = $(this).children();
            $cells.each(function (cell) {
                var attr = $(this).attr('class');
                if (attr !== typeof undefined && attr !== false) {
                    obj[$(this).attr('class')] = $(this).text().trim();
                }
            });
            ingredients.push(obj);
        });

        if ($.isEmptyObject(ingredients)) {
            $("#error").children().remove();
            $("#error").append('<p><font color="red" size="1">Add at least one ingredient to your recipe.</font></p>');
            return;
        }

        $.ajax({
            url: post_url,
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                name: recipe_name,
                instructions: instructions,
                ingredients: ingredients
            }),
            type: 'POST',
            success: function (response) {
                $("#main").children().remove();
                $("#main").append(success_message);
            },
            error: function (error) {
                console.log(error);
                $("#main").children().remove();
                $("#main").append("<p>An error occurred</p>");
            }
        });
    });


    $('button[name="clear_button"]').click(function () {
        $.fn.clearReadOnly();
    });

    $.fn.clearReadOnly = function () {
        if ($("#new_ingredient").is('[readonly]')) {
            $("#new_ingredient").attr('readonly', false);
            $("#new_ingredient").val("");
            $("#ingredient_unit").attr('readonly', false);
            $("#ingredient_unit").val("");
            $("#ingredient_category").attr('readonly', false);
            $("#ingredient_category").val("");
            $("#ingredient_kcal").attr('readonly', false);
            $("#ingredient_kcal").val("");
            $("#ingredient_id").val("");
        }
    }
});


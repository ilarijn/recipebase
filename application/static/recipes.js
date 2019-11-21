$(document).ready(function () {


    //Get ingredients for autocomplete from db
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
        $("#add_name").autocomplete({
            minLength: 0,
            position: { my: 'left-40 top', at: 'left bottom' },
            source: ingredients,
            messages: {
                noResults: '0 search results',
                results: function (amount) {
                    return amount + ' search results'
                }
            },
            focus: function (event, ui) {
                $("#add_name").val(ui.item.name);
                return false;
            },
            select: function (event, ui) {
                $("#add_name").val(ui.item.name);
                $("#add_name").attr('readonly', true);
                $("#add_id").val(ui.item.id);
                $("#add_unit").val(ui.item.unit);
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

    //Append ingredient to list in form view
    $(function () {
        $('button[name="add_button"]').click(function () {
            var amount = $('#add_amount').val();
            if (Math.floor(amount) != amount || !($.isNumeric(amount))) {
                return;
            }
            var add = { id: $('#add_id').val(), name: $('#add_name').val(), amount: amount, unit: $('#add_unit').val() };
            var entry = add['amount'] + ' ' + add['unit'] + ' ' + add['name'];
            var element = '<li class="ingredient">' +
                '<input type="hidden" id="id" value="' + add['id'] + '">' +
                '<input type="hidden" id="name" value="' + add['name'] + '">' +
                '<input type="hidden" id="amount" value="' + add['amount'] + '">' +
                '<input type="hidden" id="unit" value="' + add['unit'] + '">' +
                '<div class="col-11">' + entry + '<button type="button" name="remove_button" ' +
                'class="close" aria-label="Close"><span aria-hidden="true">&times;</span>' +
                '</button></div></li>';
            $("#added_ingredients").append(element);
            $.fn.clearReadOnly();
        })
    });

    $(document).on('click', 'button[name="remove_button"]', function () {
        $(this).parent().parent().remove();
    });

    //Create the recipe
    $(document).on('click', 'button[name="create_button"], button[name="save_button"]', function () {
        var post_url;
        var success_message;

        if ($(this).is('button[name="create_button"]')) {
            post_url = "/recipes/create/";
            success_message = "<p>Recipe created!</p>";
        } else if ($(this).is('button[name="save_button"]')) {
            var recipe_id = $('#recipe_id').val();
            console.log(recipe_id);
            post_url = "/recipes/" + recipe_id + "/save/";
            success_message = "<p>Changes saved!</p>";
        }

        var recipe_name = $("#namefield").val();
        var instructions = $("#instrfield").val();
        var servings = $('#servingsfield').val();
        var ingredients = [];
        var new_ingredients = [];

        //Validate recipe name and servings
        if (recipe_name == '' || recipe_name.length < 3) {
            $("#error").children().remove();
            $("#error").append('<p><font color="red" size="1">Give your recipe a name of at least 2 characters.</font></p>');
            return;
        }
        if (servings < 1) {
            $("#error").children().remove();
            $("#error").append('<p><font color="red" size="1">Less than 1 servings?</font></p>');
            return;
        }

        //Collect ingredients
        var index = 0;
        $("#added_ingredients li.ingredient").each(function () {
            obj = {};
            $(this).children('input').each(function () {
                var attr = $(this).attr('id');
                obj[$(this).attr('id')] = $(this).val();
            });
            obj['index'] = index++;
            obj['category'] = "";
            obj['kcal'] = 0;
            ingredients.push(obj);
            if (obj['id'] == "") {
                new_ingredients.push(obj);
            }
        });

        //Validate ingredient list
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
                servings: servings,
                ingredients: ingredients
            }),
            type: 'POST',
            success: function (response) {
                $("#main_view").children().remove();
                $("#main_view").append(response);
            },
            error: function (error) {
                console.log(error);
                $("#main_view").children().remove();
                $("#main").append("<p>An error occurred</p>");
            }
        });
    });


    $('#add_name').click(function () {
        if ($("#add_name").is('[readonly]')) {
            $.fn.clearReadOnly();
        }
    });

    $.fn.clearReadOnly = function () {
        $("#add_name").attr('readonly', false);
        $("#add_name").val("");
        $("#add_unit").attr('readonly', false);
        $("#add_unit").val("");
        $("#add_id").val("");
        $("#add_amount").val("");

    }

});


$(document).ready(function () {

    //Autocomplete for ingredient name field
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
            var name = $('#add_name').val();
            var amount = $('#add_amount').val();
            var unit = $('#add_unit').val();
            if (name == "") {
                $('#alert-add').append($.fn.yellowAlert('Empty ingredient name.'));
                return;
            }
            if (name.length > 144) {
                $('#alert-add').append($.fn.yellowAlert('Ingredient name is too long.'));
                return;
            }
            if (Math.floor(amount) != amount || !($.isNumeric(amount)) || amount < 1) {
                $('#alert-add').append($.fn.yellowAlert('Amount is not a valid number.'));
                return;
            }
            if (name.match(illegal) || unit.match(illegal)) {
                $('#alert-add').append($.fn.yellowAlert('One field contains illegal characters.'));
                return;
            }
            var add = { id: $('#add_id').val(), name: name, amount: amount, unit: unit };
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

        if ($(this).is('button[name="create_button"]')) {
            post_url = "/recipes/create/";
        } else if ($(this).is('button[name="save_button"]')) {
            var recipe_id = $('#recipe_id').val();
            post_url = "/recipes/" + recipe_id + "/save/";
        }

        var recipe_name = $("#namefield").val();
        var instructions = $("#instrfield").val();
        var servings = $('#servingsfield').val();
        var ingredients = [];
        var new_ingredients = [];

        //Validate name, instructions and servings
        if (recipe_name == '' || recipe_name.length < 2) {
            $("#alert-create").children().remove();
            $("#alert-create").append($.fn.yellowAlert('Give a name of at least 2 characters.'));
            return;
        }
        if (recipe_name.length > 144) {
            $("#alert-create").children().remove();
            $("#alert-create").append($.fn.yellowAlert('Name is too long.'));
            return;
        }
        if (servings < 1 || !$.isNumeric(servings)) {
            $("#alert-create").children().remove();
            $("#alert-create").append($.fn.yellowAlert('Invalid amount of servings.'));
            return;
        }
        if (recipe_name.match(illegal) || instructions.match(illegal)) {
            $('#alert-create').append($.fn.yellowAlert('One field contains illegal characters.'));
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
            $("#alert-create").children().remove();
            $("#alert-create").append($.fn.yellowAlert('Add at least one ingredient.'));
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
                if (response == "OK") {
                    $("#alert-create").children().remove();
                    $("#alert-create").append($.fn.greenAlert('Changes saved!'));
                } else {
                    $("#main_view").children().remove();
                    $("#main_view").append(response);
                }
            },
            error: function (error) {
                console.log(error);
                $("#main_view").children().remove();
                $("#main").append($.fn.redAlert(error));
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


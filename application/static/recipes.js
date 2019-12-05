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
            term = term.toLowerCase();
            var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(term), "i");
            return $.grep(array, function (value) {
                return matcher.test(value.name);
            });
        };
    });


    //Append ingredient to list in form view
    var ingredients_index = $('#ingredients_size').val();
    console.log("ingredients_index: " + ingredients_index);
    $(function () {
        $('button[name="add_button"]').click(function () {
            var name = $('#add_name').val();
            var amount = $('#add_amount').val();
            var unit = $('#add_unit').val();

            //Validate ingredient input
            if (name == "" || name.length < 2) {
                $('#alert-add').append($.fn.yellowAlert('Ingredient name is too short.'));
                return;
            }
            if (name.length > 144) {
                $('#alert-add').append($.fn.yellowAlert('Ingredient name is too long.'));
                return;
            }
            if (!($.isNumeric(amount)) || amount <= 0 || amount > 1000000) {
                $('#alert-add').append($.fn.yellowAlert('Amount is not a valid number.'));
                return;
            }
            if (name.match(illegal) || unit.match(illegal)) {
                $('#alert-add').append($.fn.yellowAlert('One field contains illegal characters.'));
                return;
            }
            if (unit.length > 20) {
                $('#alert-add').append($.fn.yellowAlert('Unit name is too long.'));
                return;
            }

            //Add plaintext entry and hidden fields according to WTForms syntax requirements to ingredient list 
            var add = { id: $('#add_id').val(), name: name, amount: amount, unit: unit };
            var entry = add['amount'].toString() + ' ' + add['unit'] + ' ' + add['name'];
            var element = '<li class="ingredient">' +
                '<input type="hidden" id="id" name="ingredients-' + (ingredients_index) + '-ingredient_id" value="' + add['id'] + '">' +
                '<input type="hidden" id="ri_name" name="ingredients-' + (ingredients_index) + '-ri_name" value="' + add['name'] + '">' +
                '<input type="hidden" id="amount" name="ingredients-' + (ingredients_index) + '-amount" value="' + add['amount'] + '">' +
                '<input type="hidden" id="unit" name="ingredients-' + (ingredients_index) + '-unit" value="' + add['unit'] + '">' +
                '<div class="col-11">' + entry + '<button type="button" name="remove_button" ' +
                'class="close" aria-label="Close"><span aria-hidden="true">&times;</span>' +
                '</button></div></li>';
            $("#ingredients").append(element);
            ingredients_index++;
            $.fn.clearReadOnly();
        })
    });

    //Delete ingredient from list in form view
    $(document).on('click', 'button[name="remove_button"]', function () {
        $(this).parent().parent().remove();
    });

    //Clear autocomplete ingredient selection
    $('#add_name').click(function () {
        if ($("#add_name").is('[readonly]')) {
            $.fn.clearReadOnly();
        }
    });

    //Clear readonly ingredient fields
    $.fn.clearReadOnly = function () {
        $("#add_name").attr('readonly', false);
        $("#add_name").val("");
        $("#add_unit").attr('readonly', false);
        $("#add_unit").val("");
        $("#add_id").val("");
        $("#add_amount").val("");
    }

});


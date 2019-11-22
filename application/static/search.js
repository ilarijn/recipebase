$(document).ready(function () {

    $("#sform").submit(function (event) {
        if ((!$('#snam').is(':checked')
            && !$('#sing').is(':checked')
            && !$('#scat').is(':checked'))
            || $('#stext').val() == "") {
            event.preventDefault();
        }
        return;
    });
    
});
$.fn.yellowAlert = function (message) {
    return '<div class="alert alert-warning alert-dismissible fade show">' + message +
        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
        '</div>'
}

$.fn.greenAlert = function (message) {
    return '<div class="alert alert-success alert-dismissible fade show">' + message +
        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
        '</div>'
}

$.fn.redAlert = function (message) {
    return '<div class="alert alert-danger alert-dismissible fade show">' + message +
        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
        '</div>'
}

var illegal = '\[<>/\\\\;()\]'
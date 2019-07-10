$(document).ready(function () {
    let comma_allowed = null;
    let deleted_comma = false;

    $("#coin_input").on('keypress', e => {
        if (e.keyCode === 46 && (comma_allowed || deleted_comma)) {
            comma_allowed = false;
            deleted_comma = false;
            return;
        }

        if (e.keyCode >= 48 && e.keyCode <= 57) {
            if (comma_allowed === null) comma_allowed = true;
        } else {
            e.preventDefault();
        }
        return e;
    }).on('keyup', e => {
        let val = e.target.value;

        if (val.indexOf('.') === -1 && val.length > 0) {
            deleted_comma = true;
        }
    });

    let input = document.getElementById("coin_input");
    input.addEventListener("keyup", e => {
        if (e.keyCode === 13) {
            document.getElementById("submitEnter").click();
        }
    });
});
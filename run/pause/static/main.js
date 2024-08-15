document.getElementById('system').style.display = "none";
document.getElementById('netflix').style.display = "none";
document.getElementById('spotify').style.display = "none";

function menu(act) {
    document.getElementById('system').style.display = "none";
    document.getElementById('netflix').style.display = "none";
    document.getElementById('spotify').style.display = "none";
    document.getElementById(act).style.display = "block";
}



function on_response(response) {
    response = JSON.parse(response)
    if (response.translation) {
        alert(response.translation);
    }
}
function send_data(e, act) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/pause',
        data: {'act':act},
        success: on_response,
        error: function(error) {
            console.log('Send data error:', error);
        },
    });
}

function dfFunction() {
    console.log("Opening the SSE connection")
    var source = new EventSource("/df");
    source.onmessage = function(event) {
        sent_data = JSON.parse(event.data)

        bar = "#prog_0"
        $(bar).css('width', sent_data[0]+'%').attr('aria-valuenow', sent_data[0]);
        lbar = "#prog_0_label"
        $(lbar).text(sent_data[1]);
        channel = "#channel"
        $(channel).text('Current Channel: '+sent_data[2]);
        best_seen = "#best"
        $(best_seen).text('Best Seen: '+sent_data[3] + ' Time: ' + sent_data[4]);
        current_rssi = "#current_rssi"
        $(current_rssi).text('Current RSSI: '+sent_data[1]);
    }
}

function lockChannel() {
    $('a#lock_channel').on('click', function(e) {
        e.preventDefault();
        $.getJSON('/lock_channel');
    });
}


var mute = true;

function toggleAudio() {
    if (mute === true) {
        mute = false;
        $('#audio').text("Mute Audio");
    } else {
        mute = true;
        $('#audio').text("Start Audio");
    }
}

function adjustSound(oscillator, freq) {
    oscillator.frequency.value = freq;
}

function dfFunction() {
    console.log("Opening the SSE connection")
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    oscillator.type = "square";
    oscillator.frequency.setValueAtTime(440, audioCtx.currentTime); // value in hertz
    oscillator.start();
    var localMute = true;
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

        if (mute === false) {
            oscillator.connect(audioCtx.destination);
            adjustSound(oscillator, sent_data[0]*8);
        } else {
            oscillator.disconnect(audioCtx.destination);
        }

    }
}

function lockChannel() {
    $('a#lock_channel').on('click', function(e) {
        e.preventDefault();
        $.getJSON('/lock_channel');
    });
}

function oneSixEleven() {
    $('a#oneSixEleven').on('click', function(e) {
        e.preventDefault();
        $.getJSON('/one_six_eleven');
    });
}
function twoGHz() {
    $('a#twoGHz').on('click', function(e) {
        e.preventDefault();
        $.getJSON('/two_GHz');
    });
}
function fiveGHz() {
    $('a#fiveGHz').on('click', function(e) {
        e.preventDefault();
        $.getJSON('/five_GHz');
    });
}
function hopAll() {
    $('a#hopAll').on('click', function(e) {
        e.preventDefault();
        $.getJSON('/hop_all');
    });
}



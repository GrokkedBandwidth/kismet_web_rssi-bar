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

function checkTime(last_time) {
    if (last_time > 5) {
        $(bar)[0].classList.remove("progress-bar");
        $(bar)[0].classList.add("progress-bar-stale");

    } else {
        $(bar)[0].classList.add("progress-bar");
        $(bar)[0].classList.remove("progress-bar-stale");
    }
}

function dfFunction() {
    console.log("Opening the SSE connection")
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    oscillator.type = "square";
    oscillator.frequency.setValueAtTime(0, audioCtx.currentTime); // value in hertz
    oscillator.connect(audioCtx.destination);
    oscillator.start(audioCtx.currentTime);
    var source = new EventSource("/df");
    source.onmessage = function(event) {
        sent_data = JSON.parse(event.data);
        bar = "#prog_0";
        $(bar).css('width', sent_data[0]+'%').attr('aria-valuenow', sent_data[0]);
        lbar = "#prog_0_label";
        $(lbar).text(sent_data[1]);
        channel = "#channel";
        $(channel).text('Current Channel: '+sent_data[2]);
        best_seen = "#best";
        $(best_seen).text('Best Seen: '+sent_data[3] + ' Time: ' + sent_data[4]);
        current_rssi = "#current_rssi";
        $(current_rssi).text('Current RSSI: '+sent_data[1]);
        if (mute === false) {
            adjustSound(oscillator, sent_data[0]*8);
        } else {
            adjustSound(oscillator, 0);
        }
        if (sent_data[5] > 5) {
            $(bar)[0].classList.remove("progress-bar");
            $(bar)[0].classList.add("progress-bar-stale");
            adjustSound(oscillator, 0);
        } else {
            $(bar)[0].classList.add("progress-bar");
            $(bar)[0].classList.remove("progress-bar-stale");
        }
    }
}

$('a.channel').on('click', function(e) {
    e.preventDefault();
    var channel = e.currentTarget.textContent;
    var uuid = e.currentTarget.parentNode.classList[0];
    var xhr = new XMLHttpRequest();
    var url = encodeURIComponent(JSON.stringify({"uuid": uuid})) + "/" + encodeURIComponent(JSON.stringify({"channel": channel}));
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var buttons = e.currentTarget.parentNode.children;
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove("btn-primary");
            buttons[i].classList.add("btn-outline-primary");
        }
        e.currentTarget.classList.add("btn-primary");
        e.currentTarget.classList.remove("btn-outline-primary");
    }
};
xhr.send();
});

$('a.one').on('click', function(e) {
    e.preventDefault();
    var uuid = e.currentTarget.parentNode.classList[1];
    var xhr = new XMLHttpRequest();
    var url = "hop/" + encodeURIComponent(JSON.stringify({"uuid": uuid})) + "/" + encodeURIComponent(JSON.stringify({"option": "one"}));
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var buttons = $('div.' + uuid)[0].children;
        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i].textContent === "1" || buttons[i].textContent === "6" || buttons[i].textContent === "11") {
                buttons[i].classList.add("btn-primary");
                buttons[i].classList.remove("btn-outline-primary");
            } else {
                buttons[i].classList.remove("btn-primary");
                buttons[i].classList.add("btn-outline-primary");
            }
        }
    }
};
xhr.send();
});

$('a.two').on('click', function(e) {
    e.preventDefault();
    var uuid = e.currentTarget.parentNode.classList[1];
    console.log(uuid);
    var xhr = new XMLHttpRequest();
    var url = "hop/" + encodeURIComponent(JSON.stringify({"uuid": uuid})) + "/" + encodeURIComponent(JSON.stringify({"option": "two"}));
    console.log(url);
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var buttons = $('div.' + uuid)[0].children;
        var stop = false;
        for (var i = 0; i < buttons.length; i++) {
            if (stop === false && buttons[i].textContent.length < 4) {
                buttons[i].classList.remove("btn-outline-primary");
                buttons[i].classList.add("btn-primary");
            } else {
                buttons[i].classList.remove("btn-primary");
                buttons[i].classList.add("btn-outline-primary");
            }
            console.log(stop);
            if (buttons[i].textContent === "14") {
                stop = true;
            }
        }
    }
};
xhr.send();
});

$('a.three').on('click', function(e) {
    e.preventDefault();
    var uuid = e.currentTarget.parentNode.classList[1];
    var xhr = new XMLHttpRequest();
    var url = "hop/" + encodeURIComponent(JSON.stringify({"uuid": uuid})) + "/" + encodeURIComponent(JSON.stringify({"option": "three"}));
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var buttons = $('div.' + uuid)[0].children;
        console.log(buttons);
        var stop = true;
        for (var i = 0; i < buttons.length; i++) {
            if (stop === false && buttons[i].textContent.length < 4) {
                buttons[i].classList.remove("btn-outline-primary");
                buttons[i].classList.add("btn-primary");
            } else {
                buttons[i].classList.remove("btn-primary");
                buttons[i].classList.add("btn-outline-primary");
            }
            if (buttons[i].textContent === "14") {
                stop = false;
            }
        }
    }
};
xhr.send();
});
$('a.four').on('click', function(e) {
    e.preventDefault();
    var uuid = e.currentTarget.parentNode.classList[1];
    var xhr = new XMLHttpRequest();
    var url = "hop/" + encodeURIComponent(JSON.stringify({"uuid": uuid})) + "/" + encodeURIComponent(JSON.stringify({"option": "four"}));
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var buttons = $('div.' + uuid)[0].children;
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove("btn-outline-primary");
            buttons[i].classList.add("btn-primary");
        }
    }
};
xhr.send();
});


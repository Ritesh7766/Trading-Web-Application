function compute() {
   // if (!(document.getElementById('view').value === 'Fundamentals')) return;
    var latest_price = document.getElementById('latest_price');
    var previous_price = document.getElementById('previous_price');
    if (latest_price == null) return;
    var high = document.getElementById('high');
    var low = document.getElementById('low');

    var open = document.getElementById('open');
    var close = document.getElementById('close');

    var latest_vol = document.getElementById('latest-volume');
    var previous_vol = document.getElementById('previous-volume');

    var high52 = document.getElementById('high52');
    var low52 = document.getElementById('low52');

    if (latest_price.value >= previous_price.value) {
        latest_price.classList.add('high');
        previous_price.classList.add('low');
        document.getElementById('change').classList.add('high');
        document.getElementById('change_percent').classList.add('high');
    }
    else {
        latest_price.classList.add('low');
        previous_price.classList.add('high');
        document.getElementById('change').classList.add('low');
        document.getElementById('change_percent').classList.add('low');
    }

    if (high.value >= low.value) {
        high.classList.add('high');
        low.classList.add('low');
    }
    else {
        high.classList.add('low');
        low.classList.add('high');
    }

    if (open.value >= close.value) {
        open.classList.add('high');
        close.classList.add('low');
    }
    else {
        open.classList.add('low');
        close.classList.add('high');
    }

    if (latest_vol.value >= previous_vol.value) {
        latest_vol.classList.add('high');
        previous_vol.classList.add('low');
    }
    else {
        latest_vol.classList.add('low');
        previous_vol.classList.add('high');
    }

    if (high52.value >= low52.value) {
        high52.classList.add('high');
        low52.classList.add('low');
    }
    else {
        high52.classList.add('low');
        low52.classList.add('high');
    }

}
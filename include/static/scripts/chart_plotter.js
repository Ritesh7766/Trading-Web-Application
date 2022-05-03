Array.from(document.getElementsByClassName('trigger')).forEach(element =>  {
    element.addEventListener('click', async function() {
        var type = document.getElementById('plot').value.toLowerCase();
        var sym = this.getElementsByTagName('td')[1].innerText;
        document.getElementsByClassName('hidden-info')[0].getElementsByTagName('p')[0].innerText = sym;
        plot(type, sym, this);
    });
});

document.getElementById('plot').addEventListener('change', async function() {
    var type = this.value.toLowerCase();
    var sym = document.getElementsByClassName('hidden-info')[0].getElementsByTagName('p')[0].innerText;
    console.log(sym)
    plot(type, sym, this);
});


async function plot(type, sym, parent) {
    parent.style.cursor = 'wait';
    let response = await fetch(`/plot_${type}?sym=${sym}`);
    let data = await response.json();
    let html = data['file'];
    iframe = document.getElementById('specific-plot');
    iframe.src = "blank.html";
    iframe.contentDocument.write(html);
    iframe.contentDocument.close();
    parent.style.cursor = 'default';
}
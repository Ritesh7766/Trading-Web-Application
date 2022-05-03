function parseJSON(json_obj) {
    html = '';
    html += '<tr>' +
                '<th>' + 'Logo' + '</th>' +
                '<th>' + 'Symbol' + '</th>' +
                '<th>' + 'Shares' + '</th>' +
            '</tr>'
    for (var i in json_obj) {
        html += `<tr class = "trigger">
                    <td><img class="small-logo" src="${json_obj[i].logo}" alt=""></td>
                    <td>${json_obj[i].stock_id}</td>
                    <td>${json_obj[i].shares}</td>
                </tr>`
    }
    return html
}

document.getElementById('symbol').addEventListener('input', load_stocks_by_symbol);
document.getElementById('name').addEventListener('input', load_stocks_by_name);

async function load_stocks_by_symbol() {
    let response = await fetch(`/search_ownership?sym=${this.value}`);
    let data = await response.json();
    document.getElementById('ownership').innerHTML = parseJSON(data);
}

async function load_stocks_by_name() {
    let response = await fetch(`/search_ownership?nm=${this.value}`);
    let data = await response.json();
    document.getElementById('ownership').innerHTML = parseJSON(data);
}
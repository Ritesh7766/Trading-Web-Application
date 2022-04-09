document.getElementById('symbol').addEventListener('input', load_stocks_by_symbol);
document.getElementById('name').addEventListener('input', load_stocks_by_name);

async function load_stocks_by_symbol() {
    let response = await fetch(`/quote?sym=${this.value}`)
    let data = await response.json()
    console.log(data);
}

async function load_stocks_by_name() {
    let response = await fetch(`/quote?nm=${this.value}`)
    let data = await response.json()
    console.log(data);
}
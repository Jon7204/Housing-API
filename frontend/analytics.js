let chart

async function runAnalytics() {

    const location = document.getElementById("location").value
    const type = document.getElementById("property_type").value

    let params = new URLSearchParams()

    if (location) params.append("location", location)
    if (type) params.append("property_type", type)

    loadPriceTrend(params)
    loadExpensiveStreets(params)

}

async function loadPriceTrend(params) {

    const res = await fetch(`/analytics/price-trend?${params}`)
    const data = await res.json()

    const years = data.map(x => x.year)
    const prices = data.map(x => x.average_price)

    if (chart) chart.destroy()

    chart = new Chart(
        document.getElementById("price_chart"),
        {
            type: "line",
            data: {
                labels: years,
                datasets: [{
                    label: "Average Price",
                    data: prices
                }]
            }
        }
    )
}

async function loadExpensiveStreets(params) {

    const res = await fetch(`/analytics/top-expensive-streets?${params}`)
    const data = await res.json()

    const table = document.querySelector("#expensive_table tbody")
    table.innerHTML = ""

    data.forEach(r => {

        const row = `
        <tr>
            <td>${r.street}</td>
            <td>${r.town_city}</td>
            <td>${r.sales}</td>
            <td>£${r.average_price.toLocaleString()}</td>
        </tr>
        `

        table.innerHTML += row
    })
}
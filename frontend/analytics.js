let chart

let trendChart

async function searchPriceTrend() {

    const location = document.getElementById("trend_location").value
    const type = document.getElementById("trend_type").value

    let url = "/analytics/price-trend?"
    const params = []

    if (location) params.push(`location=${location}`)
    if (type) params.push(`property_type=${type}`)

    url += params.join("&")

    const response = await fetch(url)
    const data = await response.json()

    const years = data.map(d => d.year)
    const prices = data.map(d => d.average_price)

    if (trendChart) {
        trendChart.destroy()
    }

    const ctx = document.getElementById("price_chart")

    trendChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: years,
            datasets: [{
                label: "Average Price (£)",
                data: prices,
                tension: 0.2
            }]
        },
        options: {
            scales: {
                y: {
                    ticks: {
                        callback: function(value) {
                            return "£" + value.toLocaleString()
                        }
                    }
                }
            }
        }
    })
}

async function searchExpensiveStreets() {

    const location = document.getElementById("streets_location").value
    const type = document.getElementById("streets_type").value
    const minSales = document.getElementById("streets_min_sales").value
    const limit = document.getElementById("streets_limit").value

    let url = "/analytics/top-expensive-streets?"
    const params = []

    if (location) params.push(`location=${location}`)
    if (type) params.push(`property_type=${type}`)
    if (minSales) params.push(`min_sales=${minSales}`)
    if (limit) params.push(`limit=${limit}`)

    url += params.join("&")

    const response = await fetch(url)
    const data = await response.json()

    const table = document.querySelector("#expensive_table tbody")
    table.innerHTML = ""

    data.forEach(r => {

        const row = document.createElement("tr")

        row.innerHTML = `
            <td>${r.street}</td>
            <td>${r.town_city}</td>
            <td>${r.sales}</td>
            <td>£${Number(r.average_price).toLocaleString()}</td>
        `

        table.appendChild(row)

    })
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

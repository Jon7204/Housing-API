let trendChart = null
let trendDatasets = []
let trendLabels = []
let colorIndex = 0

const chartColors = [
    "#3366CC",
    "#DC3912",
    "#FF9900",
    "#109618",
    "#990099",
    "#0099C6",
    "#DD4477",
    "#66AA00"
]

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

    trendLabels = years

    const label = `${location || "All"} ${type || "All"}`

    if (trendChart && trendChart.data.datasets.some(d => d.label === label)) {
        alert("This dataset has already been added.")
        return
    }

    const color = chartColors[colorIndex % chartColors.length]
    colorIndex++

    const dataset = {
        label: label,
        data: prices,
        borderColor: color,
        backgroundColor: color,
        tension: 0.2
    }

    trendDatasets.push(dataset)

    addDatasetTag(label, color)

    renderTrendChart()
}

function renderTrendChart() {

    const ctx = document.getElementById("price_chart")

    if (trendChart) {
        trendChart.destroy()
    }

    trendChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: trendLabels,
            datasets: trendDatasets
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

function addDatasetTag(label, color) {

    const container = document.getElementById("active_datasets")

    const tag = document.createElement("div")
    tag.className = "dataset-tag"

    tag.style.backgroundColor = color

    tag.innerHTML = `
        ${label}
        <span onclick="removeDataset('${label}', this)">✖</span>
    `

    container.appendChild(tag)
}

function removeDataset(label, element) {

    trendDatasets = trendDatasets.filter(d => d.label !== label)

    element.parentElement.remove()

    renderTrendChart()
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
async function search() {
    const location = document.getElementById("location").value
    const min_price = document.getElementById("min_price").value
    const max_price = document.getElementById("max_price").value
    const start = document.getElementById("start_date").value
    const end = document.getElementById("end_date").value
    const sortValue = document.getElementById("sort").value
    const limit = document.getElementById("limit").value
    const offset = document.getElementById("offset").value
    const type = document.getElementById("trend_type").value
    const avgElement = document.getElementById("avg_price")

    let url = "/properties?"
    const params = []
    if (location) params.push(`location=${location}`)
    if (min_price) params.push(`min_price=${min_price}`)
    if (max_price) params.push(`max_price=${max_price}`)
    if (start) params.push(`start=${start}`)
    if (end) params.push(`end=${end}`)
    if (sortValue) params.push(`sort_by=${sortValue}`)
    if (limit) params.push(`limit=${limit}`)
    if (offset) params.push(`offset=${offset}`)
    if (type) params.push(`property_type=${type}`)
    url += params.join("&")

    console.log("Fetching:", url) // ← check this in DevTools Network/Console tab

    const response = await fetch(url)
    const table = document.querySelector("#results tbody")
    table.innerHTML = ""

    if (!response.ok) {
        if (response.status === 404) {
            table.innerHTML = `<tr><td colspan="9">No properties found matching the criteria.</td></tr>`
        } else {
            const err = await response.json()
            table.innerHTML = `<tr><td colspan="9">Error: ${err.detail}</td></tr>`
        }
        avgElement.textContent = "Average Price: No data"
        return
    }

    const data = await response.json()
    data.forEach(p => {
        const row = `
        <tr>
            <td>${p.id}</td>
            <td>£${p.price.toLocaleString()}</td>
            <td>${p.transfer_date}</td>
            <td>${p.postcode || ""}</td>
            <td>${p.paon || ""}</td>
            <td>${p.street || ""}</td>
            <td>${p.town_city || ""}</td>
            <td>${p.property_type || ""}</td>
            <td>${p.tenure || ""}</td>
        </tr>`
        table.innerHTML += row
    })

    if (location) {
        const avgResponse = await fetch(`/properties/average-price?location=${location}`)
        const avgData = await avgResponse.json()
        avgElement.textContent = avgData.average_price
            ? `Average Price: £${avgData.average_price.toLocaleString()}`
            : "Average Price: No data"
    } else {
        avgElement.textContent = "Average Price: (If Location)"
    }
}

document.getElementById("trend_type").addEventListener("change", search)
document.getElementById("sort").addEventListener("change", search)
document.getElementById("limit").addEventListener("input", search)
document.getElementById("offset").addEventListener("input", search) 

function resetFilters() {
    document.getElementById("location").value = ""
    document.getElementById("min_price").value = ""
    document.getElementById("max_price").value = ""
    document.getElementById("start_date").value = ""
    document.getElementById("end_date").value = ""
    document.getElementById("sort").selectedIndex = 0
    document.getElementById("trend_type").selectedIndex = 0
    document.getElementById("limit").value = ""
    document.getElementById("offset").value = ""
    document.querySelector("#results tbody").innerHTML = ""
    document.getElementById("avg_price").innerText = "Average Price: (If Location)"

}
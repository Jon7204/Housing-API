async function search() {

    const location = document.getElementById("location").value
    const min_price = document.getElementById("min_price").value
    const max_price = document.getElementById("max_price").value
    const start = document.getElementById("start_date").value
    const end = document.getElementById("end_date").value
    const sortValue = document.getElementById("sort").value
    const limit = document.getElementById("limit").value
    const offset = document.getElementById("offset").value

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

    url += params.join("&")

    const response = await fetch(url)
    const data = await response.json()

    const table = document.querySelector("#results tbody")
    table.innerHTML = ""

    data.forEach(p => {

        const row = `
        <tr>
            <td>${p.id}</td>
            <td>${p.town_city}</td>
            <td>${p.postcode}</td>
            <td>£${p.price}</td>
            <td>${p.transfer_date}</td>
            <td>${p.property_type}</td>
        </tr>
        `

        table.innerHTML += row
    })
}

document.getElementById("sort").addEventListener("change", search)
document.getElementById("limit").addEventListener("change", search)
document.getElementById("offset").addEventListener("change", search)
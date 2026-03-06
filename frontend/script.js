async function search() {

    const location = document.getElementById("location").value
    const min_price = document.getElementById("min_price").value
    const max_price = document.getElementById("max_price").value

    let url = "/properties?"

    if (location) url += `location=${location}&`
    if (min_price) url += `min_price=${min_price}&`
    if (max_price) url += `max_price=${max_price}&`

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
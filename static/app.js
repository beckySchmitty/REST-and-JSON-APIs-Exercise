const BASE_URL = "http://localhost:5000/api";

function generateDIV(cupcake) {
  return `
<div class="col-sm" data-cupcake-id=${cupcake.id}>
<div class="card" style="width: 18rem;">
    <img class="card-img-top" src="${cupcake.image}" alt="(no image provided)">
    <div class="card-body">
      <h5 class="card-title">${cupcake.flavor}</h5>
      <p class="card-text"> ${cupcake.size} / ${cupcake.rating}</p>
    </div>
  </div>`;
}


// get request to API for all cupcakes, then display on page
async function showCupcakesHTML() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    
    for (let cupcake of response.data.cupcakes) {
        let $newCupcake = $(generateDIV(cupcake));
        $("#cupcakes-list").append($newCupcake);
    }
    console.log(response.data)
}

$(showCupcakesHTML);

$( "#add-cupcake-form" ).submit(function( event ) {
  console.log("FORM SUBMITTED:", event);
  event.preventDefault();
});
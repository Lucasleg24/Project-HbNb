// Fonction pour obtenir les paramètres de l'URL
function getQueryParams() {
  const queryString = window.location.search;
  const params = new URLSearchParams(queryString);
  return {
      name: decodeURIComponent(params.get('name') || ""), // Décoder les caractères spéciaux
      price: params.get('price'),
      host: decodeURIComponent(params.get('host') || ""),
      description: decodeURIComponent(params.get('description') || ""),
      amenities: params.get('amenities') ? params.get('amenities').split(',') : []
  };
}

// Charger les informations de la place
function loadPlaceDetails() {
  const place = getQueryParams(); // Obtenir les données depuis l'URL
  if (place.name) {
      // Mettre à jour les détails de la propriété
      document.querySelector('#place-details h1').textContent = place.name;
      document.querySelector('#place-details .place-info:nth-of-type(1)').textContent = `Host: ${place.host}`;
      document.querySelector('#place-details .place-info:nth-of-type(2)').textContent = `Price per night: $${place.price}`;
      document.querySelector('#place-details .place-info:nth-of-type(3)').textContent = `Description: ${place.description}`;
      // Mettre à jour la liste des commodités
      const amenitiesList = document.querySelector('#place-details ul');
      amenitiesList.innerHTML = ''; // Nettoyer la liste existante
      place.amenities.forEach(amenity => {
          const li = document.createElement('li');
          li.textContent = amenity;
          amenitiesList.append(li);
      });
  } else {
      alert("No place details found! Make sure to pass valid parameters in the URL.");
  }
}

// Ajouter un écouteur d'événement pour charger les détails
document.addEventListener('DOMContentLoaded', () => {
  console.log("bouh");
  loadPlaceDetails(); // Appeler la fonction au chargement de la page
});

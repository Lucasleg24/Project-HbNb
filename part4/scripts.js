// URL LOGIN
const API_URL = 'http://127.0.0.1:5000/api/v1/auth/login';

const LOGIN_PAGE_URL = 'http://127.0.0.1:5500/part4/login.html';
const INDEX_PAGE_URL = 'http://127.0.0.1:5500/part4/index.html';
const PLACE_PAGE_URL = 'http://127.0.0.1:5500/part4/place.html';
const REVIEW_PAGE_URL = 'http://127.0.0.1:5500/part4/add_review.html';

const GET_ALL_PLACES = 'http://127.0.0.1:5000/api/v1/places';
const GET_PLACE = 'http://127.0.0.1:5000/api/v1/places'
const POST_REVIEW = 'http://127.0.0.1:5000/api/v1/reviews';
const GET_REVIEWS_FROM_PLACE = 'http://127.0.0.1:5000/api/v1/reviews/places/{place_id}';
const GET_USER_BY_ID = 'http://127.0.0.1:5000/api/v1/users';

const LOGIN = 'login.html';
const INDEX = 'index.html';
const PLACE = 'place.html';
const ADD_REVIEW = 'add_review.html';

// Fonction pour gérer les cookies
function setAuthCookie(token) {
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + 7);
    document.cookie = `token=${token}; expires=${expiryDate.toUTCString()}; path=/; SameSite=Strict`;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementsByClassName('login-button');
    console.log(loginLink[0]);

    if (!token) {
        console.log("Pas de token");
        loginLink[0].style.display = 'block';
    } else {
        console.log(token);
        loginLink[0].style.display = 'none';
    }
    fetchPlaces();
}
function getCookie(name) {
    // Function to get a cookie value by its name
    const cookies = document.cookie.split(";");
    console.log(cookies);
    for (cookie of cookies) {
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

async function loginRequest(event) {
    event.preventDefault()
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    console.log(email);
    if (email && password) {
            try {
                const formData = new FormData(event.target);
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email, password
                    })
                });
                const data = await response.json();
                console.log(data);

                if (response.ok && data.access_token) {
                    setAuthCookie(data.access_token);
                    window.location.href = 'index.html';
                } else {
                    const errorElement = document.getElementById('error-message');
                    if (errorElement) {
                        errorElement.textContent = data.message || 'Échec de la connexion';
                        errorElement.style.display = 'block';
                    } else {
                        alert('Échec de la connexion');
                    }
                }
            } catch (error) {
                console.error('Erreur de login:', error);
                alert('Erreur lors de la connexion');
            }
    }
}

function indexLoad() {
    console.log("test0");
    fetchPlaces();
}

async function fetchPlaces() {
    try {
        console.log("test1");
        const response = await fetch(GET_ALL_PLACES);
        console.log(response);

        if (!response.ok) {
            throw new Error(`Erreur HTTP : ${response.status}`);
        }
        console.log("test2");

        const places = await response.json();
        console.log(places);
        displayPlaces(places);
        return places;
    } catch (error) {
        console.error('Erreur de chargement des places :', error);
    }
}

function displayPlaces(places) {
  // récupère l'id "place-list" de la balise section de index.html
  const placesList = document.getElementById('places-list');
  // vide le contenu existant dans la section
  placesList.innerHTML = '';
  // boucle dans le dictionnaire "places", crée un élément div pour chaque lieu ajoute des class CSS pour le style
  // crée un attribut personnalisé pour le prix du lieu (pour le trier plus tard) et l'id de la place puis rempli le contenue HTML avec les infos du lieu
  places.forEach(place => {
    const placeElement = document.createElement('div');
    placeElement.classList.add('card', 'place-card');
    placeElement.dataset.price = place.price;
    placeElement.dataset.placeId = place.id;
    placeElement.innerHTML = `
      <h3 class="place-name">${place.title}</h3>
      <p class="place-price">Price per night: $${place.price}</p>
      <a href="place.html?place_id=${place.id}" class="button login-button">View Details</a>`;
    // Ajoute l'élément
    placesList.appendChild(placeElement);
  });
  priceFilter();
}

function priceFilter() {
    const priceSelect = document.getElementById('price-filter'); // récup filtre
    const placeCards = document.querySelectorAll('.place-card'); // récup les cartes de lieux

    // regarde si le filtre change si oui convertie la valeur en int
    priceSelect.addEventListener('change', (event) => {
      const selectedPrice = parseInt(event.target.value); // Convertir en nombre

      placeCards.forEach(card => { // Parcourt toutes les cartes
        const placePrice = parseInt(card.dataset.price); // Récup prix stocké dans la carte du lieu

        // si le prix de la place est inférieur ou égal au prix selectionné (0 si 'All' est select)
        if (selectedPrice === 0 || placePrice <= selectedPrice) {
          card.style.display = 'block'; // affiche la carte
        } else { // sinon
          card.style.display = 'none'; // cache la carte
        }
      });
    });
  }


async function getPlaceIdFromURL() {
    try {
      console.log("commence la récupération des infos");
      const url = new URL(window.location.href);
      const placeId = url.searchParams.get('place_id');
      console.log(placeId);
      console.log('placeId extrait:', placeId);
      const token = getCookie('token');
      const requestUrl = `${GET_PLACE}/${placeId}`;

      // Appel API avec fetch
      const response = await fetch(requestUrl, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      console.log(response);

      // Vérification de la réponse
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status} - ${await response.text()}`);
      }

      const data = await response.json();
      console.log("data contenair");
      console.log(data);
      return data;

    } catch (error) {
      console.error('Erreur dans getPlaceIdFromURL:', error);
      throw error;
    }
  }

  async function placeLoad() {
    try {
        console.log("début du test place")
      displayAddReview();
      const placeData = await getPlaceIdFromURL();
      console.log("vérification place data:");
      console.log(placeData);
      displayPlaceInfos(placeData);
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
    }
  }

  async function displayPlaceInfos(data) {
    console.log(data);
    console.log(data.price);
    const placeBucket = document.getElementById('place-details'); // Cible la section existante
    placeBucket.innerHTML = ''; // Vide le contenu actuel pour le remplacer

    // Ajout du titre
    const placeTitle = document.createElement('h1');
    placeTitle.textContent = data.title || 'Unknown Title'; // Utilise une clé "title" ou une valeur par défaut
    placeBucket.appendChild(placeTitle);

    // Création de la carte de détails
    const placeElement = document.createElement('div');
    placeElement.classList.add('details-card');
    console.log(placeElement.classList)

    // Ajout des informations dynamiques
    placeElement.innerHTML = `
      <p><strong>Host:</strong> ${await getUser(data.owner) || 'Unknown Host'}</p>
      <p><strong>Price per night:</strong> $${data.price || 'N/A'}</p>
      <p><strong>Description:</strong> ${data.description || 'No description available.'}</p>
      <p><strong>Amenities:</strong> ${data.amenities ? data.amenities.map(amenity => amenity.name).join(', ') : 'No amenities listed.'}</p>
    `;

    placeBucket.appendChild(placeElement); // Ajout de la carte à la section
    displayPlaceReviews(data); // appelle la fonction pour afficher les reviews de la place
  }

  function displayAddReview() {
    const token = getCookie('token');
    console.log("test displayAddreview");
    const addReviewSection = document.getElementById('add-review');
    if (!token) {
      addReviewSection.style.display = 'none';
    } else {
      addReviewSection.style.display = 'block';
    }
  }

  async function displayPlaceReviews(placeData) {
    const reviewsList = document.getElementById('reviews');
    reviewsList.innerHTML = '';
    try {
      const placeId = placeData.id;
      const requestUrl = `${GET_REVIEWS_FROM_PLACE}/${placeId}`;

      // Effectuer la requête pour obtenir les données de reviews
      const response = await fetch(requestUrl);
      if (!response.ok) {
        const titleElement = document.createElement('h2');
        titleElement.textContent = 'Reviews';
        reviewsList.appendChild(titleElement);
        const reviewCard = document.createElement('div');
        reviewCard.classList.add('review-card');
        reviewCard.innerHTML += `<p>No reviews available for this place.</p>`;
        reviewsList.appendChild(reviewCard);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reviewsData = await response.json();

      loadReviews(reviewsData);

    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  }

  async function loadReviews(datas) {
    const reviewsList = document.getElementById('reviews');

    // Vide tout le contenu existant (y compris le titre)
    reviewsList.innerHTML = '';

    // Ajout du titre de la section
    const titleElement = document.createElement('h2');
    titleElement.textContent = 'Reviews';
    reviewsList.appendChild(titleElement);

    // Ajout dynamique des cartes de review
    for (const data of datas) {
      const reviewCard = document.createElement('div');
      reviewCard.classList.add('review-card');

      // Remplit le contenu de la carte
      reviewCard.innerHTML = `
        <p><strong>${await getUser(data.owner_id)}:</strong></p>
        <p>${data.text}</p>
        <p>Rating: ${'★'.repeat(data.rating)}${'☆'.repeat(5 - data.rating)}</p>
      `;

      // Ajoute la carte au conteneur
      reviewsList.appendChild(reviewCard);
    }
  }

// Fonction pour récupérer un utilisateur
async function getUser(id) {
  const requestUrl = `${GET_USER_BY_ID}/${id.id}`;
  const token = getCookie('token');
  console.log(id);
  console.log(requestUrl);
  try {
    const response = await fetch(requestUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (!response.ok) {
      throw new Error(`Erreur HTTP ! statut : ${response.status}`);
    }
    const data = await response.json();
    const user = `${data.first_name} ${data.last_name}`;
    return user;

  } catch (error) {
    console.error('Erreur lors de la récupération de l\’utilisateur :', error);
    return null;
  }
}

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    // Récupère le nom du fichier depuis l'URL
    const currentPage = window.location.pathname.split('/').pop();
    if (document.body.id === "login-page") {
        loginRequest();
    }

    if (document.body.id === "index-page") {
        indexLoad();
    }

    if (document.body.id === "place-page"){
        placeLoad();
    }
});
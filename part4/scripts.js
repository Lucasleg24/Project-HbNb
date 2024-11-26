// URL LOGIN
const API_URL = 'http://127.0.0.1:5000/api/v1/auth/login';

const LOGIN_PAGE_URL = 'http://127.0.0.1:5500/part4/login.html';
const INDEX_PAGE_URL = 'http://127.0.0.1:5500/part4/index.html';
const PLACE_PAGE_URL = 'http://127.0.0.1:5500/part4/place.html';
const REVIEW_PAGE_URL = 'http://127.0.0.1:5500/part4/add_review.html';

const GET_ALL_PLACES = 'http://127.0.0.1:5000/api/v1/places';
const GET_PLACE = 'http://127.0.0.1:5000/api/v1/places/{place_id}'
const POST_REVIEW = 'http://127.0.0.1:5000/api/v1/reviews';
const GET_REVIEWS_FROM_PLACE = 'http://127.0.0.1:5000/api/v1/reviews/places/{place_id}';

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
    const placesList = document.getElementById('places-list');
    console.log(placesList);
    placesList.innerHTML = '';
    places.forEach(place => {
        const placeElement = document.createElement('div');
        placeElement.classList.add('card', 'place-card');
        placeElement.dataset.price = place.price;
        placeElement.dataset.placeId = place.id;
        placeElement.innerHTML = `
        <h3 class="place-name">${place.title}</h3>
        <p class="place-price">Price per night: $${place.price}</p>
        <a href="place.html" class="button login-button">View Details</a>`;
        placesList.appendChild(placeElement);
        console.log(placeElement);
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

//function init() {
    //console.log("Initializing..." + document.body.id);
    //if (document.body.id === "index-page") {
        //console.log("Loading index page...");
        //indexLoad();
    //}
//}

//document.addEventListener('DOMContentLoaded', init);

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    // Récupère le nom du fichier depuis l'URL
    const currentPage = window.location.pathname.split('/').pop();
    if (document.body.id === "login-page") {
      loginLoad();
    }

    if (document.body.id === "index-page") {
      indexLoad();
    }
});
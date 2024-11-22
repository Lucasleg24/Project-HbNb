// URL LOGIN
const API_URL = 'http://127.0.0.1:5000/api/v1/auth/login';
const LOGIN_PAGE_URL = 'http://127.0.0.1:5500/part4/front_end/login.html';
const INDEX_PAGE_URL = 'http://127.0.0.1:5500/part4/front_end/index.html';
const PLACE_PAGE_URL = 'http://127.0.0.1:5500/part4/front_end/place.html';
const REVIEW_PAGE_URL = 'http://127.0.0.1:5500/part4/front_end/add_review.html';

// Fonction pour gérer les cookies
function setAuthCookie(token) {
    const expiryDate = new Date();
    expiryDate.setDate(expiryDate.getDate() + 7);
    // crée un cooke avec le token et la date d'expiration disponible sur tout le site mais uniquement pour le site
    document.cookie = `token=${token}; expires=${expiryDate.toUTCString()}; path=/; SameSite=Strict`;
}

function loginRequest() {
    // Récupère le formulaire de login par son ID CSS
    const loginForm = document.getElementById('login-form');

    // si l'id existe dans la page
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            try {
                // Récupère les données du formulaire
                const formData = new FormData(event.target);
                // Envoie la requête au serveur
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    // Convertit les données du formulaire en JSON
                    body: JSON.stringify({
                        email: formData.get('email'),
                        password: formData.get('password')
                    })
                });
                // Récupère la réponse du serveur en JSON
                const data = await response.json();

                // Vérifie si la connexion est réussie
                if (response.ok && data.access_token) {
                    // Sauvegarde le token dans un cookie en appelant la fonction setAuthCookie
                    setAuthCookie(data.access_token);
                    // Redirige vers la page principale
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
        });
    }
}

// Vérification de l'URL avant d'appeler loginRequest
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.href === LOGIN_PAGE_URL) {
      console.log("LOGIN")
      loginRequest();
  }

    if (window.location.href === INDEX_PAGE_URL) {
      console.log("INDEX")
  }

    if (window.location.href === PLACE_PAGE_URL) {
      console.log("PLACE")
  }

    if (window.location.href === REVIEW_PAGE_URL) {
      console.log("REVIEW")
  }
});
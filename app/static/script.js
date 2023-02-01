const FILM_STATUS_CODE_TAKEN = 1;
const FILM_STATUS_CODE_FREE = 0;

const MODAL = document.getElementById('modal');
const PLACE_ROW = document.getElementById('place-row');
const PLACE_COLUMN = document.getElementById('place-column');
const PLACE_PRICE = document.getElementById('place-price');

let CURRENT_PLACE = {};

function fetchFilmInfo(filmName) {
    window.location.href = `/film/${filmName}`;
}

function mainPage() {
    window.location.href = '/';
}

function openOrderModal(place) {
    CURRENT_PLACE = place;
    if (place.status_code === FILM_STATUS_CODE_FREE) {
        document.getElementById('modal').style.display = 'flex';
        document.getElementById('place-row').innerHTML = `Ряд: ${place.row + 1}`;
        document.getElementById('place-column').innerHTML = `Место: ${place.column + 1}`;
        document.getElementById('place-price').innerHTML = `Цена: ${place.price}₽`;
    }
}

async function orderPlace() {
    const pathnameArray = window.location.pathname.split('/');
    const response = await fetch('/film/order_place/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'film_id': pathnameArray[pathnameArray.length - 1],
            'row': CURRENT_PLACE.row,
            'column': CURRENT_PLACE.column,
        }),
    });
    const data = await response.json();
    if (response.ok) {
        location.reload();
    }
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

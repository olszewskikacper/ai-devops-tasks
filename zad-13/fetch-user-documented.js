/**
 * @typedef {Object} UserData
 * @property {string} name - Imię i nazwisko użytkownika.
 * @property {string} email - Adres e-mail użytkownika.
 * @property {Date} lastLogin - Data i czas ostatniego logowania.
 */

/**
 * Pobiera dane użytkownika z API na podstawie jego identyfikatora.
 *
 * Wysyła żądanie GET na adres `https://api.example.com/users/{userId}`.
 * Błędy HTTP i błędy sieciowe są przechwytywane, logowane w konsoli,
 * a funkcja zwraca wtedy `null` zamiast zgłaszać wyjątek.
 *
 * @param {(string|number)} userId - Identyfikator użytkownika do pobrania.
 * @returns {Promise<UserData|null>} Obietnica z obiektem danych użytkownika
 *   lub `null`, jeśli żądanie się nie powiodło (status inny niż 2xx
 *   albo błąd sieci/parsowania JSON).
 *
 * @example
 * fetchUserData(42).then(user => {
 *   if (user) console.log(user.name, user.lastLogin);
 * });
 */
function fetchUserData(userId) {
  return fetch(`https://api.example.com/users/${userId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      return {
        name: data.name,
        email: data.email,
        lastLogin: new Date(data.lastLoginTimestamp)
      };
    })
    .catch(error => {
      console.error('Fetch error:', error);
      return null;
    });
}

// Oktet: 0-255 bez zer wiodących (np. "01" jest odrzucone).
const OCTET = '(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)';
const IPV4_REGEX = new RegExp(`^(?:${OCTET}\\.){3}${OCTET}$`);

/**
 * Sprawdza, czy podany napis jest poprawnym adresem IPv4 w notacji kropkowej.
 *
 * @param {string} ip - Adres do sprawdzenia, np. "192.168.1.1".
 * @returns {boolean} `true`, jeśli adres jest poprawny.
 */
function isValidIPv4(ip) {
  return typeof ip === 'string' && IPV4_REGEX.test(ip);
}

module.exports = isValidIPv4;

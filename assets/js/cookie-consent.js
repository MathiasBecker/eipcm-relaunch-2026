/**
 * EIPCM Cookie Consent Banner
 * Lightweight, GDPR-compliant cookie consent solution.
 * Stores user preference in localStorage.
 */
(function () {
  'use strict';

  // Check if user already made a choice
  if (localStorage.getItem('eipcm_cookie_consent')) return;

  // Inject CSS
  var style = document.createElement('style');
  style.textContent = [
    '#eipcm-cookie-banner {',
    '  position: fixed;',
    '  bottom: 0;',
    '  left: 0;',
    '  right: 0;',
    '  z-index: 99999;',
    '  background: #1a1a2e;',
    '  color: #e5e5e5;',
    '  font-family: "Open Sans", sans-serif;',
    '  font-size: 0.9rem;',
    '  line-height: 1.5;',
    '  padding: 1.25rem 1.5rem;',
    '  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.25);',
    '  transform: translateY(100%);',
    '  transition: transform 0.4s ease-out;',
    '}',
    '#eipcm-cookie-banner.visible {',
    '  transform: translateY(0);',
    '}',
    '#eipcm-cookie-banner .cookie-inner {',
    '  max-width: 1200px;',
    '  margin: 0 auto;',
    '  display: flex;',
    '  align-items: center;',
    '  gap: 1.5rem;',
    '  flex-wrap: wrap;',
    '}',
    '#eipcm-cookie-banner .cookie-text {',
    '  flex: 1 1 400px;',
    '}',
    '#eipcm-cookie-banner .cookie-text a {',
    '  color: #90BB0A;',
    '  text-decoration: underline;',
    '}',
    '#eipcm-cookie-banner .cookie-text a:hover {',
    '  color: #a8d40b;',
    '}',
    '#eipcm-cookie-banner .cookie-buttons {',
    '  display: flex;',
    '  gap: 0.75rem;',
    '  flex-shrink: 0;',
    '  flex-wrap: wrap;',
    '}',
    '#eipcm-cookie-banner .btn-cookie {',
    '  padding: 0.5rem 1.25rem;',
    '  border-radius: 0.5rem;',
    '  border: none;',
    '  cursor: pointer;',
    '  font-family: "Open Sans", sans-serif;',
    '  font-size: 0.85rem;',
    '  font-weight: 600;',
    '  transition: background 0.2s, color 0.2s;',
    '  white-space: nowrap;',
    '}',
    '#eipcm-cookie-banner .btn-accept {',
    '  background: #90BB0A;',
    '  color: #fff;',
    '}',
    '#eipcm-cookie-banner .btn-accept:hover {',
    '  background: #7da509;',
    '}',
    '#eipcm-cookie-banner .btn-necessary {',
    '  background: transparent;',
    '  color: #e5e5e5;',
    '  border: 1px solid #555;',
    '}',
    '#eipcm-cookie-banner .btn-necessary:hover {',
    '  border-color: #90BB0A;',
    '  color: #90BB0A;',
    '}',
    '@media (max-width: 576px) {',
    '  #eipcm-cookie-banner .cookie-inner {',
    '    flex-direction: column;',
    '    align-items: stretch;',
    '    text-align: center;',
    '  }',
    '  #eipcm-cookie-banner .cookie-buttons {',
    '    justify-content: center;',
    '  }',
    '}'
  ].join('\n');
  document.head.appendChild(style);

  // Build banner HTML
  var banner = document.createElement('div');
  banner.id = 'eipcm-cookie-banner';
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-label', 'Cookie-Einstellungen');
  banner.innerHTML =
    '<div class="cookie-inner">' +
      '<div class="cookie-text">' +
        'Diese Website verwendet Cookies, um die bestm\u00F6gliche Funktionalit\u00E4t zu gew\u00E4hrleisten. ' +
        '<a href="privacy.html">Mehr erfahren</a>' +
      '</div>' +
      '<div class="cookie-buttons">' +
        '<button class="btn-cookie btn-accept" id="cookie-accept-all">Alle akzeptieren</button>' +
        '<button class="btn-cookie btn-necessary" id="cookie-necessary">Nur notwendige</button>' +
      '</div>' +
    '</div>';

  document.body.appendChild(banner);

  // Slide in after a short delay
  setTimeout(function () {
    banner.classList.add('visible');
  }, 500);

  // Handle button clicks
  function handleConsent(level) {
    localStorage.setItem('eipcm_cookie_consent', level);
    localStorage.setItem('eipcm_cookie_consent_date', new Date().toISOString());
    banner.classList.remove('visible');
    setTimeout(function () {
      banner.remove();
    }, 400);
  }

  document.getElementById('cookie-accept-all').addEventListener('click', function () {
    handleConsent('all');
  });

  document.getElementById('cookie-necessary').addEventListener('click', function () {
    handleConsent('necessary');
  });
})();

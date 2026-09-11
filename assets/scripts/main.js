(() => {
  'use strict';

  document.querySelectorAll('.fallback-image').forEach((image) => {
    const figure = image.closest('figure');
    const frame = image.closest('.photo-frame');
    const caption = figure.querySelector('.photo-caption');
    const credit = figure.querySelector('.photo-credit');
    const status = frame.querySelector('.photo-status');
    const primary = image.getAttribute('src');
    const fallback = image.dataset.fallback;
    let fallbackTried = false;

    function handleError() {
      if (fallbackTried || !fallback || fallback === primary) {
        image.removeEventListener('error', handleError);
        image.hidden = true;
        frame.classList.add('image-missing');
        status.textContent = 'Foto belum tersedia';
        caption.textContent = 'Foto untuk bagian ini belum tersedia.';
        credit.hidden = true;
        return;
      }

      fallbackTried = true;
      image.alt = image.dataset.fallbackAlt;
      caption.textContent = image.dataset.fallbackCaption;
      credit.textContent = image.dataset.fallbackCredit;
      credit.href = image.dataset.fallbackSource;
      image.src = fallback;
    }

    image.addEventListener('error', handleError);

    // A cached failure may precede this deferred script.
    if (image.complete && image.naturalWidth === 0) handleError();
  });
})();

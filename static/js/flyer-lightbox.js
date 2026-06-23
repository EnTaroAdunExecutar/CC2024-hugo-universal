/* Flyer Lightbox JavaScript */
(function() {
  'use strict';

  // Create lightbox modal element
  function createLightboxModal() {
    if (document.getElementById('flyer-lightbox')) {
      return; // Already exists
    }

    const modal = document.createElement('div');
    modal.id = 'flyer-lightbox';
    modal.className = 'flyer-lightbox-modal';
    modal.innerHTML = `
      <span class="flyer-lightbox-close" title="Schließen (ESC)">&times;</span>
      <img class="flyer-lightbox-content" alt="">
      <div class="flyer-lightbox-caption"></div>
    `;
    document.body.appendChild(modal);

    return modal;
  }

  // Initialize lightbox
  function initLightbox() {
    const modal = createLightboxModal();
    if (!modal) return;

    const modalImg = modal.querySelector('.flyer-lightbox-content');
    const captionText = modal.querySelector('.flyer-lightbox-caption');
    const closeBtn = modal.querySelector('.flyer-lightbox-close');

    // Handle clicks on flyer images
    document.addEventListener('click', function(e) {
      const trigger = e.target.closest('.flyer-lightbox-trigger');
      if (trigger) {
        e.preventDefault();
        const img = trigger.querySelector('img');
        modal.classList.add('active');
        modalImg.src = img.src;
        modalImg.alt = img.alt;
        captionText.textContent = img.alt;
        document.body.style.overflow = 'hidden'; // Prevent scrolling
      }
    });

    // Close lightbox on click
    function closeLightbox() {
      modal.classList.remove('active');
      document.body.style.overflow = ''; // Restore scrolling
    }

    closeBtn.addEventListener('click', closeLightbox);

    // Close on background click
    modal.addEventListener('click', function(e) {
      if (e.target === modal) {
        closeLightbox();
      }
    });

    // Close on ESC key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeLightbox();
      }
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLightbox);
  } else {
    initLightbox();
  }
})();

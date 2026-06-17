/**
 * Auto-scroll Stadtradeln widgets to center the highlighted team/municipality
 */
(function() {
  'use strict';

  function centerHighlightedRow() {
    document.querySelectorAll('.stadtradeln-widget .ranking-list').forEach(list => {
      const highlighted = list.querySelector('.ranking-row.our-team');
      if (!highlighted) return;

      const listHeight = list.clientHeight;
      const rowTop = highlighted.offsetTop;
      const rowHeight = highlighted.offsetHeight;

      // Center the row in the visible area
      const scrollTo = rowTop - (listHeight / 2) + (rowHeight / 2);
      list.scrollTop = Math.max(0, scrollTo);
    });
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', centerHighlightedRow);
  } else {
    centerHighlightedRow();
  }
})();

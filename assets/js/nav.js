document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('.nav-links a');
  const current = window.location.pathname;

  links.forEach(link => {
    const href = link.getAttribute('href');
    if (!href || href === '#') return;

    // Resolve the href relative to the current page
    const resolved = new URL(href, window.location.href).pathname;

    // Match exact page or index of directory
    const isMatch =
      current === resolved ||
      (resolved.endsWith('/') && current + '/' === resolved) ||
      (current.endsWith('/') && current === resolved + '/');

    if (isMatch) link.classList.add('active');
  });
});

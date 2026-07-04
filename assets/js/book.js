class BookReader {
  constructor() {
    this.pages = Array.from(document.querySelectorAll('.page'));
    this.total = this.pages.length;
    this.current = -1;
    this.animating = false;
    this.touchStartX = 0;
    this.touchStartY = 0;

    if (this.total === 0) return;

    this.prevBtn = document.getElementById('btn-prev');
    this.nextBtn = document.getElementById('btn-next');
    this.counter = document.getElementById('page-counter');
    this.progressFill = document.getElementById('progress-fill');

    this.showPage(0, null);
    this.bindEvents();
  }

  showPage(index, direction) {
    if (this.animating || index < 0 || index >= this.total || index === this.current) return;

    if (direction === null) {
      // Initial load — no previous page to transition from, just show it.
      this.pages[index].classList.add('show');
      this.current = index;
      this.updateUI();
      return;
    }

    this.animating = true;
    const goingNext = direction === 'next';
    const fromPage = this.pages[this.current];
    this.current = index;
    const toPage = this.pages[this.current];

    // Both pages are visible at once: the outgoing one flips away on
    // its spine edge, revealing the incoming one already sitting beneath it.
    toPage.classList.add('show', 'reveal-in');
    fromPage.classList.add('show');
    void fromPage.offsetWidth; // force reflow so the flip animation triggers
    fromPage.classList.add(goingNext ? 'flip-next-out' : 'flip-prev-out');

    const FLIP_DURATION = 560;
    setTimeout(() => {
      fromPage.classList.remove('show', 'flip-next-out', 'flip-prev-out');
      toPage.classList.remove('reveal-in');
      this.animating = false;
    }, FLIP_DURATION);

    this.updateUI();
  }

  next() { this.showPage(this.current + 1, 'next'); }
  prev() { this.showPage(this.current - 1, 'prev'); }

  updateUI() {
    // Counter
    if (this.counter) {
      this.counter.textContent = this.current === 0
        ? 'Cover'
        : `${this.current} / ${this.total - 1}`;
    }

    // Buttons
    if (this.prevBtn) this.prevBtn.disabled = this.current === 0;
    if (this.nextBtn) this.nextBtn.disabled = this.current === this.total - 1;

    // Progress bar
    if (this.progressFill) {
      const pct = this.total <= 1 ? 100 : (this.current / (this.total - 1)) * 100;
      this.progressFill.style.width = `${pct}%`;
    }
  }

  bindEvents() {
    this.prevBtn?.addEventListener('click', () => this.prev());
    this.nextBtn?.addEventListener('click', () => this.next());

    // Keyboard
    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') this.next();
      if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   this.prev();
    });

    // Touch / swipe
    const container = document.querySelector('.book-container');
    if (!container) return;

    container.addEventListener('touchstart', e => {
      this.touchStartX = e.touches[0].clientX;
      this.touchStartY = e.touches[0].clientY;
    }, { passive: true });

    container.addEventListener('touchend', e => {
      const dx = e.changedTouches[0].clientX - this.touchStartX;
      const dy = e.changedTouches[0].clientY - this.touchStartY;
      if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 48) {
        dx < 0 ? this.next() : this.prev();
      }
    }, { passive: true });
  }
}

document.addEventListener('DOMContentLoaded', () => new BookReader());

class BookReader {
  constructor() {
    this.pages = Array.from(document.querySelectorAll('.page'));
    this.total = this.pages.length;
    this.current = 0;
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
    if (this.animating || index < 0 || index >= this.total) return;
    this.animating = true;

    this.pages[this.current].style.display = 'none';
    this.pages[this.current].classList.remove('active', 'dir-prev');

    this.current = index;
    const page = this.pages[this.current];
    page.style.display = '';
    page.classList.remove('dir-prev');

    if (direction === 'prev') page.classList.add('dir-prev');

    // Force reflow so animation triggers
    void page.offsetWidth;
    page.classList.add('active');

    // Re-enable after animation
    setTimeout(() => { this.animating = false; }, 420);

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

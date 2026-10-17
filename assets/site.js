(() => {
  const root = document.documentElement;
  const body = document.body;
  root.classList.add('js');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const progress = document.querySelector('.site-progress');
  const updateProgress = () => {
    if (!progress) return;
    const available = document.documentElement.scrollHeight - window.innerHeight;
    const value = available > 0 ? Math.min(window.scrollY / available, 1) : 0;
    progress.style.transform = `scaleX(${value})`;
  };
  addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();

  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      links.classList.toggle('open', !open);
    });
    links.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      links.classList.remove('open');
    }));
  }

  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href');
    const homeMatch = path === 'index.html' && href === 'index.html';
    const productMatch = ['products.html', 'winpilot.html', 'winheart.html', 'clipvault.html', 'winqor.html', 'tradingx.html'].includes(path) && href === 'products.html';
    if (homeMatch || productMatch || href === path) link.setAttribute('aria-current', 'page');
  });

  const reveals = [...document.querySelectorAll('[data-reveal]')];
  reveals.forEach((element, index) => element.style.setProperty('--delay', `${Math.min(index % 5, 4) * 70}ms`));
  if (reducedMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(element => element.classList.add('is-visible'));
  } else {
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: .11, rootMargin: '0px 0px -4% 0px' });
    reveals.forEach(element => {
      const rect = element.getBoundingClientRect();
      if (rect.top < window.innerHeight + 100 && rect.bottom > -100) {
        element.classList.add('is-visible');
      } else {
        revealObserver.observe(element);
      }
    });
  }

  if (!reducedMotion && matchMedia('(pointer:fine)').matches) {
    addEventListener('pointermove', event => {
      root.style.setProperty('--mx', `${event.clientX}px`);
      root.style.setProperty('--my', `${event.clientY}px`);
    }, { passive: true });

    document.querySelectorAll('[data-tilt]').forEach(card => {
      card.addEventListener('pointermove', event => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - .5;
        const y = (event.clientY - rect.top) / rect.height - .5;
        card.style.transform = `perspective(900px) rotateX(${-y * 3.5}deg) rotateY(${x * 4.5}deg) translateY(-5px)`;
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });

    document.querySelectorAll('[data-magnetic]').forEach(button => {
      button.addEventListener('pointermove', event => {
        const rect = button.getBoundingClientRect();
        const x = event.clientX - (rect.left + rect.width / 2);
        const y = event.clientY - (rect.top + rect.height / 2);
        button.style.transform = `translate(${x * .075}px, ${y * .1 - 3}px) scale(1.015)`;
      });
      button.addEventListener('pointerleave', () => { button.style.transform = ''; });
    });
  }

  document.querySelectorAll('.toggle-demo').forEach(item => {
    item.addEventListener('click', () => {
      item.classList.toggle('on');
      item.setAttribute('aria-checked', String(item.classList.contains('on')));
    });
  });

  document.querySelectorAll('[data-contact-form]').forEach(form => {
    form.addEventListener('submit', event => {
      event.preventDefault();
      const data = new FormData(form);
      const name = String(data.get('name') || '').trim();
      const email = String(data.get('email') || '').trim();
      const message = String(data.get('message') || '').trim();
      const subject = encodeURIComponent(`Project inquiry from ${name || 'website visitor'}`);
      const bodyText = encodeURIComponent(`Name: ${name}\nEmail: ${email}\n\n${message}`);
      location.href = `mailto:winpilotai@gmail.com?subject=${subject}&body=${bodyText}`;
    });
  });

  body.classList.add('is-ready');
})();

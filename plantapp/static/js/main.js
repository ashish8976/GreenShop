// =============================================
//   GreenShop - Main JavaScript
// =============================================

document.addEventListener('DOMContentLoaded', () => {

  // =============================================
  // CART STATE
  // =============================================
  let cart = [
    { id: 1, name: 'Monstera Deliciosa', price: 649, qty: 1, emoji: '🌿' },
    { id: 2, name: 'Peace Lily', price: 399, qty: 2, emoji: '🌸' },
  ];
  let wishlist = [3, 5];

  // =============================================
  // NAVBAR - HAMBURGER MENU
  // =============================================
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      mobileNav.classList.toggle('open');
      hamburger.classList.toggle('active');
    });
  }

  // Close mobile nav on outside click
  document.addEventListener('click', (e) => {
    if (mobileNav && !mobileNav.contains(e.target) && !hamburger.contains(e.target)) {
      mobileNav.classList.remove('open');
    }
  });

  // Active nav link
  const navLinks = document.querySelectorAll('.navbar-menu a, .mobile-nav a');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
      if (mobileNav) mobileNav.classList.remove('open');
    });
  });

  // =============================================
  // CART SIDEBAR
  // =============================================
  const cartOverlay = document.getElementById('cartOverlay');
  const cartBtn = document.getElementById('cartBtn');
  const cartClose = document.getElementById('cartClose');

  function openCart() {
    if (cartOverlay) cartOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    renderCart();
  }

  function closeCart() {
    if (cartOverlay) cartOverlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (cartBtn) cartBtn.addEventListener('click', openCart);
  if (cartClose) cartClose.addEventListener('click', closeCart);
  if (cartOverlay) {
    cartOverlay.addEventListener('click', (e) => {
      if (e.target === cartOverlay) closeCart();
    });
  }

  function renderCart() {
    const cartItemsEl = document.getElementById('cartItems');
    const cartCountEl = document.querySelectorAll('.cart-count');
    if (!cartItemsEl) return;

    const totalItems = cart.reduce((s, i) => s + i.qty, 0);
    cartCountEl.forEach(el => el.textContent = totalItems);

    if (cart.length === 0) {
      cartItemsEl.innerHTML = `
        <div style="text-align:center;padding:60px 20px;color:var(--text-light);">
          <div style="font-size:60px;margin-bottom:16px;">🛒</div>
          <h4 style="font-family:'Playfair Display',serif;color:var(--green-dark);margin-bottom:8px;">Your cart is empty</h4>
          <p style="font-size:14px;">Add some beautiful plants!</p>
        </div>`;
      updateCartTotals();
      return;
    }

    cartItemsEl.innerHTML = cart.map(item => `
      <div class="cart-item" data-id="${item.id}">
        <div class="cart-item-img">${item.emoji}</div>
        <div class="cart-item-info">
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-price">₹${item.price.toLocaleString()}</div>
          <div class="cart-qty">
            <button class="qty-btn" onclick="changeQty(${item.id}, -1)">−</button>
            <span class="qty-num">${item.qty}</span>
            <button class="qty-btn" onclick="changeQty(${item.id}, 1)">+</button>
          </div>
        </div>
        <button class="cart-item-del" onclick="removeFromCart(${item.id})">
          <i class="fas fa-trash-alt"></i>
        </button>
      </div>
    `).join('');

    updateCartTotals();
  }

  function updateCartTotals() {
    const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
    const shipping = cart.length > 0 ? 99 : 0;
    const discount = cart.length > 0 ? 50 : 0;
    const total = subtotal + shipping - discount;

    const el = (id) => document.getElementById(id);
    if (el('cartSubtotal')) el('cartSubtotal').textContent = `₹${subtotal.toLocaleString()}`;
    if (el('cartShipping')) el('cartShipping').textContent = `₹${shipping}`;
    if (el('cartDiscount')) el('cartDiscount').textContent = `-₹${discount}`;
    if (el('cartTotal')) el('cartTotal').textContent = `₹${total.toLocaleString()}`;
  }

  window.changeQty = (id, delta) => {
    const item = cart.find(i => i.id === id);
    if (!item) return;
    item.qty = Math.max(1, item.qty + delta);
    renderCart();
  };

  window.removeFromCart = (id) => {
    cart = cart.filter(i => i.id !== id);
    renderCart();
    showToast('Item removed from cart', '🗑️');
  };

  window.addToCart = (id, name, price, emoji) => {
    const existing = cart.find(i => i.id === id);
    if (existing) {
      existing.qty++;
    } else {
      cart.push({ id, name, price, qty: 1, emoji });
    }
    renderCart();
    showToast(`${name} added to cart!`, '🛒');
    openCart();
  };

  // =============================================
  // WISHLIST TOGGLE
  // =============================================
  window.toggleWishlist = (id, btn) => {
    if (wishlist.includes(id)) {
      wishlist = wishlist.filter(w => w !== id);
      btn.style.color = '';
      showToast('Removed from wishlist', '💔');
    } else {
      wishlist.push(id);
      btn.style.color = '#e63946';
      showToast('Added to wishlist!', '❤️');
    }
    updateWishlistCount();
  };

  function updateWishlistCount() {
    const wEl = document.querySelectorAll('.wishlist-count');
    wEl.forEach(el => el.textContent = wishlist.length);
  }

  // =============================================
  // PRODUCT FILTER TABS
  // =============================================
  const filterBtns = document.querySelectorAll('.filter-btn');
  const productCards = document.querySelectorAll('.product-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;

      productCards.forEach(card => {
        if (filter === 'all' || card.dataset.category === filter) {
          card.style.display = 'block';
          card.style.animation = 'fadeInUp 0.4s ease both';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // =============================================
  // SCROLL TO TOP
  // =============================================
  const scrollTopBtn = document.getElementById('scrollTop');

  window.addEventListener('scroll', () => {
    if (scrollTopBtn) {
      if (window.scrollY > 400) scrollTopBtn.classList.add('visible');
      else scrollTopBtn.classList.remove('visible');
    }
  });

  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  
  // =============================================
  // LOGIN / REGISTER MODAL
  // =============================================
  const loginModal = document.getElementById('loginModal');
  const loginBtn = document.getElementById('loginBtn');
  const modalClose = document.getElementById('modalClose');
  const switchToRegister = document.getElementById('switchToRegister');
  const switchToLogin = document.getElementById('switchToLogin');
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');

  function openModal() {
    if (loginModal) { loginModal.classList.add('open'); document.body.style.overflow = 'hidden'; }
  }
  function closeModal() {
    if (loginModal) { loginModal.classList.remove('open'); document.body.style.overflow = ''; }
  }

  if (loginBtn) loginBtn.addEventListener('click', openModal);
  if (modalClose) modalClose.addEventListener('click', closeModal);
  if (loginModal) loginModal.addEventListener('click', (e) => { if (e.target === loginModal) closeModal(); });

  if (switchToRegister) {
    switchToRegister.addEventListener('click', () => {
      loginForm.style.display = 'none';
      registerForm.style.display = 'block';
    });
  }
  if (switchToLogin) {
    switchToLogin.addEventListener('click', () => {
      registerForm.style.display = 'none';
      loginForm.style.display = 'block';
    });
  }

  // Form submission simulation
  document.querySelectorAll('.btn-form').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      closeModal();
      showToast('Welcome to GreenShop! 🌿', '✅');
    });
  });

  // =============================================
  // COUPON CODE
  // =============================================
  const couponBtn = document.getElementById('applyCoupon');
  if (couponBtn) {
    couponBtn.addEventListener('click', () => {
      const input = document.getElementById('couponInput');
      const code = input ? input.value.trim().toUpperCase() : '';
      if (code === 'GREEN10') {
        showToast('Coupon applied! 10% discount added 🎉', '✅');
        if (input) input.value = '';
      } else if (code === '') {
        showToast('Please enter a coupon code', '⚠️');
      } else {
        showToast('Invalid coupon code', '❌');
      }
    });
  }

  // =============================================
  // NEWSLETTER
  // =============================================
  const newsletterBtn = document.getElementById('newsletterBtn');
  if (newsletterBtn) {
    newsletterBtn.addEventListener('click', () => {
      const input = document.getElementById('newsletterInput');
      const email = input ? input.value.trim() : '';
      if (email && email.includes('@')) {
        showToast('Thank you for subscribing! 🌱', '✅');
        if (input) input.value = '';
      } else {
        showToast('Please enter a valid email address', '⚠️');
      }
    });
  }

  // =============================================
  // CHECKOUT BUTTON
  // =============================================
  const checkoutBtn = document.getElementById('checkoutBtn');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
      if (cart.length === 0) {
        showToast('Your cart is empty!', '⚠️');
        return;
      }
      closeCart();
      showToast('Redirecting to checkout... 🚀', '✅');
    });
  }

  // =============================================
  // TOAST NOTIFICATIONS
  // =============================================
  function showToast(message, icon = '✅') {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>${icon}</span> ${message}`;
    toast.style.cssText = `
      position:fixed;bottom:32px;left:50%;transform:translateX(-50%) translateY(20px);
      background:var(--green-dark);color:white;
      padding:14px 26px;border-radius:30px;
      font-family:'DM Sans',sans-serif;font-size:14px;font-weight:500;
      box-shadow:0 8px 32px rgba(0,0,0,0.18);
      z-index:9999;display:flex;align-items:center;gap:10px;
      opacity:0;transition:all 0.35s cubic-bezier(0.4,0,0.2,1);
      white-space:nowrap;
    `;
    document.body.appendChild(toast);
    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
    });
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(20px)';
      setTimeout(() => toast.remove(), 350);
    }, 3000);
  }

  // =============================================
  // SCROLL ANIMATIONS
  // =============================================
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.cat-card, .product-card, .feature-card, .testi-card').forEach(el => {
    observer.observe(el);
  });

  // =============================================
  // PASSWORD TOGGLE
  // =============================================
  document.querySelectorAll('.toggle-pass').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.parentElement.querySelector('input');
      if (!input) return;
      if (input.type === 'password') {
        input.type = 'text';
        btn.classList.replace('fa-eye', 'fa-eye-slash');
      } else {
        input.type = 'password';
        btn.classList.replace('fa-eye-slash', 'fa-eye');
      }
    });
  });



  // =============================================
  // PROFILE DROPDOWN
  // =============================================
  const profileBtn = document.getElementById('profileBtn');
  const profileDropdown = document.getElementById('profileDropdown');
  const profileWrap = document.getElementById('profileWrap');

  if (profileBtn && profileDropdown) {
    profileBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      profileDropdown.classList.toggle('show');  // ← open → show
    });
    document.addEventListener('click', function (e) {
      if (profileWrap && !profileWrap.contains(e.target)) {
        profileDropdown.classList.remove('show');  // ← open → show
      }
    });
  }

  // =============================================
  // INIT
  // =============================================
  renderCart();
  updateWishlistCount();
  console.log('%c🌿 GreenShop Loaded!', 'color:#52b788;font-size:16px;font-weight:bold;');

}); // end DOMContentLoaded
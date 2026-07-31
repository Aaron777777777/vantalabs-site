(() => {
  const stores = {
    android: null,
    ios: null
  };

  document.querySelectorAll("[data-store]").forEach((link) => {
    const url = stores[link.dataset.store];

    if (!url) {
      link.removeAttribute("href");
      link.setAttribute("aria-disabled", "true");
      link.classList.add("disabled");
      return;
    }

    link.href = url;
    link.target = "_blank";
    link.rel = "noopener";
    link.removeAttribute("aria-disabled");
    link.classList.remove("disabled");
  });
})();

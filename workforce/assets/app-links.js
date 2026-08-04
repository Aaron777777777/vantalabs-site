(() => {
  const stores = {
    android: "https://play.google.com/store/apps/details?id=com.vantalabs.vantaworkforce",
    ios: null
  };

  document.querySelectorAll("[data-store]").forEach((element) => {
    const store = element.dataset.store;
    const url = stores[store];

    if (!url) {
      element.removeAttribute("href");
      element.setAttribute("aria-disabled", "true");
      element.classList.add("disabled");
      return;
    }

    element.href = url;
    element.target = "_blank";
    element.rel = "noopener";
    element.removeAttribute("aria-disabled");
    element.classList.remove("disabled");
  });
})();

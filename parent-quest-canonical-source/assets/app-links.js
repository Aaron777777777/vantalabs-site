(() => {
  const links = {
    android: "https://play.google.com/store/apps/details?id=com.vantalabs.parentquest",
    ios: "https://apps.apple.com/us/app/parent-quest/id6782297539",
  };

  document.querySelectorAll("[data-store]").forEach((element) => {
    const url = links[element.dataset.store];
    if (!url) return;
    element.href = url;
    element.target = "_blank";
    element.rel = "noopener noreferrer";
  });
})();

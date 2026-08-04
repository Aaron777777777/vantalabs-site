(() => {
  const links = {
    android:
      "https://play.google.com/store/apps/details?id=com.vantashift.app",
    ios:
      "https://apps.apple.com/us/app/shift-planner-rota-hours/id6771880899",
  };

  document.querySelectorAll("[data-store]").forEach((element) => {
    const url = links[element.dataset.store];

    if (!url) return;

    element.href = url;
    element.target = "_blank";
    element.rel = "noopener noreferrer";
  });
})();

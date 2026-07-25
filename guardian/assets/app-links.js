window.GUARDIAN_STORE_LINKS = {
  ios: "https://apps.apple.com/app/guardian-family-tracker/id6785882067",
  android: "https://play.google.com/store/apps/details?id=com.vantalabs.guardian&pcampaignid=web_share"
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-store]").forEach((element) => {
    const url = window.GUARDIAN_STORE_LINKS[element.dataset.store];

    if (url && !url.startsWith("__")) {
      element.href = url;
      element.classList.remove("disabled");
      element.removeAttribute("aria-disabled");
      element.textContent =
        element.dataset.store === "ios"
          ? "App Store"
          : "Google Play";
    } else {
      element.removeAttribute("href");
      element.classList.add("disabled");
      element.setAttribute("aria-disabled", "true");
    }
  });
});

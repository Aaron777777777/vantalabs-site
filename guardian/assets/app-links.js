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


/*
 * Optional GA4 measurement for Guardian pages and the Vanta Labs homepage.
 * No Google tag is loaded before an affirmative analytics choice.
 * The visitor can reject analytics and reopen preferences from the footer.
 */
(function () {
  "use strict";

  const MEASUREMENT_ID = "G-SL0K09HHQ2";
  const STORAGE_KEY = "vantalabs_analytics_choice_v1";
  const CHOICE_LIFETIME_MS = 180 * 24 * 60 * 60 * 1000;
  let analyticsEnabled = false;

  function readChoice() {
    try {
      const saved = JSON.parse(window.localStorage.getItem(STORAGE_KEY));
      if (!saved || !["allow", "reject"].includes(saved.value)) return null;
      if (!Number.isFinite(saved.at) || saved.at > Date.now()) return null;
      if (Date.now() - saved.at > CHOICE_LIFETIME_MS) return null;
      return saved.value;
    } catch (_) {
      return null;
    }
  }

  function saveChoice(value) {
    try {
      window.localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ value: value, at: Date.now() })
      );
    } catch (_) {
      // Some browsers block local storage. The visitor's current choice
      // still applies until they leave the page.
    }
  }

  function loadAnalytics() {
    if (analyticsEnabled) return;
    analyticsEnabled = true;

    window["ga-disable-" + MEASUREMENT_ID] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () {
      window.dataLayer.push(arguments);
    };
    window.gtag("js", new Date());
    window.gtag("config", MEASUREMENT_ID);

    const tag = document.createElement("script");
    tag.async = true;
    tag.src =
      "https://www.googletagmanager.com/gtag/js?id=" +
      encodeURIComponent(MEASUREMENT_ID);
    document.head.appendChild(tag);
  }

  function clearAnalyticsCookies() {
    const domain = window.location.hostname.replace(/^www\./, "");
    const cookieNames = document.cookie
      .split(";")
      .map((value) => value.trim().split("=")[0])
      .filter((name) => name === "_ga" || name.startsWith("_ga_"));

    for (const name of cookieNames) {
      document.cookie = name + "=; Max-Age=0; Path=/; SameSite=Lax";
      document.cookie =
        name + "=; Max-Age=0; Path=/; Domain=" + domain + "; SameSite=Lax";
      document.cookie =
        name + "=; Max-Age=0; Path=/; Domain=." + domain + "; SameSite=Lax";
    }
  }

  function applyChoice(value) {
    saveChoice(value);
    const banner = document.getElementById("vantalabs-analytics-banner");
    if (banner) banner.remove();

    if (value === "allow") {
      loadAnalytics();
    } else if (analyticsEnabled) {
      // Stop any loaded tracker immediately; reload without the Google tag.
      window["ga-disable-" + MEASUREMENT_ID] = true;
      if (typeof window.gtag === "function") {
        window.gtag("consent", "update", { analytics_storage: "denied" });
      }
      clearAnalyticsCookies();
      window.location.reload();
    }
  }

  function showPreferences() {
    if (document.getElementById("vantalabs-analytics-banner")) return;

    if (!document.getElementById("vantalabs-analytics-css")) {
      const css = document.createElement("style");
      css.id = "vantalabs-analytics-css";
      css.textContent = [
        "#vantalabs-analytics-banner{position:fixed;bottom:16px;left:16px;",
        "z-index:2147483000;max-width:560px;width:calc(100% - 32px);",
        "box-sizing:border-box;background:#101827;color:#fff;",
        "border:1px solid #475569;border-radius:12px;padding:18px;",
        "box-shadow:0 8px 36px rgba(0,0,0,.35);",
        "font:15px/1.5 system-ui,-apple-system,sans-serif}",
        "#vantalabs-analytics-banner strong{font-size:16px}",
        "#vantalabs-analytics-banner p{margin:8px 0 14px;color:#e2e8f0}",
        "#vantalabs-analytics-banner a{color:#fff;text-decoration:underline}",
        "#vantalabs-analytics-banner .analytics-actions{display:flex;",
        "gap:10px;flex-wrap:wrap}",
        "#vantalabs-analytics-banner button{border:1px solid #e2e8f0;",
        "background:#e2e8f0;color:#111827;padding:9px 14px;",
        "border-radius:7px;cursor:pointer;font:inherit;font-weight:600}",
        "#vantalabs-analytics-banner button:first-child{",
        "background:transparent;color:#fff}"
      ].join("");
      document.head.appendChild(css);
    }

    const banner = document.createElement("section");
    banner.id = "vantalabs-analytics-banner";
    banner.setAttribute("role", "region");
    banner.setAttribute("aria-label", "Optional analytics choices");
    banner.innerHTML =
      "<strong>Optional website analytics</strong>" +
      "<p>May we use Google Analytics cookies to understand visits and " +
      "clicks to app stores? You can reject analytics and still use " +
      'the website. <a href="/privacy.html">Privacy policy</a>.</p>' +
      '<div class="analytics-actions">' +
      '<button type="button" data-analytics-choice="reject">Reject analytics</button>' +
      '<button type="button" data-analytics-choice="allow">Accept analytics</button>' +
      "</div>";
    banner.querySelectorAll("[data-analytics-choice]").forEach((button) => {
      button.addEventListener("click", () => {
        applyChoice(button.getAttribute("data-analytics-choice"));
      });
    });
    document.body.appendChild(banner);
  }

  function addSettingsLink() {
    const footer = document.querySelector("footer");
    if (!footer) return;
    const target =
      footer.querySelector("div > span:last-child") ||
      footer.querySelector(":scope > span:last-child") ||
      footer;
    const link = document.createElement("a");
    link.href = "#analytics-preferences";
    link.textContent = "Cookie settings";
    link.style.textDecoration = "underline";
    link.style.cursor = "pointer";
    link.addEventListener("click", (event) => {
      event.preventDefault();
      showPreferences();
    });
    target.appendChild(document.createTextNode(" · "));
    target.appendChild(link);
  }

  function initAnalytics() {
    addSettingsLink();
    const choice = readChoice();
    if (choice === "allow") {
      loadAnalytics();
    } else if (choice === null) {
      showPreferences();
    }

    // Enhanced Measurement also counts outbound clicks. This custom event
    // makes Guardian Android and iOS store-button clicks easy to distinguish.
    document.addEventListener("click", (event) => {
      const anchor = event.target.closest("a[data-store]");
      if (!anchor || !analyticsEnabled || typeof window.gtag !== "function") {
        return;
      }
      const platform = anchor.dataset.store;
      if (platform !== "android" && platform !== "ios") return;
      window.gtag("event", "guardian_store_click", {
        store_platform: platform,
        link_url: anchor.href,
        page_path: window.location.pathname,
        transport_type: "beacon"
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAnalytics);
  } else {
    initAnalytics();
  }
})();

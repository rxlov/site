(() => {
  "use strict";

  /* ------------------------------------------------------------------
     Bramka wieku 18+ (samodeklaracja; sklep produkcyjny wymaga
     własnej, prawnie zatwierdzonej weryfikacji). Pamięta wybór
     na czas sesji karty, więc działa na wszystkich podstronach.
  ------------------------------------------------------------------ */
  const gate = document.querySelector("[data-gate]");
  const yesBtn = document.querySelector("[data-age-yes]");
  const noBtn = document.querySelector("[data-age-no]");
  const denied = document.querySelector("[data-gate-denied]");
  const AGE_KEY = "wejpy-age-ok";

  function setGate(open) {
    document.body.classList.toggle("is-gated", open);
    document.documentElement.classList.toggle("is-gated", open);
    gate.hidden = !open;
    document.querySelectorAll(".topbar, main, .footer").forEach((el) => { el.inert = open; });
    if (open) yesBtn.focus();
    document.dispatchEvent(new CustomEvent("wejpy:gate", { detail: { open } }));
  }

  if (gate && yesBtn && noBtn) {
    let ageOk = false;
    try { ageOk = sessionStorage.getItem(AGE_KEY) === "1"; } catch (e) { /* storage niedostępny */ }
    yesBtn.addEventListener("click", () => {
      try { sessionStorage.setItem(AGE_KEY, "1"); } catch (e) { /* ignoruj */ }
      setGate(false);
    });
    noBtn.addEventListener("click", () => {
      denied.hidden = false;
      yesBtn.hidden = true;
      noBtn.hidden = true;
    });
    setGate(!ageOk);
  }

  /* ------------------------------------------------------------------
     Formularz kontaktowy (demo: żadne dane nie opuszczają strony)
  ------------------------------------------------------------------ */
  const form = document.querySelector("[data-form]");
  const status = document.querySelector("[data-status]");
  if (form && status) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      let ok = true;
      for (const field of form.querySelectorAll("input, textarea")) {
        const valid = field.checkValidity() && field.value.trim() !== "";
        field.classList.toggle("is-invalid", !valid);
        if (!valid) ok = false;
      }
      status.textContent = ok
        ? "Dziękujemy. To wersja demonstracyjna, więc dane nie zostały wysłane."
        : "Uzupełnij imię, poprawny e-mail i wiadomość.";
      if (ok) form.reset();
    });
  }
})();

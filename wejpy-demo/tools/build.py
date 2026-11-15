#!/usr/bin/env python3
"""Generuje stronę wejpy.pl z jednego źródła:

  index.html            strona główna (hero scroll-scrub, kategorie, kontakt)
  kategorie/*.html      podstrony kategorii
  preview.html          jeden plik z całością (router na hashach), do podglądu

Edytuj dane w CATS poniżej i uruchom:  python3 tools/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISCORD_URL = "https://discord.gg/wejpy"

# kolejność = kolejność kafelków i nawigacja poprzednia/następna
CATS = [
    dict(
        slug="jednorazowki", name="Jednorazówki", art="m1",
        card="Urządzenia gotowe do użycia od razu, bez napełniania i wymiany części.",
        lead="Urządzenia gotowe do użycia od razu po wyjęciu z opakowania, bez napełniania i wymiany części. Przy każdym produkcie zawartość nikotyny podana wprost.",
        subs=[
            ("Mała pojemność", "Kompaktowe modele na krótsze użycie."),
            ("Duża pojemność", "Większe modele o dłuższej żywotności."),
            ("Bez nikotyny", "Wersje bez dodatku nikotyny. Zasady sprzedaży mogą się różnić."),
        ],
        note=("Wymaga weryfikacji prawnej",
              "Według doniesień z kwietnia 2026 rządowy projekt zakazu jednorazowych e-papierosów (z nikotyną i bez) "
              "był w Sejmie, a obecny status trzeba sprawdzić. Przed publikacją potwierdź, czy ta kategoria może "
              "w ogóle pozostać w ofercie. Usuń tę notatkę przed publikacją."),
    ),
    dict(
        slug="liquidy", name="Liquidy", art="m3",
        card="Różne smaki i pojemności, z jasną informacją o nikotynie.",
        lead="Liquidy do e-papierosów w różnych pojemnościach i smakach. Przy każdym produkcie zawartość nikotyny podana wprost, także dla wersji bez nikotyny.",
        subs=[
            ("Do systemów pod", "Liquidy dopasowane do mniejszych urządzeń."),
            ("Do większych urządzeń", "Pojemniejsze butelki do urządzeń z napełnianym zbiornikiem."),
            ("Sole nikotynowe", "Osobna grupa liquidów, oznaczona wyraźnie."),
            ("Bez nikotyny", "Liquidy bez dodatku nikotyny."),
        ],
        note=None,
    ),
    dict(
        slug="snusy", name="Snusy", art="m4",
        card="Woreczki nikotynowe w różnych mocach, dla osób pełnoletnich.",
        lead="Woreczki nikotynowe w różnych mocach i smakach. Dla osób pełnoletnich. Skład i zawartość nikotyny podane przy każdym produkcie.",
        subs=[
            ("Niższa zawartość nikotyny", "Woreczki o mniejszej mocy."),
            ("Średnia zawartość nikotyny", "Woreczki o umiarkowanej mocy."),
            ("Wyższa zawartość nikotyny", "Woreczki o większej mocy."),
        ],
        note=("Wymaga weryfikacji prawnej",
              "Nazwa „snus” bywa używana potocznie, a prawo rozróżnia woreczki nikotynowe i tytoniowe wyroby do użytku "
              "doustnego. Rządowy projekt z marca 2026 przewiduje pozostawienie w sprzedaży tylko woreczków o smaku "
              "tytoniowym, a jego obecny status trzeba sprawdzić. Opisuj produkty zgodnie z klasyfikacją prawną. "
              "Usuń tę notatkę przed publikacją."),
    ),
    dict(
        slug="grzalki-i-wklady", name="Grzałki i wkłady", art="m5",
        card="Części eksploatacyjne dopasowane do konkretnych urządzeń.",
        lead="Części eksploatacyjne dopasowane do konkretnych urządzeń. Przed zakupem sprawdź zgodność z modelem.",
        subs=[
            ("Wkłady do systemów pod", "Wymienne wkłady dopasowane do modelu urządzenia."),
            ("Grzałki do zbiorników", "Grzałki w różnych oporach i rozmiarach."),
            ("Zbiorniki i szkła zapasowe", "Części zapasowe do zbiorników."),
        ],
        note=None,
    ),
    dict(
        slug="dodatki", name="Dodatki", art="m2",
        card="Ładowarki, kable, baterie i drobne akcesoria.",
        lead="Ładowarki, kable, baterie i drobne akcesoria do urządzeń. Zawsze zgodnie z instrukcją producenta urządzenia.",
        subs=[
            ("Ładowarki i kable", "Zasilanie i ładowanie urządzeń."),
            ("Baterie", "Wymienne ogniwa dla urządzeń, które ich używają."),
            ("Czyszczenie i przechowywanie", "Drobne akcesoria na co dzień."),
        ],
        note=None,
    ),
]
BY_SLUG = {c["slug"]: c for c in CATS}

NOTICE = "Produkty z nikotyną tylko dla osób pełnoletnich. Nikotyna jest substancją silnie uzależniającą."


# ---------------------------------------------------------------- linki
def link_cat(mode, slug):
    return {"home": f"kategorie/{slug}.html", "sub": f"{slug}.html", "bundle": f"#/{slug}"}[mode]


def link_top(mode):
    return {"home": "#film", "sub": "../index.html", "bundle": "#/"}[mode]


def link_anchor(mode, anchor):
    return {"home": f"#{anchor}", "sub": f"../index.html#{anchor}", "bundle": f"#/@{anchor}"}[mode]


# ---------------------------------------------------------------- klocki
def gate_html():
    return """<!-- ============ BRAMKA WIEKU 18+ ============ -->
<div class="gate" data-gate role="dialog" aria-modal="true" aria-labelledby="gate-title" aria-describedby="gate-desc">
  <div class="gate__box">
    <div class="gate__badge" aria-hidden="true">18+</div>
    <h2 id="gate-title">Tylko dla dorosłych</h2>
    <p id="gate-desc">Ta strona dotyczy e-papierosów, liquidów i produktów z nikotyną. Wejście jest dozwolone wyłącznie dla osób, które ukończyły 18 lat.</p>
    <div class="gate__actions" data-gate-actions>
      <button type="button" class="gate__yes" data-age-yes>Mam 18 lat lub więcej</button>
      <button type="button" class="gate__no" data-age-no>Nie mam 18 lat</button>
    </div>
    <p class="gate__denied" data-gate-denied role="alert" hidden>Dziękujemy. Ta strona jest dostępna tylko dla osób pełnoletnich.</p>
    <p class="gate__note">Nikotyna jest substancją silnie uzależniającą.</p>
  </div>
</div>"""


def header_html(mode):
    return f"""<header class="topbar">
  <a class="brand" href="{link_top(mode)}" aria-label="wejpy.pl — strona główna">wejpy<span>.pl</span></a>
  <nav aria-label="Nawigacja">
    <a href="{link_anchor(mode, 'film')}">Film</a>
    <a href="{link_anchor(mode, 'kategorie')}">Kategorie</a>
    <a href="{link_anchor(mode, 'kontakt')}" class="nav-cta">Kontakt</a>
  </nav>
</header>"""


def footer_html():
    return """<footer class="footer">
  <p class="footer__brand">wejpy<span>.pl</span></p>
  <p class="footer__legal">Produkty zawierające nikotynę są przeznaczone wyłącznie dla osób pełnoletnich. Nikotyna jest substancją silnie uzależniającą. To koncepcja demonstracyjna: teksty, kategorie i wizualia wymagają akceptacji wejpy.pl oraz weryfikacji zgodności z przepisami o reklamie i sprzedaży e-papierosów przed jakąkolwiek publikacją.</p>
</footer>"""


def cards_html(mode):
    out = []
    for i, c in enumerate(CATS, 1):
        out.append(f"""      <a class="card {c['art']}" href="{link_cat(mode, c['slug'])}">
        <div class="card__art" aria-hidden="true"></div>
        <p class="card__tag">Kategoria {i:02d}</p>
        <h3>{c['name']}</h3>
        <p>{c['card']}</p>
        <span class="card__more">Zobacz kategorię <i aria-hidden="true">→</i></span>
      </a>""")
    out.append(f"""      <a class="card m6 card--ext" href="{DISCORD_URL}" target="_blank" rel="noopener noreferrer">
        <div class="card__art" aria-hidden="true"></div>
        <p class="card__tag">Zewnętrzny link · Discord</p>
        <h3>Dołącz do Discorda</h3>
        <p>Społeczność wejpy. Link otwiera Discord w nowej karcie.</p>
        <span class="card__more">discord.gg/wejpy <i aria-hidden="true">↗</i><span class="sr-only"> (otwiera się w nowej karcie)</span></span>
      </a>""")
    return "\n".join(out)


def home_main(mode, attrs=""):
    return f"""<main{attrs}>

  <!-- ============ SCROLL-SCRUB HERO ============ -->
  <section id="film" class="track" data-track aria-label="Film przewijany scrollem">
    <div class="stage" data-stage>

      <video class="stage__media stage__video" data-video muted playsinline preload="auto" tabindex="-1" aria-hidden="true"></video>
      <canvas class="stage__media stage__canvas" data-canvas aria-hidden="true"></canvas>
      <div class="stage__shade" aria-hidden="true"></div>
      <div class="stage__grain" aria-hidden="true"></div>

      <h1 class="stage__title"><span>wejpy.pl</span><em>Koncept · 18+</em></h1>

      <p class="badge" data-badge role="note">
        <i></i><span data-badge-text>Podgląd zastępczy · brak klipu media/hero.mp4</span>
      </p>

      <div class="chapters">
        <article class="chapter is-active" data-chapter="0">
          <p class="chapter__kicker">Rozdział 01 / 03</p>
          <h2>Urządzenia</h2>
          <p class="chapter__text">Systemy pod, zestawy startowe i większe urządzenia. Spokojny przegląd kategorii, bez pośpiechu.</p>
          <p class="chapter__hint" aria-hidden="true"><span></span>Przewijaj</p>
        </article>
        <article class="chapter" data-chapter="1" aria-hidden="true">
          <p class="chapter__kicker">Rozdział 02 / 03</p>
          <h2>Liquidy</h2>
          <p class="chapter__text">Różne smaki i pojemności. Przy każdym produkcie jasna informacja o zawartości nikotyny.</p>
        </article>
        <article class="chapter" data-chapter="2" aria-hidden="true">
          <p class="chapter__kicker">Rozdział 03 / 03</p>
          <h2>Akcesoria</h2>
          <p class="chapter__text">Grzałki, wkłady, baterie i ładowarki. Części dopasowane do konkretnych urządzeń.</p>
        </article>
      </div>

      <p class="stage__warn">{NOTICE}</p>

      <aside class="hud" role="progressbar" aria-label="Postęp sceny" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
        <div class="hud__row">
          <span class="hud__label">Postęp sceny</span>
          <span class="hud__pct"><b data-pct>000</b>%</span>
        </div>
        <div class="hud__bar">
          <span class="seg"><i data-seg="0"></i></span>
          <span class="seg"><i data-seg="1"></i></span>
          <span class="seg"><i data-seg="2"></i></span>
        </div>
        <ol class="hud__chapters">
          <li class="is-active" data-hud="0"><span>01</span>Urządzenia</li>
          <li data-hud="1"><span>02</span>Liquidy</li>
          <li data-hud="2"><span>03</span>Akcesoria</li>
        </ol>
        <p class="hud__note">Wskaźnik pokazuje pozycję w scenie. To nie jest pomiar żadnego produktu.</p>
      </aside>

    </div>
  </section>

  <!-- ============ KATEGORIE ============ -->
  <section id="kategorie" class="section details">
    <div class="section__head">
      <p class="eyebrow">Kategorie</p>
      <h2 class="section__title">Pięć działów, <em>jedna społeczność</em></h2>
      <p class="section__lead">Wybierz dział, żeby zobaczyć jego stronę. Zdjęcia i opisy produktów czekają na uzupełnienie.</p>
    </div>

    <div class="grid">
{cards_html(mode)}
    </div>
  </section>

  <!-- ============ KONTAKT ============ -->
  <section id="kontakt" class="section contact">
    <div class="contact__panel">
      <div class="contact__copy">
        <p class="eyebrow">Kontakt</p>
        <h2 class="section__title">Masz pytanie <em>o asortyment?</em></h2>
        <p class="section__lead">Opisz krótko, w czym możemy pomóc. Pytania o zamówienia i dostępność trafią do obsługi sklepu.</p>
        <p class="contact__demo">To strona demonstracyjna. Formularz nie wysyła jeszcze danych.</p>
      </div>

      <form class="form" data-form novalidate>
        <label>
          <span>Imię</span>
          <input type="text" name="name" autocomplete="name" required>
        </label>
        <label>
          <span>E-mail</span>
          <input type="email" name="email" autocomplete="email" required>
        </label>
        <label>
          <span>Wiadomość</span>
          <textarea name="message" rows="4" required></textarea>
        </label>
        <button type="submit">Wyślij wiadomość</button>
        <p class="form__status" data-status role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>

</main>"""


def sub_main(mode, slug, attrs=""):
    i = next(n for n, c in enumerate(CATS) if c["slug"] == slug)
    c = CATS[i]
    prev_c = CATS[i - 1] if i > 0 else None
    next_c = CATS[i + 1] if i < len(CATS) - 1 else None

    chips = "\n".join(
        f"""        <div class="chip"><h3>{t}</h3><p>{d}</p></div>""" for t, d in c["subs"]
    )
    slots = "\n".join(
        f"""        <article class="slot">
          <div class="slot__img" aria-hidden="true"><span>Zdjęcie produktu</span></div>
          <div class="slot__body">
            <p class="slot__tag">Slot produktu {n:02d}</p>
            <h3>Nazwa produktu</h3>
            <dl>
              <div><dt>Nikotyna</dt><dd>do uzupełnienia</dd></div>
              <div><dt>Cena</dt><dd>do uzupełnienia</dd></div>
            </dl>
            <button type="button" disabled>Szczegóły wkrótce</button>
          </div>
        </article>"""
        for n in range(1, 7)
    )
    note = ""
    if c["note"]:
        note = f"""
    <aside class="note" role="note">
      <strong>{c['note'][0]}</strong>
      {c['note'][1]}
    </aside>"""

    prev_html = (
        f"""<a class="pager__prev" href="{link_cat(mode, prev_c['slug'])}"><span>← Poprzednia</span>{prev_c['name']}</a>"""
        if prev_c else "<span></span>"
    )
    next_html = (
        f"""<a class="pager__next" href="{link_cat(mode, next_c['slug'])}"><span>Następna →</span>{next_c['name']}</a>"""
        if next_c else "<span></span>"
    )

    return f"""<main class="page"{attrs}>
  <nav class="crumbs" aria-label="Ścieżka">
    <a href="{link_top(mode)}">Strona główna</a><span aria-hidden="true">/</span>
    <a href="{link_anchor(mode, 'kategorie')}">Kategorie</a><span aria-hidden="true">/</span>
    <span aria-current="page">{c['name']}</span>
  </nav>

  <header class="page__hero {c['art']}">
    <div class="card__art" aria-hidden="true"></div>
    <p class="eyebrow">Kategoria {i + 1:02d} / {len(CATS):02d}</p>
    <h1>{c['name']}</h1>
    <p class="lead">{c['lead']}</p>
  </header>

  <section class="page__section" aria-labelledby="sub-h">
    <h2 id="sub-h">W tej kategorii</h2>
    <div class="chips">
{chips}
    </div>
    <p class="page__hint">Przykładowy podział do akceptacji przez wejpy.pl.</p>
  </section>

  <section class="page__section" aria-labelledby="prod-h">
    <h2 id="prod-h">Produkty</h2>
    <div class="slots">
{slots}
    </div>
    <p class="warnline">{NOTICE}</p>{note}
  </section>

  <nav class="pager" aria-label="Inne kategorie">
    {prev_html}
    <a class="pager__all" href="{link_anchor(mode, 'kategorie')}">Wszystkie kategorie</a>
    {next_html}
  </nav>
</main>"""


# ---------------------------------------------------------------- strony
HEAD = """<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#07070F">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%2307070F'/%3E%3Ccircle cx='16' cy='16' r='6' fill='none' stroke='%234DF0C0' stroke-width='3'/%3E%3C/svg%3E">"""


def real_page(title, desc, body_class, mode, main, prefix, home):
    scripts = f'<script src="{prefix}common.js"></script>' + (f'\n<script src="{prefix}app.js"></script>' if home else "")
    return f"""<!doctype html>
<html lang="pl">
<head>
  {HEAD}
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="stylesheet" href="{prefix}style.css">
</head>
<body class="{body_class}" data-source="placeholder">

{gate_html()}

{header_html(mode)}

{main}

{footer_html()}

{scripts}
</body>
</html>
"""


ROUTER = """
(() => {
  "use strict";
  const pages = [...document.querySelectorAll("[data-page]")];
  const titles = {};
  pages.forEach((p) => { titles[p.dataset.page] = p.dataset.title; });

  function go(hash) {
    const h = decodeURIComponent((hash || "").replace(/^#\\/?/, ""));
    let slug = "home", anchor = null;
    if (h.startsWith("@")) anchor = h.slice(1);
    else if (h) slug = h;
    if (!(slug in titles)) slug = "home";
    pages.forEach((p) => { p.hidden = p.dataset.page !== slug; });
    document.body.classList.toggle("subpage", slug !== "home");
    document.title = titles[slug];
    window.scrollTo({ top: 0, behavior: "instant" });
    window.dispatchEvent(new Event("resize"));
    requestAnimationFrame(() => {
      if (anchor) {
        const el = document.getElementById(anchor);
        if (el) el.scrollIntoView({ behavior: "instant", block: "start" });
      }
      window.dispatchEvent(new Event("scroll"));
    });
  }

  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#/"]');
    if (!a) return;
    e.preventDefault();
    const href = a.getAttribute("href");
    try { history.replaceState(null, "", href); } catch (err) { /* sandbox */ }
    go(href);
  });
  window.addEventListener("hashchange", () => go(location.hash));
  go(location.hash || "#/");
})();
"""


def build():
    css = (ROOT / "style.css").read_text(encoding="utf-8")
    common = (ROOT / "common.js").read_text(encoding="utf-8")
    app = (ROOT / "app.js").read_text(encoding="utf-8")

    # strona główna
    (ROOT / "index.html").write_text(
        real_page("wejpy.pl — koncept scroll film", "Koncept demonstracyjny strony scroll-scrub dla wejpy.pl. Treści tylko dla osób pełnoletnich.",
                  "is-gated", "home", home_main("home"), "", True),
        encoding="utf-8")

    # podstrony
    (ROOT / "kategorie").mkdir(exist_ok=True)
    for c in CATS:
        (ROOT / "kategorie" / f"{c['slug']}.html").write_text(
            real_page(f"{c['name']} — wejpy.pl", f"{c['name']}: koncept strony kategorii wejpy.pl. Treści tylko dla osób pełnoletnich.",
                      "is-gated subpage", "sub", sub_main("sub", c["slug"]), "../", False),
            encoding="utf-8")

    # preview: wszystko w jednym pliku, nawigacja na hashach
    mains = [home_main("bundle", ' data-page="home" data-title="wejpy.pl — koncept scroll film"')]
    for c in CATS:
        mains.append(sub_main("bundle", c["slug"], f' data-page="{c["slug"]}" data-title="{c["name"]} — wejpy.pl" hidden'))
    preview = f"""<!doctype html>
<html lang="pl">
<head>
  {HEAD}
  <title>wejpy.pl — koncept scroll film</title>
  <style>
{css}
  </style>
</head>
<body class="is-gated" data-source="placeholder">

{gate_html()}

{header_html("bundle")}

{chr(10).join(mains)}

{footer_html()}

<script>
{common}
</script>
<script>
{app}
</script>
<script>
{ROUTER}
</script>
</body>
</html>
"""
    (ROOT / "preview.html").write_text(preview, encoding="utf-8")
    print("OK:", "index.html,", ", ".join(f"kategorie/{c['slug']}.html" for c in CATS) + ", preview.html")


if __name__ == "__main__":
    build()

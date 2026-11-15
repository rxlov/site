# wejpy.pl — koncept scroll film

Statyczna strona bez zależności. Źródło: `style.css`, `app.js` (hero), `common.js` (bramka 18+, formularz)
i `tools/build.py` (generuje HTML). Po zmianie treści kategorii edytuj `CATS` w `tools/build.py` i uruchom:

```bash
python3 tools/build.py   # tworzy index.html, kategorie/*.html i preview.html
```

## Struktura

- `index.html` — strona główna (hero, kafelki kategorii, kontakt)
- `kategorie/jednorazowki.html`, `liquidy.html`, `snusy.html`, `grzalki-i-wklady.html`, `dodatki.html` — podstrony
- Kafelek „Dołącz do Discorda” prowadzi do https://discord.gg/wejpy (nowa karta, `rel="noopener noreferrer"`)
- Każda podstrona ma okruszki, 6 slotów produktów (zdjęcie, nikotyna, cena do uzupełnienia) i nawigację poprzednia/następna
- `preview.html` — cała strona w jednym pliku (nawigacja na hashach), do szybkiego podglądu bez serwera


## Uruchomienie lokalnie

```bash
cd wejpy-demo
python3 -m http.server 8080
# http://localhost:8080
```

Serwer musi obsługiwać zapytania zakresowe (Range). `python3 -m http.server` je obsługuje.

## Jak działa

- Sekcja `#film` ma 520 svh (420 svh na telefonie), scena jest przypięta (`position: sticky`).
- Postęp scrolla (0–1) steruje klatką: `video.currentTime = postęp × długość`.
- Rozdziały: URZĄDZENIA (0–⅓), LIQUIDY (⅓–⅔), AKCESORIA (⅔–1).
- HUD pokazuje postęp w scenie i aktywny rozdział, nie dane produktowe.
- Przy wejściu pojawia się bramka 18+ (samodeklaracja, zapamiętana na czas sesji karty).

## Stan wizualiów

Klipu `media/hero.mp4` jeszcze nie ma (szczegóły i prompty w `PROMPTS.md`). Dopóki go brak,
hero pokazuje podgląd zastępczy na canvasie z widoczną plakietką. Po wgraniu klipu strona
sama przełącza się na wideo.

```bash
tools/prepare-clip.sh ~/Downloads/klip.mp4   # tworzy media/hero.mp4
```

## Zgodność z przepisami: do sprawdzenia przed publikacją

W Polsce reklama i promocja e-papierosów jest ograniczona, sprzedaż osobom poniżej 18 lat jest
zakazana, a od lipca 2025 zmiany objęły też wyroby bez nikotyny (m.in. sprzedaż na odległość
i reklama). Kinowe hero może być uznane za promocję. Strona to koncepcja i **nie powinna być
publikowana bez opinii prawnika**. Bramka 18+ oparta na samodeklaracji nie jest weryfikacją
wieku wymaganą w sklepie. Strona ma `noindex`.

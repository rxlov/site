# Prompty do wizualiów (wejpy.pl)

Stan: generowanie nie przeszło na koncie Higgsfield (plan free, 10 kr). GPT Image 2.5/2.6
zwróciły „Requires basic plan or higher", a najtańszy klip Seedance 2.5 to 12 kr. Szacunki
z preflightu: still 16:9 2k high ≈ 2,75 kr, klip 12 s 720p bez dźwięku ≈ 84 kr, draft 480p ≈ 36 kr.
Tryb `video_extension` jest dostępny w `seedance_2_5`.

Zasady dla wszystkich kadrów: bez ludzi, bez twarzy, bez rąk, bez logo i napisów, bez
pokazywania samego palenia. Urządzenie ma być generyczne (bez marki). Żadnych ujęć
lifestyle'owych ani sugerujących młody wiek odbiorcy.

## 1. Hero still (GPT Image 2.x, 16:9)

```
Cinematic macro product photograph of a generic, unbranded matte-black compact pod vape device standing upright on a dark reflective surface, low camera angle, soft violet and mint rim light, a faint wisp of vapor drifting behind it in the background, deep ink-black studio backdrop with subtle violet haze, shallow depth of field, photorealistic, wide 16:9 framing with the device on the left third and open negative space on the right. No people, no hands, no faces, no text, no logos, no brand marks, no packaging, no watermark.
```

Zatwierdź kształt, kolor i kierunek kadru, zanim pójdzie dalej.

## 2. Klip 12 s (Seedance 2.5, image-to-video)

`mode: omni_reference`, `start_image` = hero still, `duration: 12`, `aspect_ratio: 16:9`,
`generate_audio: false`, najpierw `draft: true` (480p).

```
One continuous slow macro dolly shot, no cuts, perfectly stable gimbal movement, no shake. The camera glides slowly along the unbranded matte-black device on the dark reflective surface, violet light sliding along its edge, a soft wisp of vapor slowly drifting and dissolving in the background. Same device, same colour, same silhouette throughout. No people, no text, no logos.
```

## 3. Przedłużenia (tylko gdy ciągłość trzyma)

`mode: video_extension`, `extension_mode: forward`, `video_references` = ostatni dobry klip.

Liquidy:
```
Continue the same single dolly shot without a cut. The light shifts from violet to mint green, the camera drifts past a row of generic unlabeled glass bottles with softly glowing liquid in different colours, same dark reflective surface. No labels, no text, no logos, no people.
```

Akcesoria:
```
Continue the same single dolly shot without a cut. The light shifts to cool ice blue, the camera drifts over small unbranded accessories lined up on the same dark surface: replacement coils, a battery and a charging cable. No text, no logos, no people.
```

Reguła ciągłości: po każdym przedłużeniu porównaj kolor i kształt urządzenia z hero stillem.
Jeśli coś odpłynie, zapisz co i w której sekundzie, po czym wróć do ostatniego dobrego klipu
zamiast generować urządzenie od zera.

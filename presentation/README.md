# Presentación — Alleanza Academy

Deck ejecutivo (ES) para la reunión de alineación estratégica previa al lanzamiento.

## Archivos

- `Alleanza_Academy_Presentacion.pptx` — presentación, 10 slides, 16:9.
- `assets/` — versiones del logo:
  - `alleanza_logo.png` — color, para fondos claros.
  - `alleanza_logo_white.png` — wordmark blanco, para fondos oscuros.
  - `alleanza_mark.png` — solo el escudo.
- `scripts/` — generadores reproducibles:
  - `make_logo_variants.py` — deriva `_white` y `_mark` desde el logo oficial.
  - `build_deck.py` — construye el `.pptx` (usa rutas relativas a `assets/`).

## Branding

- Color principal `#7C46A6` · acento `#9958D7` · navy `#061330` · fondo claro `#EAECF3`.
- Tipografía: **Inter** (instalar antes de presentar para fidelidad exacta).

## Logo

> Se usa el **logo oficial** (`LOGO ACADEMY USE THIS.png` subido al repo). La variante de
> wordmark blanco se genera automáticamente para los fondos oscuros (portada y slide de
> instructores). Para regenerar todo:
>
> ```
> python3 scripts/make_logo_variants.py
> python3 scripts/build_deck.py
> ```

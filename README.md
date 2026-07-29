# 💎 Alonda

Galería de 10 retratos hiperrealistas de **Alonda** — un avatar femenino rubio, ojos verdes, facciones finas, generado con el modelo `image-01` de MiniMax.

## Stack

- `index.html` — landing + grid responsive
- `style.css` — tema oscuro premium con acentos dorados
- `script.js` — lightbox + carga lazy
- `assets/images/` — 10 retratos generados con IA

## Ver en vivo

GitHub Pages (se activa después del primer push):
`https://aguitech.github.io/alonda/`

## Generar nuevas imágenes localmente

```bash
cd scripts/
uv venv .venv && source .venv/bin/activate
uv pip install requests pillow
python gen_alonda.py  # genera 10 imágenes en assets/images/
```

## Licencia

Solo para uso personal del autor. Las imágenes son generadas por IA y pueden contener artefactos inherentes al modelo.
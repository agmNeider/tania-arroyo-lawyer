# Prototipo estático del sitio

> La versión oficial del sitio es la **app de Next.js** en la raíz del repositorio (`app/`, `components/`, `lib/`). Esta carpeta conserva el prototipo en un solo archivo HTML.

Página única construida con el sistema de diseño de `design-system/`. Vista previa publicada: https://claude.ai/artifact/Jk3s3XRUhyNANvpyRRNBiX

## Archivos

- `plantilla.html`: el contenido y los estilos. **Aquí se edita.**
- `construir.py`: inserta los tokens, el logotipo, el monograma y los íconos oficiales, y genera:
  - `index.html`: el sitio listo para subir a cualquier hosting (Netlify, Vercel, GitHub Pages, cPanel).
  - `artefacto.html`: la misma página sin `<html>` ni `<head>`, para la vista previa en claude.ai.

```bash
python3 sitio/construir.py
```

## Secciones

Portada con seguimiento de un caso · Áreas de práctica · Cómo trabajo · Procesos y casos típicos (por área, con plazo y norma) · Casos resueltos · Guía útil (plazos, qué traer, preguntas frecuentes) · Agendar cita (presencial o virtual, día, hora y datos) · Contacto.

## Antes de publicar

1. **Datos reales:** teléfono y WhatsApp (+57 313 699 4178), correo (arroyo752tania@gmail.com), Instagram (@taniaarroyo_abogada) y ciudad (Chinú, Córdoba).
2. **Casos resueltos:** los cuatro casos son los definitivos del sitio.
3. **Agenda:** hoy la solicitud se arma en la página y se envía por WhatsApp; los horarios ocupados son de ejemplo. Para bloquear horas reales, conecte la agenda a un servicio de citas (Google Calendar, Calendly o Cal.com) o a un formulario con respaldo (Formspree, Netlify Forms).
4. **Normas citadas:** verifique que sigan vigentes antes de publicar.
5. **Política de datos:** enlace la política de tratamiento de datos personales (Ley 1581 de 2012) en la casilla de autorización.

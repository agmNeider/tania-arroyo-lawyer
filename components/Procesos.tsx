'use client';
import { useRef, useState } from 'react';
import { PROCESOS } from '@/lib/contenido';
import { Icono } from './Marca';

export function Procesos() {
  const [activo, setActivo] = useState(0);
  const tabs = useRef<(HTMLButtonElement | null)[]>([]);
  const mover = (e: React.KeyboardEvent, i: number) => {
    const paso = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
    if (!paso) return;
    e.preventDefault();
    const n = (i + paso + PROCESOS.length) % PROCESOS.length;
    setActivo(n);
    tabs.current[n]?.focus();
  };
  return (
    <section className="sec sup" id="procesos" aria-labelledby="t-procesos">
      <div className="envoltura">
        <div className="sec-cab">
          <div>
            <p className="etq pino">Procesos y casos típicos</p>
            <h2 id="t-procesos">¿Se parece a lo que le está pasando?</h2>
          </div>
          <p>Estas son las situaciones que más atiendo. Para cada una le cuento qué proceso aplica y cuál es el plazo que no debe dejar pasar.</p>
        </div>
        <div className="pestanas" role="tablist" aria-label="Áreas">
          {PROCESOS.map((g, i) => (
            <button
              key={g.id}
              ref={(el) => { tabs.current[i] = el; }}
              className="pestana"
              role="tab"
              type="button"
              id={`tab-${g.id}`}
              aria-controls={`pan-${g.id}`}
              aria-selected={i === activo}
              tabIndex={i === activo ? 0 : -1}
              onClick={() => setActivo(i)}
              onKeyDown={(e) => mover(e, i)}
            >
              <Icono nombre={g.icono} />
              {g.nombre}
            </button>
          ))}
        </div>
        {PROCESOS.map((g, i) => (
          <div key={g.id} className="panel" role="tabpanel" id={`pan-${g.id}`} aria-labelledby={`tab-${g.id}`} hidden={i !== activo}>
            {g.casos.map((c) => (
              <article key={c.pregunta} className="caso">
                <p className="q">{c.pregunta}</p>
                <dl>
                  <div><dt>{c.etiqueta1}</dt><dd>{c.texto1}</dd></div>
                  <div><dt>Qué hacer ahora</dt><dd>{c.ahora}</dd></div>
                </dl>
                <div className="plazo">
                  <b>{c.plazo}</b>
                  <span className="norma">{c.norma}</span>
                </div>
              </article>
            ))}
          </div>
        ))}
        <p className="nota-datos">
          Esta información es general. Cada caso tiene detalles que cambian los plazos y el camino: agende una consulta para revisar el suyo.
        </p>
      </div>
    </section>
  );
}

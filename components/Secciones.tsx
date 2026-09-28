import { AREAS, CASOS, CASOS_DE_EJEMPLO, PASOS, PLAZOS, PREGUNTAS, QUE_TRAER } from '@/lib/contenido';
import { Icono } from './Marca';

function Cabecera({ etiqueta, titulo, id, children }: { etiqueta: string; titulo: string; id: string; children: React.ReactNode }) {
  return (
    <div className="sec-cab">
      <div>
        <p className="etq pino">{etiqueta}</p>
        <h2 id={id}>{titulo}</h2>
      </div>
      <p>{children}</p>
    </div>
  );
}

export function Areas() {
  return (
    <section className="sec sup" id="areas" aria-labelledby="t-areas">
      <div className="envoltura">
        <Cabecera etiqueta="Áreas de práctica" titulo="Una especialidad, cinco áreas que la acompañan" id="t-areas">
          El derecho procesal civil es mi especialidad: saber cómo avanza un proceso, qué plazos corren y qué se puede pedir en cada
          etapa. Ese conocimiento lo aplico a cada área en la que trabajo.
        </Cabecera>
        <div className="areas">
          {AREAS.map((a) => (
            <article key={a.nombre} className={`area${a.especialidad ? ' esp' : ''}`}>
              <Icono nombre={a.icono} />
              {a.especialidad && <p className="etq">Especialidad</p>}
              <h3>{a.nombre}</h3>
              <p>{a.texto}</p>
              <ul>
                {a.temas.map((t) => (
                  <li key={t}>{t}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Metodo() {
  return (
    <section className="sec" aria-labelledby="t-metodo">
      <div className="envoltura">
        <Cabecera etiqueta="Cómo trabajo" titulo="Usted sabe siempre en qué va su caso" id="t-metodo">
          Nada de lenguaje enredado ni de semanas sin noticias. Cada etapa tiene una fecha y usted la conoce desde el principio.
        </Cabecera>
        <ol className="pasos">
          {PASOS.map((p) => (
            <li key={p.titulo} className="paso">
              <h3>{p.titulo}</h3>
              <p>{p.texto}</p>
              <span className="cuando">{p.cuando}</span>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}

export function Casos() {
  return (
    <section className="sec oscura" id="casos" aria-labelledby="t-casos">
      <div className="envoltura">
        <div className="sec-cab">
          <div>
            <p className="etq">Casos resueltos</p>
            <h2 id="t-casos">Lo que pasó, lo que hicimos y lo que puede aprender</h2>
          </div>
          <p>Cada caso se publica sin nombres ni datos que permitan identificar a las personas, y solo con la autorización del cliente.</p>
        </div>
        {CASOS_DE_EJEMPLO && (
          <p className="aviso">
            <b>Casos de ejemplo.</b> Reemplácelos por casos reales, anonimizados y autorizados por escrito, antes de publicar el sitio.
          </p>
        )}
        <div className="resueltos">
          {CASOS.map((c) => (
            <article key={c.titulo} className="res">
              <div className="res-cab">
                <span className="chip">
                  <Icono nombre={c.icono} />
                  {c.area}
                </span>
                <span className="dur">Duración: {c.duracion}</span>
              </div>
              <h3>{c.titulo}</h3>
              <div className="fases">
                <div><span>La situación</span><p>{c.situacion}</p></div>
                <div><span>Qué hicimos</span><p>{c.hicimos}</p></div>
                <div><span>El resultado</span><p>{c.resultado}</p></div>
              </div>
              <p className="leccion">
                <b>Para usted:</b> {c.leccion}
              </p>
            </article>
          ))}
        </div>
        <div className="invita">
          <p>¿Tiene un caso parecido? Revisémoslo antes de que corra otro plazo.</p>
          <a className="btn" href="#agendar">
            Agendar una cita <span className="flecha" aria-hidden="true">→</span>
          </a>
        </div>
      </div>
    </section>
  );
}

export function Guia() {
  return (
    <section className="sec" id="guia" aria-labelledby="t-guia">
      <div className="envoltura">
        <Cabecera etiqueta="Guía útil" titulo="Plazos que no debe dejar pasar" id="t-guia">
          En los procesos, perder un término puede significar perder la oportunidad de defenderse o de reclamar. Estos son los más
          comunes.
        </Cabecera>
        <div className="guia">
          <div className="tabla-env">
            <table>
              <caption>Términos frecuentes</caption>
              <thead>
                <tr><th scope="col">Situación</th><th scope="col">Plazo</th></tr>
              </thead>
              <tbody>
                {PLAZOS.map((p) => (
                  <tr key={p.situacion}>
                    <td>{p.situacion}<span className="norma">{p.norma}</span></td>
                    <td className="dias">{p.plazo}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <aside className="lista" aria-labelledby="t-traer">
            <h3 id="t-traer">Qué traer a la primera consulta</h3>
            <ul>
              {QUE_TRAER.map((t) => (
                <li key={t}>{t}</li>
              ))}
            </ul>
          </aside>
        </div>
        <div className="faq">
          <h3>Preguntas frecuentes</h3>
          <div>
            {PREGUNTAS.map((q) => (
              <details key={q.p}>
                <summary>{q.p}</summary>
                <p>{q.r}</p>
              </details>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

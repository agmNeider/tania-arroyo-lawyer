import { BarraTerminos } from './Marca';

const HITOS = [
  { estado: 'h', texto: 'Revisión de la demanda y de las pruebas', dia: 'Día 3' },
  { estado: 'h', texto: 'Reunión con usted: estrategia y excepciones', dia: 'Día 8' },
  { estado: 'hoy', texto: 'Borrador de la contestación para su revisión', dia: 'Hoy' },
  { estado: '', texto: 'Radicación ante el juzgado', dia: 'Día 18' },
];

export function Portada() {
  return (
    <section className="portada" aria-labelledby="t-portada">
      <div className="envoltura">
        <div>
          <p className="etq pino">Abogada · Procesalista civil</p>
          <h1 id="t-portada">
            Cada término, <em>cumplido.</em>
          </h1>
          <p className="intro">
            Soy <b>Tania Arroyo Guzmán</b>. Llevo procesos civiles, laborales, de familia, sucesiones y contratos. Le explico su
            caso en palabras claras, le digo qué sigue y le aviso antes de que venza cada plazo.
          </p>
          <div className="acciones">
            <a className="btn btn-p" href="#agendar">
              Agendar una cita <span className="flecha" aria-hidden="true">→</span>
            </a>
            <a className="btn btn-l" href="#procesos">
              Ver casos típicos
            </a>
          </div>
          <div className="datos">
            <div><b>Presencial o virtual</b><span>Usted elige en cada cita</span></div>
            <div><b>Respuesta en 1 día hábil</b><span>A cada mensaje y solicitud</span></div>
            <div><b>Por escrito</b><span>Opciones, plazos y costos</span></div>
          </div>
        </div>

        <article className="seguimiento" aria-label="Ejemplo de seguimiento de un caso">
          <div className="seg-cab">
            <div>
              <p className="etq">Su caso · Proceso verbal</p>
              <h3>Contestación de la demanda</h3>
            </div>
            <span className="estado warn">Vence en 6 días hábiles</span>
          </div>
          <p className="cifra">
            Día 14 <small>de 20</small>
          </p>
          <BarraTerminos total={20} cumplidos={13} />
          <div className="seg-pie">
            <span className="norma">Notificación</span>
            <span className="norma">CGP, art. 369</span>
          </div>
          <ul className="hitos">
            {HITOS.map((h) => (
              <li key={h.texto}>
                <span className={`pto ${h.estado}`} />
                <span>{h.texto}</span>
                <time>{h.dia}</time>
              </li>
            ))}
          </ul>
          <p className="ejemplo">Así le muestro el avance de su proceso. Caso de ejemplo.</p>
        </article>
      </div>
    </section>
  );
}

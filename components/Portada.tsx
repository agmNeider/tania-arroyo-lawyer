import { CONTACTO, SERVICIOS } from '@/lib/contenido';
import { Icono } from './Marca';

export function Portada() {
  return (
    <section className="portada" aria-labelledby="t-portada">
      <div className="envoltura">
        <div>
          <p className="etq pino">Abogada · Procesalista civil</p>
          <h1 id="t-portada">
            Asesoría legal <em>clara y cercana.</em>
          </h1>
          <p className="intro">
            Soy <b>Tania Arroyo Guzmán</b>. Asesoro y represento a personas, familias y pequeñas empresas en asuntos civiles,
            laborales, de familia, sucesiones y contratos. Le explico su caso en palabras sencillas y lo acompaño de principio a fin.
          </p>
          <div className="acciones">
            <a className="btn btn-p" href="#agendar">
              Agendar una cita <span className="flecha" aria-hidden="true">→</span>
            </a>
            <a className="btn btn-l" href="#areas">
              Ver áreas de práctica
            </a>
          </div>
          <div className="datos">
            <div><b>Presencial o virtual</b><span>Usted elige en cada cita</span></div>
            <div><b>Respuesta en 1 día hábil</b><span>A cada mensaje y solicitud</span></div>
            <div><b>Honorarios por escrito</b><span>Antes de empezar</span></div>
          </div>
        </div>

        <article className="servicios" aria-labelledby="t-servicios">
          <p className="etq">Servicios</p>
          <h2 id="t-servicios">Cómo puedo ayudarle</h2>
          <ul>
            {SERVICIOS.map((s) => (
              <li key={s.nombre}>
                <Icono nombre={s.icono} />
                <div>
                  <h3>{s.nombre}</h3>
                  <p>{s.texto}</p>
                </div>
              </li>
            ))}
          </ul>
          <p className="srv-pie">
            Oficina en {CONTACTO.ciudad}, {CONTACTO.departamento}. Consultas virtuales por videollamada.
          </p>
        </article>
      </div>
    </section>
  );
}

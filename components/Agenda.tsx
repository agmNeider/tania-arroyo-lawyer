'use client';
import { useEffect, useRef, useState } from 'react';
import { CONTACTO, DIAS_A_MOSTRAR, HORAS_CITA, TEMAS_CITA } from '@/lib/contenido';
import {
  desdeIso, diaCorto, fechaLarga, iso, mesCorto, proximosDiasHabiles, textoSolicitud, validarCita,
  type ErroresCita, type Modalidad, type SolicitudCita,
} from '@/lib/citas';
import { Icono } from './Marca';

type Estado = 'editando' | 'enviando' | 'listo';

export function Agenda() {
  const [dias, setDias] = useState<Date[]>([]);
  const [modalidad, setModalidad] = useState<Modalidad>('Presencial');
  const [fecha, setFecha] = useState<string>('');
  const [hora, setHora] = useState<string>('');
  const [datos, setDatos] = useState({ nombre: '', celular: '', correo: '', tema: '', mensaje: '', empresa: '' });
  const [autoriza, setAutoriza] = useState(false);
  const [errores, setErrores] = useState<ErroresCita>({});
  const [estado, setEstado] = useState<Estado>('editando');
  const [avisoEnvio, setAvisoEnvio] = useState('');
  const [copiado, setCopiado] = useState('');
  const [enviada, setEnviada] = useState<SolicitudCita | null>(null);
  const listoRef = useRef<HTMLDivElement>(null);

  // Las fechas dependen del día de quien visita: se calculan en el navegador.
  useEffect(() => {
    const d = proximosDiasHabiles(DIAS_A_MOSTRAR);
    setDias(d);
    setFecha(iso(d[0]));
  }, []);
  useEffect(() => { if (estado === 'listo') listoRef.current?.focus(); }, [estado]);

  const campo = (k: keyof typeof datos) => ({
    value: datos[k],
    onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
      setDatos({ ...datos, [k]: e.target.value });
      setErrores((x) => ({ ...x, [k]: undefined }));
    },
  });
  const fechaSel = dias.find((d) => iso(d) === fecha);

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    const s: SolicitudCita = {
      modalidad, fecha, hora, tema: datos.tema, nombre: datos.nombre.trim(), celular: datos.celular.trim(),
      correo: datos.correo.trim(), mensaje: datos.mensaje.trim() || undefined, autoriza,
    };
    const err = validarCita(s);
    setErrores(err);
    if (Object.keys(err).length) {
      const primero = document.querySelector<HTMLElement>('.campo.mal input, .campo.mal select');
      primero?.focus();
      return;
    }
    setEstado('enviando');
    setAvisoEnvio('');
    try {
      const r = await fetch('/api/citas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...s, empresa: datos.empresa }),
      });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) {
        if (j.errores) setErrores(j.errores);
        setAvisoEnvio(j.mensaje || 'No pudimos registrar la solicitud. Revise los datos o escríbanos por WhatsApp.');
        setEstado('editando');
        return;
      }
      setAvisoEnvio('');
    } catch {
      setAvisoEnvio('No hay conexión con el servidor. Puede enviar la solicitud por WhatsApp.');
    }
    setEnviada(s);
    setEstado('listo');
  }

  const copiar = async () => {
    if (!enviada) return;
    try {
      await navigator.clipboard.writeText(textoSolicitud(enviada));
      setCopiado('Copiado.');
    } catch {
      setCopiado('No se pudo copiar. Seleccione el texto y cópielo.');
    }
  };

  const clase = (k: keyof ErroresCita, extra = '') => `campo${extra}${errores[k] ? ' mal' : ''}`;

  return (
    <section className="sec sup" id="agendar" aria-labelledby="t-agendar">
      <div className="envoltura agenda">
        <div className="agenda-info">
          <p className="etq pino">Agendar cita</p>
          <h2 id="t-agendar">Hablemos de su caso</h2>
          <p>Elija si prefiere vernos en la oficina o por videollamada, y escoja el día y la hora que le queden mejor.</p>
          <ul className="incluye">
            <li><Icono nombre="consulta" /><span><b>45 minutos solo para su caso</b>Me cuenta qué pasó y revisamos sus documentos.</span></li>
            <li><Icono nombre="terminos" /><span><b>Plazos claros desde el primer día</b>Sale sabiendo qué términos corren y hasta cuándo.</span></li>
            <li><Icono nombre="contratos" /><span><b>Diagnóstico por escrito</b>Opciones, riesgos y costos, en los 3 días hábiles siguientes.</span></li>
          </ul>
        </div>

        <form className="form" onSubmit={enviar} noValidate>
          <div hidden={estado === 'listo'}>
            <fieldset>
              <legend><span className="n">1.</span> Modalidad</legend>
              <div className="modos">
                {(['Presencial', 'Virtual'] as const).map((m) => (
                  <div className="opcion" key={m}>
                    <input type="radio" name="modo" id={`modo-${m}`} value={m} checked={modalidad === m} onChange={() => setModalidad(m)} />
                    <label htmlFor={`modo-${m}`}>
                      <Icono nombre={m === 'Presencial' ? 'oficina' : 'videollamada'} />
                      <span>
                        <b>{m}</b>
                        <span>{m === 'Presencial' ? 'En la oficina, con sus documentos en físico' : 'Por videollamada; le envío el enlace'}</span>
                      </span>
                    </label>
                  </div>
                ))}
              </div>
            </fieldset>

            <fieldset style={{ marginTop: 26 }}>
              <legend><span className="n">2.</span> Día</legend>
              <div className="dias" role="group" aria-label="Días hábiles disponibles">
                {dias.length === 0 && <p className="norma">Cargando días hábiles…</p>}
                {dias.map((d) => (
                  <button key={iso(d)} type="button" className="dia" aria-pressed={iso(d) === fecha} aria-label={fechaLarga(d)}
                    onClick={() => { setFecha(iso(d)); setErrores((x) => ({ ...x, fecha: undefined })); }}>
                    <span className="ds">{diaCorto(d)}</span>
                    <span className="dn">{d.getDate()}</span>
                    <span className="dm">{mesCorto(d)}</span>
                  </button>
                ))}
              </div>
              <p className="norma">Solo días hábiles: sin fines de semana ni festivos.</p>
            </fieldset>

            <fieldset style={{ marginTop: 26 }}>
              <legend>
                <span className="n">3.</span> Hora{' '}
                {fechaSel && <span style={{ textTransform: 'none', letterSpacing: 0, fontWeight: 400 }}>· {fechaLarga(fechaSel)}</span>}
              </legend>
              <div className="horas" role="group" aria-label="Horas disponibles">
                {HORAS_CITA.map((h) => (
                  <button key={h} type="button" className="hora" aria-pressed={h === hora}
                    onClick={() => { setHora(h); setErrores((x) => ({ ...x, hora: undefined })); }}>
                    {h}
                  </button>
                ))}
              </div>
              {errores.hora && <p className="norma" style={{ color: 'var(--plazo)' }}>{errores.hora}</p>}
            </fieldset>

            <fieldset style={{ marginTop: 26 }}>
              <legend><span className="n">4.</span> Sus datos</legend>
              <div className="campos">
                <div className={clase('nombre')}>
                  <label htmlFor="c-nombre">Nombre completo</label>
                  <input type="text" id="c-nombre" autoComplete="name" {...campo('nombre')} />
                  <span className="err">{errores.nombre}</span>
                </div>
                <div className={clase('celular')}>
                  <label htmlFor="c-tel">Celular</label>
                  <input type="tel" id="c-tel" autoComplete="tel" inputMode="tel" {...campo('celular')} />
                  <span className="err">{errores.celular}</span>
                </div>
                <div className={clase('correo')}>
                  <label htmlFor="c-correo">Correo</label>
                  <input type="email" id="c-correo" autoComplete="email" {...campo('correo')} />
                  <span className="err">{errores.correo}</span>
                </div>
                <div className={clase('tema')}>
                  <label htmlFor="c-area">Tema</label>
                  <select id="c-area" {...campo('tema')}>
                    <option value="">Elija un tema</option>
                    {TEMAS_CITA.map((t) => <option key={t}>{t}</option>)}
                  </select>
                  <span className="err">{errores.tema}</span>
                </div>
                <div className={clase('mensaje', ' ancho')}>
                  <label htmlFor="c-msg">Cuénteme brevemente su caso <small>(opcional)</small></label>
                  <textarea id="c-msg" placeholder="Por ejemplo: me notificaron una demanda el 15 de septiembre por un contrato de arrendamiento." {...campo('mensaje')} />
                  <span className="err">{errores.mensaje}</span>
                </div>
                {/* Campo trampa contra bots: las personas no lo ven. */}
                <div className="sr" aria-hidden="true">
                  <label htmlFor="c-empresa">Empresa</label>
                  <input type="text" id="c-empresa" tabIndex={-1} autoComplete="off" {...campo('empresa')} />
                </div>
              </div>
            </fieldset>

            <label className={`acepto${errores.autoriza ? ' mal' : ''}`} style={{ marginTop: 20 }}>
              <input type="checkbox" id="c-acepto" checked={autoriza} onChange={(e) => { setAutoriza(e.target.checked); setErrores((x) => ({ ...x, autoriza: undefined })); }} />
              <span>Autorizo el tratamiento de mis datos personales para gestionar esta cita, según la Ley 1581 de 2012. La información de su caso es confidencial.</span>
            </label>

            <div className="resumen" style={{ marginTop: 22 }}>
              <p aria-live="polite">
                {!fechaSel ? 'Elija un día y una hora.' : (
                  <>Cita <b>{modalidad.toLowerCase()}</b> el <b>{fechaLarga(fechaSel)}</b>{hora ? <> a las <b>{hora}</b>.</> : '. Falta la hora.'}</>
                )}
              </p>
              <button className="btn btn-p" type="submit" disabled={estado === 'enviando'}>
                {estado === 'enviando' ? 'Enviando…' : <>Solicitar cita <span className="flecha" aria-hidden="true">→</span></>}
              </button>
            </div>
            {avisoEnvio && <p className="nota-datos" role="alert" style={{ color: 'var(--plazo)' }}>{avisoEnvio}</p>}
          </div>

          {estado === 'listo' && enviada && (
            <div className="listo" ref={listoRef} tabIndex={-1}>
              <div className="marca"><i aria-hidden="true" /><p className="etq pino">Solicitud recibida</p></div>
              <h3>Su solicitud de cita quedó registrada</h3>
              <dl>
                <dt>Modalidad</dt><dd>{enviada.modalidad}</dd>
                <dt>Fecha</dt><dd>{fechaLarga(desdeIso(enviada.fecha))}</dd>
                <dt>Hora</dt><dd>{enviada.hora}</dd>
                <dt>Tema</dt><dd>{enviada.tema}</dd>
                <dt>Nombre</dt><dd>{enviada.nombre}</dd>
                <dt>Celular</dt><dd>{enviada.celular}</dd>
                <dt>Correo</dt><dd>{enviada.correo}</dd>
              </dl>
              <p className="sig">
                Le confirmo la cita en máximo un día hábil{enviada.modalidad === 'Virtual' ? ', con el enlace de la videollamada' : ''}. Si es urgente o tiene un plazo corriendo, escríbame también por WhatsApp.
              </p>
              {avisoEnvio && <p className="nota-datos" style={{ color: 'var(--plazo)' }}>{avisoEnvio}</p>}
              <div className="fila">
                <a className="btn btn-p" href={`https://wa.me/${CONTACTO.whatsapp}?text=${encodeURIComponent(textoSolicitud(enviada))}`} target="_blank" rel="noopener noreferrer">
                  Enviar por WhatsApp
                </a>
                <button className="btn btn-s" type="button" onClick={copiar}>Copiar solicitud</button>
                <button className="btn btn-l" type="button" onClick={() => { setEstado('editando'); setCopiado(''); }}>Pedir otra cita</button>
              </div>
              <p className="nota-datos" aria-live="polite">{copiado}</p>
            </div>
          )}
        </form>
      </div>
    </section>
  );
}

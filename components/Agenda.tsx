'use client';
import Cal, { getCalApi } from '@calcom/embed-react';
import { useEffect, useState } from 'react';
import { CONTACTO, TIPOS_CITA } from '@/lib/contenido';
import { Icono } from './Marca';

type TipoCita = (typeof TIPOS_CITA)[number];

// Colores de la marca dentro del calendario de Cal.com (pino en claro, pino aclarado en oscuro).
const COLORES_CAL = {
  light: { 'cal-brand': '#17433D', 'cal-brand-emphasis': '#0F2E2A', 'cal-brand-text': '#FFFFFF' },
  dark: { 'cal-brand': '#7CC2B1', 'cal-brand-emphasis': '#8FD3BE', 'cal-brand-text': '#0D1917' },
};

function Calendario({ tipo }: { tipo: TipoCita }) {
  const ns = `cita-${tipo.id}`;
  useEffect(() => {
    let vivo = true;
    getCalApi({ namespace: ns }).then((cal) => {
      if (vivo) cal('ui', { cssVarsPerTheme: COLORES_CAL, hideEventTypeDetails: false, layout: 'month_view' });
    });
    return () => { vivo = false; };
  }, [ns]);
  return (
    <Cal
      key={ns}
      namespace={ns}
      calLink={tipo.calLink}
      config={{ layout: 'month_view', theme: 'auto' }}
      style={{ width: '100%' }}
    />
  );
}

export function Agenda() {
  const [tipo, setTipo] = useState<TipoCita>(TIPOS_CITA[0]);
  const whatsapp = `https://wa.me/${CONTACTO.whatsapp}?text=${encodeURIComponent('Hola, quiero agendar una cita con Arroyo Guzmán.')}`;

  return (
    <section className="sec sup" id="agendar" aria-labelledby="t-agendar">
      <div className="envoltura agenda">
        <div className="agenda-info">
          <p className="etq pino">Agendar cita</p>
          <h2 id="t-agendar">Hablemos de su caso</h2>
          <p>Elija si prefiere vernos en la oficina o por videollamada, y escoja el día y la hora que le queden mejor. Solo aparecen las horas disponibles.</p>
          <ul className="incluye">
            <li><Icono nombre="consulta" /><span><b>Una hora solo para su caso</b>Me cuenta qué pasó y revisamos sus documentos.</span></li>
            <li><Icono nombre="terminos" /><span><b>Confirmación inmediata</b>Recibe un correo con la cita y un recordatorio antes de ella.</span></li>
            <li><Icono nombre="contratos" /><span><b>Diagnóstico por escrito</b>Opciones, riesgos y costos, en los 3 días hábiles siguientes.</span></li>
          </ul>
        </div>

        <div className="form">
          <fieldset>
            <legend><span className="n">1.</span> Modalidad</legend>
            <div className="modos">
              {TIPOS_CITA.map((t) => (
                <div className="opcion" key={t.id}>
                  <input type="radio" name="modo" id={`modo-${t.id}`} value={t.id} checked={tipo.id === t.id} onChange={() => setTipo(t)} />
                  <label htmlFor={`modo-${t.id}`}>
                    <Icono nombre={t.icono} />
                    <span><b>{t.nombre}</b><span>{t.detalle}</span></span>
                  </label>
                </div>
              ))}
            </div>
          </fieldset>

          <fieldset>
            <legend><span className="n">2.</span> Día, hora y sus datos</legend>
            <div className="cal-caja">
              <Calendario key={tipo.id} tipo={tipo} />
            </div>
          </fieldset>

          <p className="cal-alterno">
            ¿No ve el calendario?{' '}
            <a href={`https://cal.com/${tipo.calLink}`} target="_blank" rel="noopener noreferrer">Abra la agenda en Cal.com</a>
            {' '}o{' '}
            <a href={whatsapp} target="_blank" rel="noopener noreferrer">escríbame por WhatsApp</a>.
          </p>
        </div>
      </div>
    </section>
  );
}

'use client';
import { useState } from 'react';
import { CONTACTO } from '@/lib/contenido';

function Copiar({ texto, etiqueta }: { texto: string; etiqueta: string }) {
  const [msg, setMsg] = useState(etiqueta);
  const copiar = async () => {
    try {
      await navigator.clipboard.writeText(texto);
      setMsg('Copiado');
    } catch {
      setMsg('Seleccione y copie');
    }
    setTimeout(() => setMsg(etiqueta), 1600);
  };
  return <button className="copiar" type="button" onClick={copiar}>{msg}</button>;
}

export function Contacto() {
  return (
    <section className="sec" id="contacto" aria-labelledby="t-contacto">
      <div className="envoltura">
        <div className="sec-cab">
          <div>
            <p className="etq pino">Contacto</p>
            <h2 id="t-contacto">Escríbame, le respondo en un día hábil</h2>
          </div>
          <p>Si tiene un plazo corriendo, dígalo en el primer mensaje: esos casos los atiendo primero.</p>
        </div>
        <div className="contacto">
          <div className="canal">
            <p className="etq">WhatsApp y llamadas</p>
            <a className="val" href={`https://wa.me/${CONTACTO.whatsapp}`} target="_blank" rel="noopener noreferrer">{CONTACTO.telefono}</a>
            <p className="sub">{CONTACTO.horario}</p>
            <Copiar texto={CONTACTO.telefono} etiqueta="Copiar número" />
          </div>
          <div className="canal">
            <p className="etq">Correo</p>
            <a className="val" href={`mailto:${CONTACTO.correo}`}>{CONTACTO.correo}</a>
            <p className="sub">Para enviar documentos</p>
            <Copiar texto={CONTACTO.correo} etiqueta="Copiar correo" />
          </div>
          <div className="canal">
            <p className="etq">Oficina</p>
            <p className="val">{CONTACTO.ciudad}, {CONTACTO.departamento}</p>
            <p className="sub">Solo con cita previa</p>
          </div>
          <div className="canal">
            <p className="etq">Instagram</p>
            <a className="val" href={`https://instagram.com/${CONTACTO.instagram.replace('@', '')}`} target="_blank" rel="noopener noreferrer">{CONTACTO.instagram}</a>
            <p className="sub">Datos útiles sobre sus derechos, cada semana</p>
          </div>
        </div>
      </div>
    </section>
  );
}

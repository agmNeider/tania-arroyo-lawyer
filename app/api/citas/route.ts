import { NextResponse } from 'next/server';
import { validarCita, type SolicitudCita } from '@/lib/citas';

// Recibe una solicitud de cita, la valida con las mismas reglas del formulario y la
// reenvía a CITAS_WEBHOOK_URL (Zapier, Make, n8n, Google Apps Script…) si está configurada.
export async function POST(req: Request) {
  let cuerpo: Partial<SolicitudCita> & { empresa?: string };
  try {
    cuerpo = await req.json();
  } catch {
    return NextResponse.json({ ok: false, mensaje: 'La solicitud no tiene un formato válido.' }, { status: 400 });
  }

  // Campo trampa: si viene lleno, es un bot. Respondemos como si todo estuviera bien.
  if (cuerpo.empresa) return NextResponse.json({ ok: true });

  const errores = validarCita(cuerpo);
  if (Object.keys(errores).length) {
    return NextResponse.json({ ok: false, mensaje: 'Revise los datos marcados.', errores }, { status: 422 });
  }

  const cita = {
    modalidad: cuerpo.modalidad,
    fecha: cuerpo.fecha,
    hora: cuerpo.hora,
    tema: cuerpo.tema,
    nombre: cuerpo.nombre!.trim(),
    celular: cuerpo.celular!.trim(),
    correo: cuerpo.correo!.trim(),
    mensaje: cuerpo.mensaje?.trim() || '',
    autorizaTratamientoDatos: true,
    recibida: new Date().toISOString(),
  };

  const webhook = process.env.CITAS_WEBHOOK_URL;
  if (!webhook) {
    console.info('[citas] Solicitud recibida (configure CITAS_WEBHOOK_URL para guardarla):', { fecha: cita.fecha, hora: cita.hora, tema: cita.tema });
    return NextResponse.json({ ok: true, guardada: false });
  }
  try {
    const r = await fetch(webhook, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(cita) });
    if (!r.ok) throw new Error(`webhook ${r.status}`);
    return NextResponse.json({ ok: true, guardada: true });
  } catch (e) {
    console.error('[citas] No se pudo reenviar la solicitud:', e);
    return NextResponse.json({ ok: false, mensaje: 'No pudimos registrar su solicitud en este momento. Envíela por WhatsApp y le respondo.' }, { status: 502 });
  }
}

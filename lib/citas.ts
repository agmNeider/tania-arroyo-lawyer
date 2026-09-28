// Lógica de citas compartida por el formulario (cliente) y la API (servidor).
import { HORAS_CITA, TEMAS_CITA } from './contenido';

export type Modalidad = 'Presencial' | 'Virtual';
export type SolicitudCita = {
  modalidad: Modalidad;
  fecha: string; // AAAA-MM-DD
  hora: string;
  tema: string;
  nombre: string;
  celular: string;
  correo: string;
  mensaje?: string;
  autoriza: boolean;
};
export type ErroresCita = Partial<Record<keyof SolicitudCita, string>>;

// ---------------------------------------------------------------- Festivos de Colombia
// Ley 51 de 1983 (traslado al lunes) y fechas que dependen de la Pascua.
function pascua(anio: number): Date {
  const a = anio % 19, b = Math.floor(anio / 100), c = anio % 100, d = Math.floor(b / 4), e = b % 4;
  const f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30;
  const i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451);
  const mes = Math.floor((h + l - 7 * m + 114) / 31), dia = ((h + l - 7 * m + 114) % 31) + 1;
  return new Date(anio, mes - 1, dia);
}
const mas = (f: Date, n: number) => new Date(f.getFullYear(), f.getMonth(), f.getDate() + n);
const alLunes = (f: Date) => (f.getDay() === 1 ? f : mas(f, (8 - f.getDay()) % 7 || 7));

const cacheFestivos = new Map<number, Set<string>>();
export function festivos(anio: number): Set<string> {
  const guardado = cacheFestivos.get(anio);
  if (guardado) return guardado;
  const p = pascua(anio);
  const fijos = [[0, 1], [4, 1], [6, 20], [7, 7], [11, 8], [11, 25]].map(([m, d]) => new Date(anio, m, d));
  const trasladables = [[0, 6], [2, 19], [5, 29], [7, 15], [9, 12], [10, 1], [10, 11]].map(([m, d]) => alLunes(new Date(anio, m, d)));
  const pascuales = [mas(p, -3), mas(p, -2), alLunes(mas(p, 39)), alLunes(mas(p, 60)), alLunes(mas(p, 68))];
  const set = new Set([...fijos, ...trasladables, ...pascuales].map(iso));
  cacheFestivos.set(anio, set);
  return set;
}

export function iso(f: Date): string {
  return `${f.getFullYear()}-${String(f.getMonth() + 1).padStart(2, '0')}-${String(f.getDate()).padStart(2, '0')}`;
}
export function desdeIso(s: string): Date {
  const [a, m, d] = s.split('-').map(Number);
  return new Date(a, m - 1, d);
}
export function esDiaHabil(f: Date): boolean {
  return f.getDay() !== 0 && f.getDay() !== 6 && !festivos(f.getFullYear()).has(iso(f));
}
/** Los próximos `n` días hábiles, empezando mañana. */
export function proximosDiasHabiles(n: number, desde = new Date()): Date[] {
  const dias: Date[] = [];
  let f = mas(new Date(desde.getFullYear(), desde.getMonth(), desde.getDate()), 1);
  while (dias.length < n) {
    if (esDiaHabil(f)) dias.push(f);
    f = mas(f, 1);
  }
  return dias;
}

// ---------------------------------------------------------------- Formato
const DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
const MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
export const fechaLarga = (f: Date) => `${DIAS[f.getDay()]} ${f.getDate()} de ${MESES[f.getMonth()]}`;
export const diaCorto = (f: Date) => DIAS[f.getDay()].slice(0, 3);
export const mesCorto = (f: Date) => MESES[f.getMonth()].slice(0, 3);

// ---------------------------------------------------------------- Validación
export function validarCita(s: Partial<SolicitudCita>, hoy = new Date()): ErroresCita {
  const e: ErroresCita = {};
  if (s.modalidad !== 'Presencial' && s.modalidad !== 'Virtual') e.modalidad = 'Elija presencial o virtual.';
  if (!s.fecha || !/^\d{4}-\d{2}-\d{2}$/.test(s.fecha)) e.fecha = 'Elija un día.';
  else {
    const f = desdeIso(s.fecha);
    const manana = mas(new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate()), 1);
    if (f < manana || !esDiaHabil(f)) e.fecha = 'Elija un día hábil a partir de mañana.';
  }
  if (!s.hora || !HORAS_CITA.includes(s.hora)) e.hora = 'Elija una hora para su cita.';
  if (!s.tema || !TEMAS_CITA.includes(s.tema)) e.tema = 'Elija el tema de su consulta.';
  if (!s.nombre || s.nombre.trim().length < 3) e.nombre = 'Escriba su nombre.';
  if (!s.celular || s.celular.replace(/\D/g, '').length < 10) e.celular = 'Escriba un celular de 10 dígitos.';
  if (!s.correo || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s.correo.trim())) e.correo = 'Escriba un correo válido.';
  if (s.mensaje && s.mensaje.length > 2000) e.mensaje = 'Resuma su caso en máximo 2.000 caracteres.';
  if (!s.autoriza) e.autoriza = 'Necesitamos su autorización para gestionar la cita.';
  return e;
}

export function textoSolicitud(s: SolicitudCita): string {
  const filas = [
    ['Modalidad', s.modalidad],
    ['Fecha', fechaLarga(desdeIso(s.fecha))],
    ['Hora', s.hora],
    ['Tema', s.tema],
    ['Nombre', s.nombre],
    ['Celular', s.celular],
    ['Correo', s.correo],
  ];
  if (s.mensaje) filas.push(['Caso', s.mensaje]);
  return 'Hola, quiero agendar una cita con Arroyo Guzmán.\n' + filas.map(([k, v]) => `${k}: ${v}`).join('\n');
}

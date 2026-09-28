'use client';
import { useState } from 'react';
import { Logotipo } from './Marca';

const ENLACES = [
  ['#areas', 'Áreas'],
  ['#procesos', 'Procesos típicos'],
  ['#casos', 'Casos'],
  ['#guia', 'Guía útil'],
  ['#contacto', 'Contacto'],
] as const;

export function Encabezado() {
  const [abierto, setAbierto] = useState(false);
  const cerrar = () => setAbierto(false);
  return (
    <header className="cab">
      <div className="envoltura">
        <a className="logo" href="#inicio" aria-label="Arroyo Guzmán, inicio">
          <Logotipo />
        </a>
        <button className="abrir" type="button" aria-expanded={abierto} aria-controls="menu" onClick={() => setAbierto(!abierto)}>
          {abierto ? 'Cerrar' : 'Menú'}
        </button>
        <nav className={`menu${abierto ? ' abierto' : ''}`} id="menu" aria-label="Principal">
          {ENLACES.map(([href, texto]) => (
            <a key={href} href={href} onClick={cerrar}>
              {texto}
            </a>
          ))}
          <a className="btn btn-p" href="#agendar" onClick={cerrar}>
            Agendar cita
          </a>
        </nav>
      </div>
    </header>
  );
}

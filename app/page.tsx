import { Agenda } from '@/components/Agenda';
import { Contacto } from '@/components/Contacto';
import { Encabezado } from '@/components/Encabezado';
import { Pie } from '@/components/Pie';
import { Portada } from '@/components/Portada';
import { Procesos } from '@/components/Procesos';
import { Areas, Casos, Guia, Metodo } from '@/components/Secciones';

export default function Inicio() {
  return (
    <>
      <Encabezado />
      <main id="inicio">
        <Portada />
        <Areas />
        <Metodo />
        <Procesos />
        <Casos />
        <Guia />
        <Agenda />
        <Contacto />
      </main>
      <Pie />
    </>
  );
}

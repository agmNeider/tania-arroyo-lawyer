// Todo el texto del sitio. Edite aquí; los componentes solo lo presentan.
import type { NombreIcono } from './marca.generada';

// ---------------------------------------------------------------- Datos de contacto
// Teléfono, WhatsApp y correo son reales. Dirección, T.P. e Instagram siguen siendo DE EJEMPLO:
// reemplácelos por los reales antes de publicar y cambie datosDeEjemplo a false.
export const CONTACTO = {
  nombre: 'Tania Arroyo Guzmán',
  cargo: 'Abogada · Procesalista civil',
  tarjetaProfesional: 'T.P. 000.000 del C. S. de la J.',
  telefono: '+57 313 699 4178',
  whatsapp: process.env.NEXT_PUBLIC_WHATSAPP || '573136994178',
  correo: 'arroyogtania@gmail.com',
  direccion: 'Calle 00 # 00-00, oficina 000',
  ciudad: 'Bogotá D. C.',
  instagram: '@arroyoguzman.abogada',
  horario: 'Lunes a viernes, 8:00 a. m. a 6:00 p. m.',
  datosDeEjemplo: true,
};

// ---------------------------------------------------------------- Áreas
export type Area = { icono: NombreIcono; nombre: string; texto: string; temas: string[]; especialidad?: boolean };
export const AREAS: Area[] = [
  { icono: 'procesal', nombre: 'Procesal civil', especialidad: true, texto: 'Demandas, contestaciones, recursos y audiencias. Represento a personas y pequeñas empresas de principio a fin del proceso.', temas: ['Procesos verbales', 'Ejecutivos', 'Recursos'] },
  { icono: 'civil', nombre: 'Civil', texto: 'Conflictos por bienes, deudas, daños y propiedad. Busco primero un acuerdo y, si no es posible, acudo al juez.', temas: ['Pertenencia', 'Responsabilidad civil', 'Cobro de deudas'] },
  { icono: 'laboral', nombre: 'Laboral', texto: 'Despidos, liquidaciones y salarios que no se pagaron. Reviso sus cuentas y le digo cuánto le deben y por qué.', temas: ['Despido sin justa causa', 'Liquidación', 'Seguridad social'] },
  { icono: 'familia', nombre: 'Familia', texto: 'Divorcios, cuotas alimentarias y custodia, con el cuidado que merecen los temas de familia y los niños.', temas: ['Divorcio', 'Alimentos', 'Custodia y visitas'] },
  { icono: 'sucesiones', nombre: 'Sucesiones', texto: 'Repartir una herencia en orden, ante notaría o ante el juez, según el acuerdo que haya entre los herederos.', temas: ['Sucesión notarial', 'Sucesión judicial', 'Partición'] },
  { icono: 'contratos', nombre: 'Contratos', texto: 'Reviso y redacto contratos antes de que usted firme, y lo acompaño si la otra parte no cumple lo pactado.', temas: ['Arrendamiento', 'Compraventa', 'Prestación de servicios'] },
];

// ---------------------------------------------------------------- Cómo trabajo
export const PASOS = [
  { titulo: 'Consulta inicial', texto: 'Me cuenta qué pasó y revisamos juntos sus documentos. Le digo si tiene un caso y qué caminos existen.', cuando: '45 minutos, presencial o virtual' },
  { titulo: 'Diagnóstico por escrito', texto: 'Recibe un documento corto con las opciones, los plazos que corren, los riesgos y el costo de cada camino.', cuando: 'En los 3 días hábiles siguientes' },
  { titulo: 'Actuación', texto: 'Si decide seguir, preparo y radico lo necesario: acuerdo, demanda, contestación o recurso. Usted lo revisa antes.', cuando: 'Con fechas acordadas' },
  { titulo: 'Seguimiento', texto: 'Le envío cada novedad del proceso y le aviso con anticipación de audiencias y términos por vencer.', cuando: 'Hasta el final del proceso' },
];

// ---------------------------------------------------------------- Procesos y casos típicos
export type CasoTipico = { pregunta: string; etiqueta1: string; texto1: string; ahora: string; plazo: string; norma: string };
export type GrupoProcesos = { id: string; icono: NombreIcono; nombre: string; casos: CasoTipico[] };
export const PROCESOS: GrupoProcesos[] = [
  {
    id: 'procesal', icono: 'procesal', nombre: 'Procesal civil', casos: [
      { pregunta: 'Me notificaron una demanda', etiqueta1: 'Qué proceso aplica', texto1: 'Depende de la demanda: casi siempre un proceso verbal o verbal sumario.', ahora: 'No deje pasar los días. Reúna el documento de notificación y todo lo que tenga sobre el caso.', plazo: '20 días hábiles para contestar', norma: 'Verbal: CGP, art. 369. Verbal sumario: 10 días, art. 391.' },
      { pregunta: 'Me deben dinero y tengo un pagaré, una letra o una factura', etiqueta1: 'Qué proceso aplica', texto1: 'Proceso ejecutivo. El juez puede ordenar el pago y el embargo de bienes del deudor.', ahora: 'Guarde el título original. Revisemos que esté vigente, porque los títulos valores tienen plazos de prescripción.', plazo: 'El deudor tiene 5 días para pagar y 10 para defenderse', norma: 'CGP, arts. 431 y 442.' },
      { pregunta: 'Mi inquilino no paga ni entrega el inmueble', etiqueta1: 'Qué proceso aplica', texto1: 'Restitución de inmueble arrendado, para recuperar el inmueble; el cobro de los cánones puede ir en el mismo proceso.', ahora: 'Tenga a mano el contrato y la relación de los meses que le deben.', plazo: 'Sin pagar, el arrendatario no puede ser oído en el proceso', norma: 'CGP, art. 384.' },
    ],
  },
  {
    id: 'laboral', icono: 'laboral', nombre: 'Laboral', casos: [
      { pregunta: 'Me despidieron sin justa causa', etiqueta1: 'Qué le corresponde', texto1: 'Una indemnización que depende del tipo de contrato y del tiempo trabajado, además de la liquidación.', ahora: 'Guarde la carta de terminación, el contrato y sus desprendibles de pago.', plazo: '3 años para reclamar', norma: 'Indemnización: CST, art. 64. Prescripción: CST, art. 488.' },
      { pregunta: 'Terminé mi contrato y no me pagaron la liquidación', etiqueta1: 'Qué le corresponde', texto1: 'Salarios, prestaciones y vacaciones pendientes. Si el empleador no paga a tiempo, puede deberle una sanción por cada día de retraso.', ahora: 'Anote la fecha exacta de terminación y la de su último pago.', plazo: 'La sanción corre desde el día de la terminación', norma: 'CST, art. 65.' },
      { pregunta: 'No me afiliaron a seguridad social', etiqueta1: 'Qué le corresponde', texto1: 'El pago de los aportes que faltan y, según el caso, la protección que habría tenido.', ahora: 'Descargue su historia laboral de pensiones y su certificado de afiliación a salud.', plazo: 'Revíselo cuanto antes', norma: 'Algunos derechos prescriben; otros, como los aportes a pensión, no.' },
    ],
  },
  {
    id: 'familia', icono: 'familia', nombre: 'Familia', casos: [
      { pregunta: 'Queremos divorciarnos y estamos de acuerdo', etiqueta1: 'Qué proceso aplica', texto1: 'Divorcio de mutuo acuerdo ante notario, sin juicio, con un acuerdo sobre bienes, hijos y alimentos.', ahora: 'Consigan el registro civil de matrimonio y hagan una lista de los bienes y deudas.', plazo: 'Es el camino más corto', norma: 'Ley 962 de 2005, art. 34.' },
      { pregunta: 'El papá o la mamá de mis hijos no aporta', etiqueta1: 'Qué proceso aplica', texto1: 'Fijación de cuota alimentaria: primero conciliación y, si no hay acuerdo, un proceso ante el juez de familia.', ahora: 'Reúna los registros civiles de los niños y los recibos de sus gastos mensuales.', plazo: 'La conciliación va primero', norma: 'Requisito previo para acudir al juez.' },
      { pregunta: 'No nos ponemos de acuerdo con la custodia', etiqueta1: 'Qué proceso aplica', texto1: 'Custodia y régimen de visitas. El juez decide pensando primero en el interés de los niños.', ahora: 'Anote cómo ha sido el cuidado diario hasta hoy: quién lleva al colegio, a citas médicas, fines de semana.', plazo: 'Se puede acordar antes de ir al juez', norma: 'Código de la Infancia y la Adolescencia.' },
    ],
  },
  {
    id: 'sucesiones', icono: 'sucesiones', nombre: 'Sucesiones', casos: [
      { pregunta: 'Falleció un familiar y todos los herederos estamos de acuerdo', etiqueta1: 'Qué proceso aplica', texto1: 'Sucesión ante notaría. Todos los herederos firman, con apoderado, y se reparte según lo acordado y la ley.', ahora: 'Consigan el registro de defunción, los registros de parentesco y los certificados de los bienes.', plazo: 'Suele tomar pocos meses', norma: 'Decreto 902 de 1988.' },
      { pregunta: 'Los herederos no nos ponemos de acuerdo', etiqueta1: 'Qué proceso aplica', texto1: 'Sucesión judicial ante el juez, que resuelve las diferencias y aprueba la partición.', ahora: 'Evite vender o disponer de los bienes mientras no haya partición aprobada.', plazo: 'Toma más tiempo que la notarial', norma: 'CGP, arts. 487 y siguientes.' },
      { pregunta: 'Alguien vive en un inmueble de la herencia y no quiere salir', etiqueta1: 'Qué proceso aplica', texto1: 'Depende de su calidad: heredero, arrendatario o poseedor. Cada caso tiene un camino distinto.', ahora: 'Consiga el certificado de libertad y tradición del inmueble.', plazo: 'Revíselo pronto', norma: 'Una posesión larga puede afectar los derechos de los herederos.' },
    ],
  },
  {
    id: 'contratos', icono: 'contratos', nombre: 'Contratos y civil', casos: [
      { pregunta: 'Voy a firmar un contrato de arrendamiento', etiqueta1: 'Qué revisar', texto1: 'Duración, reajuste del canon, depósitos, cláusula penal y quién paga los servicios y las reparaciones.', ahora: 'Envíeme el borrador antes de firmar. Una revisión a tiempo cuesta menos que un proceso.', plazo: 'Vivienda urbana tiene reglas propias', norma: 'Ley 820 de 2003.' },
      { pregunta: 'La otra parte no cumplió el contrato', etiqueta1: 'Qué proceso aplica', texto1: 'Puede pedir que cumpla o que el contrato se resuelva, y en ambos casos la indemnización de perjuicios.', ahora: 'Guarde el contrato, los pagos y los mensajes o correos con la otra parte.', plazo: 'Primero se intenta conciliar', norma: 'Código Civil, art. 1546.' },
      { pregunta: 'Vivo hace años en un inmueble que no está a mi nombre', etiqueta1: 'Qué proceso aplica', texto1: 'Proceso de pertenencia, para que el juez lo declare dueño por prescripción adquisitiva.', ahora: 'Reúna pruebas del tiempo que lleva: recibos de impuesto predial, servicios, mejoras y testigos.', plazo: 'Exige un tiempo mínimo de posesión', norma: 'CGP, art. 375.' },
    ],
  },
];

// ---------------------------------------------------------------- Casos resueltos
// CASOS DE EJEMPLO: reemplácelos por casos reales, anonimizados y autorizados por escrito,
// y cambie CASOS_DE_EJEMPLO a false para quitar el aviso.
export const CASOS_DE_EJEMPLO = true;
export type CasoResuelto = { area: string; icono: NombreIcono; duracion: string; titulo: string; situacion: string; hicimos: string; resultado: string; leccion: string };
export const CASOS: CasoResuelto[] = [
  { area: 'Procesal civil', icono: 'procesal', duracion: '7 meses', titulo: 'Una contestación a tiempo cambió el rumbo de un cobro', situacion: 'Una comerciante recibió una demanda por una deuda que ya había pagado en parte. Llegó con 12 de los 20 días de traslado ya corridos.', hicimos: 'Organizamos sus recibos y contestamos dentro del término, con excepción de pago parcial y la prueba de cada abono.', resultado: 'El juez reconoció los pagos y la condena se redujo al saldo real.', leccion: 'cuente los días desde la notificación y busque apoyo sin esperar al último momento.' },
  { area: 'Laboral', icono: 'laboral', duracion: '3 meses', titulo: 'Liquidación completa sin llegar a juicio', situacion: 'Un trabajador fue despedido tras cuatro años y la empresa le pagó solo el último mes.', hicimos: 'Calculamos prestaciones, vacaciones e indemnización, y presentamos la reclamación con soporte de cada valor.', resultado: 'La empresa aceptó conciliar y pagó el valor reclamado.', leccion: 'guarde sus desprendibles de pago; son la prueba más útil en un reclamo laboral.' },
  { area: 'Sucesiones', icono: 'sucesiones', duracion: '4 meses', titulo: 'Tres hermanos, una herencia y un acuerdo en notaría', situacion: 'Tres hermanos heredaron una casa y una cuenta de ahorros, y no sabían cómo empezar.', hicimos: 'Reunimos los documentos, propusimos una partición que todos aceptaron y adelantamos la sucesión ante notaría.', resultado: 'La casa quedó registrada a nombre de los herederos, sin juicio.', leccion: 'si hay acuerdo entre herederos, la vía notarial suele ser más rápida y económica.' },
  { area: 'Contratos', icono: 'contratos', duracion: '2 semanas', titulo: 'Una revisión antes de firmar evitó un problema', situacion: 'Una pareja iba a arrendar un local con una cláusula penal de seis cánones y reparaciones a su cargo.', hicimos: 'Revisamos el contrato y propusimos cambios razonables al arrendador.', resultado: 'Firmaron un contrato equilibrado, con reglas claras de salida.', leccion: 'lo que no se negocia antes de firmar es difícil de cambiar después.' },
];

// ---------------------------------------------------------------- Guía útil
export const PLAZOS = [
  { situacion: 'Contestar una demanda en proceso verbal', norma: 'CGP, art. 369', plazo: '20 días hábiles' },
  { situacion: 'Contestar en proceso verbal sumario', norma: 'CGP, art. 391', plazo: '10 días hábiles' },
  { situacion: 'Proponer excepciones en un proceso ejecutivo', norma: 'CGP, art. 442', plazo: '10 días hábiles' },
  { situacion: 'Apelar un auto por escrito', norma: 'CGP, art. 322', plazo: '3 días hábiles' },
  { situacion: 'Reclamar derechos laborales', norma: 'CST, art. 488', plazo: '3 años' },
];
export const QUE_TRAER = [
  'Su documento de identidad.',
  'La notificación, demanda o carta que recibió, con la fecha.',
  'Contratos, recibos, facturas o pagarés relacionados.',
  'Mensajes o correos con la otra parte.',
  'Una línea de tiempo corta: qué pasó y cuándo.',
];
export const PREGUNTAS = [
  { p: '¿Cuánto cuesta la primera consulta?', r: 'La consulta inicial tiene un valor fijo que le informo al agendar. Si decide contratar el caso, ese valor se descuenta de los honorarios.' },
  { p: '¿Una cita virtual sirve igual que una presencial?', r: 'Sí. Revisamos los documentos en pantalla y usted recibe el mismo diagnóstico por escrito. Las audiencias también pueden ser virtuales cuando el juzgado lo permite.' },
  { p: '¿Cuánto dura un proceso?', r: 'Depende del tipo de proceso y del juzgado. En el diagnóstico le doy un estimado con las etapas y las fechas probables, y lo actualizo si algo cambia.' },
  { p: '¿Siempre hay que ir a juicio?', r: 'No. Muchos casos se resuelven con una conciliación o un acuerdo. Si hay una salida más corta y segura para usted, se la propongo primero.' },
  { p: '¿Cómo sé en qué va mi caso?', r: 'Le envío cada novedad y un resumen con la siguiente fecha importante. Puede escribirme cuando quiera y le respondo en máximo un día hábil.' },
];

// ---------------------------------------------------------------- Agenda
export const TEMAS_CITA = ['Procesal civil (demanda o proceso en curso)', 'Civil', 'Laboral', 'Familia', 'Sucesiones', 'Contratos', 'No estoy seguro'];
export const HORAS_CITA = ['8:00 a. m.', '9:00 a. m.', '10:00 a. m.', '11:00 a. m.', '2:00 p. m.', '3:00 p. m.', '4:00 p. m.', '5:00 p. m.'];
export const DIAS_A_MOSTRAR = 10;

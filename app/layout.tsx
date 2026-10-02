import type { Metadata, Viewport } from 'next';
import '../design-system/tokens.css';
import './globals.css';
import { CONTACTO } from '@/lib/contenido';

const url = process.env.NEXT_PUBLIC_SITIO_URL || 'https://arroyoguzman.co';
const descripcion =
  'Tania Arroyo Guzmán, abogada procesalista civil. Procesos civiles, laborales, de familia, sucesiones y contratos, con plazos claros. Citas presenciales y virtuales.';

export const metadata: Metadata = {
  metadataBase: new URL(url),
  title: 'Arroyo Guzmán Abogados · Tania Arroyo Guzmán, procesalista civil',
  description: descripcion,
  alternates: { canonical: '/' },
  openGraph: { title: 'Arroyo Guzmán · Cada término, cumplido.', description: descripcion, url, siteName: 'Arroyo Guzmán', locale: 'es_CO', type: 'website' },
  robots: { index: true, follow: true },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  viewportFit: 'cover',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#F4F5F2' },
    { media: '(prefers-color-scheme: dark)', color: '#0D1917' },
  ],
};

const datosEstructurados = {
  '@context': 'https://schema.org',
  '@type': 'LegalService',
  name: 'Arroyo Guzmán',
  description: descripcion,
  url,
  email: CONTACTO.correo,
  telephone: CONTACTO.telefono,
  address: { '@type': 'PostalAddress', streetAddress: CONTACTO.direccion, addressLocality: CONTACTO.ciudad, addressCountry: 'CO' },
  areaServed: 'CO',
  sameAs: [`https://instagram.com/${CONTACTO.instagram.replace('@', '')}`],
  founder: { '@type': 'Person', name: CONTACTO.nombre, jobTitle: 'Abogada procesalista civil' },
  knowsAbout: ['Derecho procesal civil', 'Derecho civil', 'Derecho laboral', 'Derecho de familia', 'Sucesiones', 'Contratos'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es-CO">
      <body>
        {children}
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(datosEstructurados) }} />
      </body>
    </html>
  );
}

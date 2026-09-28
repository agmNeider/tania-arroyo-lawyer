import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const url = process.env.NEXT_PUBLIC_SITIO_URL || 'https://arroyoguzman.co';
  return { rules: { userAgent: '*', allow: '/', disallow: '/api/' }, sitemap: `${url}/sitemap.xml` };
}

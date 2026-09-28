import type { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  const url = process.env.NEXT_PUBLIC_SITIO_URL || 'https://arroyoguzman.co';
  return [{ url, changeFrequency: 'monthly', priority: 1 }];
}

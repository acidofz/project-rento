import type { Metadata } from 'next';
import './globals.css';
import { AuthProvider } from '@/contexts/AuthContext';
import { LangProvider } from '@/contexts/LangContext';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://uy-click.uz';

export const metadata: Metadata = {
  title: 'UY-CLICK — Недвижимость в Самарканде: аренда и продажа',
  description: 'Снимайте, сдавайте и покупайте недвижимость в Самарканде напрямую без посредников и комиссий.',
  metadataBase: new URL(SITE_URL),
  openGraph: {
    type: 'website',
    siteName: 'UY-CLICK',
    locale: 'ru_RU',
    url: SITE_URL,
  },
  robots: { index: true, follow: true },
};

const websiteJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'UY-CLICK',
  url: SITE_URL,
  description: 'Аренда и продажа недвижимости в Самарканде без посредников',
  potentialAction: {
    '@type': 'SearchAction',
    target: { '@type': 'EntryPoint', urlTemplate: `${SITE_URL}/listings?q={search_term_string}` },
    'query-input': 'required name=search_term_string',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <head>
        <meta name="theme-color" content="#0d9488" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteJsonLd) }}
        />
      </head>
      <body className="min-h-screen flex flex-col bg-gray-50 antialiased">
        <AuthProvider>
          <LangProvider>
            <Navbar />
            <main className="flex-1">{children}</main>
            <Footer />
          </LangProvider>
        </AuthProvider>
      </body>
    </html>
  );
}

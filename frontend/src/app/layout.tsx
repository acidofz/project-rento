import type { Metadata } from 'next';
import './globals.css';
import { AuthProvider } from '@/contexts/AuthContext';
import { LangProvider } from '@/contexts/LangContext';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';

export const metadata: Metadata = {
  title: 'UY-CLICK — Аренда жилья без посредников в Ташкенте',
  description: 'Снимайте и сдавайте квартиры по всему Узбекистану напрямую без посредников и комиссий.',
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? 'https://uy-click.uz'),
  openGraph: {
    type: 'website',
    siteName: 'UY-CLICK',
    locale: 'ru_RU',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <head>
        <meta name="theme-color" content="#0d9488" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
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

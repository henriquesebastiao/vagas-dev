import { IBM_Plex_Mono, IBM_Plex_Sans } from "next/font/google";
import Script from "next/script";
import "./globals.css";

const plexSans = IBM_Plex_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-plex-sans",
});

const plexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-plex-mono",
});

export const metadata = {
  title: "Vagas Dev",
  description:
    "Vagas para desenvolvedores no Brasil, coletadas da Gupy e do LinkedIn e atualizadas automaticamente.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR" className={`${plexSans.variable} ${plexMono.variable}`}>
      <head>
        <script
          defer
          src="https://umami.henriquesebastiao.com/script.js"
          data-website-id="7562705b-6fb8-44ad-a836-0ba266cdfcab"
        />
      </head>
      <body>
        {/* Configuração de execução (URL da API); ver public/config.js */}
        <Script src="/config.js" strategy="beforeInteractive" />
        {children}
      </body>
    </html>
  );
}

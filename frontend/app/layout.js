// Layout global — envolve todas as páginas do Next.js.
// Aqui você configura o <head> (título, fontes, favicon) e estilos globais.

import { DM_Sans } from "next/font/google";

// Importa a fonte DM Sans do Google Fonts de forma otimizada
const dmSans = DM_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata = {
  title: "Vagas DEV",
  description: "Agregador automático de vagas de emprego",
};

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body className={dmSans.className} style={{ margin: 0, padding: 0 }}>
        {children}
      </body>
    </html>
  );
}

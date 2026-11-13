// Tela exibida quando a API não responde. A interface fica no Cloudflare
// Pages e continua acessível mesmo com a API fora do ar, então mostramos uma
// mensagem amigável de manutenção em vez de um erro.

import { Cog } from "lucide-react";

export default function Maintenance() {
  return (
    <main className="maintenance" role="status" aria-live="polite">
      <div className="maintenance__gears" aria-hidden="true">
        <Cog className="gear gear--big" size={72} strokeWidth={1.5} />
        <Cog className="gear gear--small" size={44} strokeWidth={1.5} />
      </div>

      <h1 className="maintenance__title">Estamos em manutenção</h1>
      <p className="maintenance__text">
        A Vagas Dev está passando por uma manutenção rápida para continuar
        trazendo as melhores vagas para você. Voltamos em instantes.
      </p>

      <p className="maintenance__status mono">
        <span className="pulse" aria-hidden="true" />
        Esta página se atualiza sozinha quando tudo estiver pronto
      </p>
    </main>
  );
}

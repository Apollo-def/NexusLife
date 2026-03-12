import { Button } from "@/components/ui/button";
import { Instagram, Facebook, Linkedin } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-primary text-primary-foreground py-12">
      <div className="container">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
          {/* Column 1 */}
          <div className="space-y-3">
            <h4 className="font-semibold text-sm text-accent">Quem somos?</h4>
            <ul className="space-y-2 text-xs text-primary-foreground/70">
              <li><a href="#" className="hover:text-accent transition-colors">Sobre nós</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">Nossa missão</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">Nosso objetivo</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">FAQ</a></li>
            </ul>
          </div>

          {/* Column 2 */}
          <div className="space-y-3">
            <h4 className="font-semibold text-sm text-accent">Recursos</h4>
            <ul className="space-y-2 text-xs text-primary-foreground/70">
              <li><a href="#" className="hover:text-accent transition-colors">Gestão de e-mails</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">Organização de tarefas</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">Dicas</a></li>
            </ul>
          </div>

          {/* Column 3 */}
          <div className="space-y-3">
            <h4 className="font-semibold text-sm text-accent">Suporte</h4>
            <ul className="space-y-2 text-xs text-primary-foreground/70">
              <li><a href="#" className="hover:text-accent transition-colors">Central de ajuda</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">Comunidade</a></li>
              <li><a href="#" className="hover:text-accent transition-colors">Suporte técnico</a></li>
            </ul>
          </div>

          {/* Column 4 - Social + Contact */}
          <div className="space-y-4">
            <div className="flex gap-3">
              <a href="#" className="w-9 h-9 rounded-full bg-primary-foreground/10 flex items-center justify-center hover:bg-accent/20 transition-colors">
                <Instagram className="w-4 h-4" />
              </a>
              <a href="#" className="w-9 h-9 rounded-full bg-primary-foreground/10 flex items-center justify-center hover:bg-accent/20 transition-colors">
                <Facebook className="w-4 h-4" />
              </a>
              <a href="#" className="w-9 h-9 rounded-full bg-primary-foreground/10 flex items-center justify-center hover:bg-accent/20 transition-colors">
                <Linkedin className="w-4 h-4" />
              </a>
            </div>
            <Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90 text-xs">
              Contato
            </Button>
          </div>
        </div>

        <div className="border-t border-primary-foreground/10 pt-6 text-center">
          <p className="text-xs text-primary-foreground/50">
            © 2024 NexusLife. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

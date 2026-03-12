import { Button } from "@/components/ui/button";
import { Menu, X } from "lucide-react";
import { useState } from "react";

const Header = () => {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full bg-background/95 backdrop-blur border-b border-border">
      <div className="container flex h-16 items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="flex items-center">
            <span className="text-xl font-bold text-primary">nexus</span>
            <span className="text-xl font-bold text-accent">life</span>
            <span className="text-accent ml-0.5">✦</span>
          </div>
        </div>

        {/* Nav Desktop */}
        <nav className="hidden md:flex items-center gap-1">
          <Button variant="ghost" size="sm" className="text-sm font-medium text-muted-foreground hover:text-primary">
            Eu quero trabalhar
          </Button>
          <Button variant="ghost" size="sm" className="text-sm font-medium text-muted-foreground hover:text-primary">
            Eu quero contratar
          </Button>
        </nav>

        {/* Actions Desktop */}
        <div className="hidden md:flex items-center gap-2">
          <Button variant="outline" size="sm">Entrar</Button>
          <Button size="sm" className="bg-primary text-primary-foreground hover:bg-primary/90">
            Cadastrar-se
          </Button>
        </div>

        {/* Mobile Toggle */}
        <button
          className="md:hidden p-2 text-foreground"
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          {mobileOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-border bg-background px-4 pb-4 pt-2 space-y-2">
          <Button variant="ghost" className="w-full justify-start text-muted-foreground">Eu quero trabalhar</Button>
          <Button variant="ghost" className="w-full justify-start text-muted-foreground">Eu quero contratar</Button>
          <div className="flex gap-2 pt-2">
            <Button variant="outline" size="sm" className="flex-1">Entrar</Button>
            <Button size="sm" className="flex-1">Cadastrar-se</Button>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;

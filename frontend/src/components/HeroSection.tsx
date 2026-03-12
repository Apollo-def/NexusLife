import { Button } from "@/components/ui/button";
import { Bot, Brain, Cpu, Sparkles } from "lucide-react";

const HeroSection = () => {
  return (
    <section className="relative overflow-hidden bg-primary py-16 md:py-24">
      {/* Subtle pattern overlay */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-10 left-10 w-32 h-32 rounded-full bg-accent/30 blur-3xl" />
        <div className="absolute bottom-10 right-20 w-40 h-40 rounded-full bg-accent/20 blur-3xl" />
      </div>

      <div className="container relative z-10">
        <div className="grid md:grid-cols-2 gap-10 items-center">
          {/* Text */}
          <div className="text-primary-foreground space-y-6">
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold leading-tight">
              Assistente inteligente pronto para simplificar{" "}
              <span className="text-accent underline decoration-accent/50 underline-offset-4">
                sua rotina
              </span>
            </h1>
            <p className="text-primary-foreground/80 text-base md:text-lg max-w-md leading-relaxed">
              Conecte-se com seus aplicativos favoritos e deixe o NexusLife cuidar das tarefas repetitivas, fornecer sugestões inteligentes, organizar compromissos e gerenciar interrupções importantes com segurança e praticidade.
            </p>
            <div className="flex flex-wrap gap-3">
              <Button className="bg-accent text-accent-foreground hover:bg-accent/90 font-semibold px-6">
                Começar Agora
              </Button>
              <Button variant="outline" className="border-primary-foreground/30 text-primary-foreground hover:bg-primary-foreground/10">
                Veja quer trabalhar?
              </Button>
            </div>
          </div>

          {/* AI Illustration */}
          <div className="flex justify-center">
            <div className="relative w-64 h-64 md:w-80 md:h-80">
              {/* Central circle */}
              <div className="absolute inset-4 rounded-full bg-primary-foreground/10 border-2 border-accent/40 flex items-center justify-center">
                <div className="relative">
                  <Bot className="w-20 h-20 md:w-28 md:h-28 text-accent" strokeWidth={1.5} />
                  <div className="absolute -top-2 -right-2">
                    <Sparkles className="w-6 h-6 text-accent animate-pulse" />
                  </div>
                </div>
              </div>

              {/* Orbiting icons */}
              <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-2 bg-primary-foreground/15 rounded-full p-3 border border-accent/30">
                <Brain className="w-5 h-5 text-accent" />
              </div>
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-2 bg-primary-foreground/15 rounded-full p-3 border border-accent/30">
                <Cpu className="w-5 h-5 text-accent" />
              </div>
              <div className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-2 bg-primary-foreground/15 rounded-full p-3 border border-accent/30">
                <Sparkles className="w-5 h-5 text-accent" />
              </div>
              <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-2 bg-primary-foreground/15 rounded-full p-3 border border-accent/30">
                <Bot className="w-5 h-5 text-accent" />
              </div>

              {/* Decorative ring */}
              <div className="absolute inset-0 rounded-full border border-dashed border-accent/20 animate-spin" style={{ animationDuration: '30s' }} />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;

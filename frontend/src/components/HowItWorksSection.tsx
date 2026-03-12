import { Cable, BellRing, ListChecks } from "lucide-react";

const steps = [
  {
    icon: Cable,
    title: "Conecte seus aplicativos",
    step: "01",
  },
  {
    icon: BellRing,
    title: "Sugestões e notificações",
    step: "02",
  },
  {
    icon: ListChecks,
    title: "Automatize tarefas",
    step: "03",
  },
];

const HowItWorksSection = () => {
  return (
    <section className="py-16 md:py-24 bg-muted">
      <div className="container">
        <div className="text-center mb-12 space-y-3">
          <h2 className="text-2xl md:text-3xl font-bold text-foreground">Como funciona?</h2>
          <p className="text-muted-foreground max-w-md mx-auto">
            Organize sua vida digital de forma automática e inteligente.
          </p>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-center gap-6 md:gap-12">
          {steps.map((step, index) => (
            <div key={index} className="flex flex-col items-center text-center group">
              <div className="relative mb-4">
                <div className="w-20 h-20 rounded-full bg-background border-2 border-primary/20 flex items-center justify-center group-hover:border-accent group-hover:shadow-lg transition-all duration-300">
                  <step.icon className="w-8 h-8 text-primary group-hover:text-accent transition-colors" strokeWidth={1.5} />
                </div>
                <span className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-accent text-accent-foreground text-xs font-bold flex items-center justify-center">
                  {step.step}
                </span>
              </div>
              <p className="font-medium text-sm text-foreground">{step.title}</p>

              {/* Connector line (desktop) */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute">
                  {/* Handled by gap */}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;

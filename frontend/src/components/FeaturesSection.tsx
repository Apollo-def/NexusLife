import { Shield, Zap, Link2, CalendarClock } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const features = [
  {
    icon: Shield,
    title: "Segurança e privacidade",
    description: "Proteção de dados com tecnologia de criptografia avançada para sua tranquilidade.",
    color: "text-primary",
    bg: "bg-primary/10",
  },
  {
    icon: Zap,
    title: "Automação inteligente",
    description: "O NexusLife simplifica processos automatizando tarefas, otimizando seu tempo.",
    color: "text-accent",
    bg: "bg-accent/10",
  },
  {
    icon: Link2,
    title: "Integração de serviços",
    description: "Uma solução para conectar, organizar e otimizar seus aplicativos favoritos.",
    color: "text-primary",
    bg: "bg-primary/10",
  },
  {
    icon: CalendarClock,
    title: "Organização de rotina",
    description: "Controle compromissos e tarefas em um só lugar de forma inteligente.",
    color: "text-accent",
    bg: "bg-accent/10",
  },
];

const FeaturesSection = () => {
  return (
    <section className="py-16 md:py-24 bg-background">
      <div className="container">
        <h2 className="text-2xl md:text-3xl font-bold text-center text-foreground mb-12">
          O que o NexusLife oferece?
        </h2>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Card
              key={index}
              className="group border border-border hover:border-primary/30 hover:shadow-lg transition-all duration-300 text-center"
            >
              <CardContent className="pt-8 pb-6 px-6 space-y-4">
                <div className={`inline-flex p-4 rounded-2xl ${feature.bg} mx-auto`}>
                  <feature.icon className={`w-8 h-8 ${feature.color}`} strokeWidth={1.5} />
                </div>
                <h3 className="font-semibold text-foreground text-sm">{feature.title}</h3>
                <p className="text-muted-foreground text-xs leading-relaxed">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;

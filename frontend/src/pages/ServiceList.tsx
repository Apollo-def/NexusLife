import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface Category {
  id: number;
  name: string;
  description: string;
}

interface Service {
  id: number;
  title: string;
  description: string;
  price: string;
  category: Category;
  freelancer: {
    id: number;
    username: string;
  };
  is_active: boolean;
  created_at: string;
}

const ServiceList = () => {
  const [services, setServices] = useState<Service[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCategories();
    fetchServices();
  }, [selectedCategory]);

  const fetchCategories = async () => {
    try {
      const response = await fetch("/api/marketplace/categories/");
      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      }
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  const fetchServices = async () => {
    try {
      const url = selectedCategory
        ? `/api/marketplace/services/?category=${selectedCategory}`
        : "/api/marketplace/services/";
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setServices(data);
      }
    } catch (error) {
      console.error("Error fetching services:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="container mx-auto px-4 py-8">Carregando...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Serviços Disponíveis</h1>

      <div className="mb-6">
        <Select value={selectedCategory} onValueChange={setSelectedCategory}>
          <SelectTrigger className="w-64">
            <SelectValue placeholder="Todas as categorias" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">Todas as categorias</SelectItem>
            {categories.map((category) => (
              <SelectItem key={category.id} value={category.id.toString()}>
                {category.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.map((service) => (
          <Card key={service.id}>
            <CardHeader>
              <CardTitle>{service.title}</CardTitle>
              <Badge variant="secondary">{service.category.name}</Badge>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                {service.description.length > 100
                  ? `${service.description.substring(0, 100)}...`
                  : service.description}
              </p>
              <div className="flex justify-between items-center">
                <span className="text-lg font-bold text-green-600">
                  R$ {service.price}
                </span>
                <Button asChild>
                  <Link to={`/marketplace/service/${service.id}`}>Ver Detalhes</Link>
                </Button>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Por: {service.freelancer.username}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {services.length === 0 && (
        <p className="text-center text-gray-500 mt-8">Nenhum serviço encontrado.</p>
      )}

      <div className="mt-8">
        <Button asChild>
          <Link to="/marketplace/service/create">Criar Novo Serviço</Link>
        </Button>
      </div>
    </div>
  );
};

export default ServiceList;
from ninja import NinjaAPI, Redoc
from services.models import Provider, Service, Address, Contact
from .models import (ServiceOutputSchema, ProviderOutputSchema, AddressOutputSchema, ContactOutputSchema, MessageSchema, ServiceInputSchema)
from django.contrib.auth.models import User
from typing import List
from datetime import datetime

api = NinjaAPI(docs=Redoc(), title="Documentación para el servicio", version="1.0.0", description="Esta es la documentación de la API")


@api.get("/services", response={200:List[ServiceOutputSchema]}, summary="Permite obtener todos los servicios vigentes")
def get_servicies(request):
    services = Service.objects.all().order_by()

    results = []

    for service in services:
        contact_providers = Contact.objects.filter(provider=service.provider.id)
        contact_data = []
        for contact_provider in contact_providers:
            contact_data.append({
                'provider': service.provider.id,
                'type': contact_provider.type,
                'first_name': contact_provider.first_name,
                'last_name': contact_provider.last_name,
                'email': contact_provider.email,
                'phone': contact_provider.phone,
                'mobile':contact_provider.mobile,
            })
        direccion_provider = Address.objects.filter(provider=service.provider.id).first()
        direccion = {
            'provider': direccion_provider.provider.id if direccion_provider is not None else 'Sin informacion',
            'type': direccion_provider.type if direccion_provider is not None else 'Sin informacion',
            'direction1': direccion_provider.address1 if direccion_provider is not None else 'Sin informacion',
            'direction2': direccion_provider.address2 if direccion_provider is not None else 'Sin informacion',
            'codepost': direccion_provider.zipcode if direccion_provider is not None and direccion_provider.zipcode is not None else 'Sin informacion',
            'city': direccion_provider.city if direccion_provider is not None else 'Sin informacion',
            'region': direccion_provider.region if direccion_provider is not None else 'Sin informacion',
            'country': direccion_provider.country if direccion_provider is not None else 'Sin informacion',
        }
        result = {
            'name': service.name,
            'description': service.description,
            'provider': {
                'fantasy': service.provider.fantasy_name,
                'tax_name': service.provider.tax_name,
                'tax_id': service.provider.tax_id,
                'enable': service.provider.enabled,
            },
            'valeu': service.price,
            'from_date': service.from_date.strftime("%d/%m/%Y"),
            'thru_date': service.thru_date.strftime("%d/%m/%Y"),
            'contact': contact_data,
            'direction': direccion,
        }
        results.append(result)
    return results



@api.get("service/{id}", response={200:ServiceOutputSchema, 404:MessageSchema}, summary="Servicio que obtiene un servicio en particular")
def get_service(request, id):

    try: 
        service = Service.objects.get(id=id)
        contact_providers = Contact.objects.filter(provider=service.provider.id)
        contact_data = []
        for contact_provider in contact_providers:
            contact_data.append({
                'provider': service.provider.id,
                'type': contact_provider.type,
                'first_name': contact_provider.first_name,
                'last_name': contact_provider.last_name,
                'email': contact_provider.email,
                'phone': contact_provider.phone,
                'mobile':contact_provider.mobile,
            })
        direccion_provider = Address.objects.filter(provider=service.provider.id).first()
        direccion = {
            'provider': direccion_provider.provider.id if direccion_provider is not None else 'Sin informacion',
            'type': direccion_provider.type if direccion_provider is not None else 'Sin informacion',
            'direction1': direccion_provider.address1 if direccion_provider is not None else 'Sin informacion',
            'direction2': direccion_provider.address2 if direccion_provider is not None else 'Sin informacion',
            'codepost': direccion_provider.zipcode if direccion_provider is not None and direccion_provider.zipcode is not None else 'Sin informacion',
            'city': direccion_provider.city if direccion_provider is not None else 'Sin informacion',
            'region': direccion_provider.region if direccion_provider is not None else 'Sin informacion',
            'country': direccion_provider.country if direccion_provider is not None else 'Sin informacion',
        }
        result = {
            'nome': service.name,
            'description': service.description,
            'provider': {
                'fantasy': service.provider.fantasy_name,
                'tax_name': service.provider.tax_name,
                'tax_id': service.provider.tax_id,
                'enable': service.provider.enabled,
            },
            'valeu': service.price,
            'from_date': service.from_date.strftime("%d/%m/%Y"),
            'thru_date': service.thru_date.strftime("%d/%m/%Y"),
            'contact': contact_data,
            'direction': direccion,
        }
        return result
    except Exception:
        return 404, { 'message': 'service not found' }



@api.post("/service", response={200:MessageSchema, 404:MessageSchema}, summary="Servicio crea un servicio")
def save_servicio(request, p: ServiceInputSchema):

    try: 
        provider = Provider.objects.get(id=p.provider)
    except Exception:
        return 404, { 'message': 'provider not found' }

    service = {
        'name': p.name,
        'description': p.description,
        'provider': provider,
        'valeu': p.valeu,
        'from_date': datetime.strptime(p.from_date, "%d/%m/%Y"),
        'thru_date': datetime.strptime(p.thru_date, "%d/%m/%Y")
    }

    # Se crea el objeto directamente y se persiste    
    service = Service.objects.create(**service)
    service.save()
    return { 'message': 'Service has been created' }



@api.delete("service/{id}", response={200:MessageSchema, 404:MessageSchema}, summary="Elimina un servicio")
def delete_service(request, id: int):
   
    try: 
        service = Service.objects.get(id=id)
    except Exception:
        return 404, { 'message': 'Service not found' }
    
  
    service.delete()
    return { 'message': 'Service has been deleted' }

from pydantic import BaseModel


# Definition de notre schéma d'élément
class ItemSchema(BaseModel):
    name: str  # Le nom de l'élément, une chaîne de caratères est attendue
    description: str = None  # Une description optionnelle de l'élément, par défaut c'est None
    price: float  # Le prix de l'élément, un nombre flottant est attendu
    is_available: bool = True  # Un indicateur pour montrer si l'élément est disponible ou pas, par défaut c'est True

    class Config:
        from_attributes = True  # Permettre l'attribution des valeurs du schéma directement depuis les attributs

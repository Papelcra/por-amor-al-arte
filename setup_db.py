import os
import django

# 1. Configuración del entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import LineaArtistica, Genre

def run_setup():
    # Datos extraídos de tu PDF
    data = {
        "ARTES ESCÉNICAS": [
            "Teatro", "Danza", "Circo", "Performance y artes vivas"
        ],
        "MÚSICA": [
            "Interpretación", "Composición y producción", 
            "Investigación y pedagogía", "Lutería y oficios musicales"
        ],
        "ARTES PLÁSTICAS Y VISUAL": [
            "Artes bidimensionales", "Artes tridimensionales", "Fotografía", 
            "Arte contemporáneo", "Arte digital y nuevos medios", "Curaduría e investigación"
        ],
        "AUDIOVISUALES Y MEDIOS": [
            "Cine y realización", "Animación", "Narrativas digitales", 
            "Experiencias inmersivas", "Producción comunitaria y participativa"
        ],
        "LITERATURA": [
            "Creación literaria", "Literatura infantil y juvenil", "Narrativa gráfica", 
            "Traducción literaria", "Investigación y crítica", "Promoción de lectura y escritura"
        ],
        "ARTESANÍAS Y OFICIOS ART": [
            "Artesanía tradicional", "Oficios contemporáneos", 
            "Restauración y conservación", "Saberes ancestrales"
        ],
        "ARTES INTEGRADAS / INTERDISCIPLINARES": [
            "Cruces disciplinares", "Experiencias sensoriales", 
            "Arte y territorio", "Prácticas sociales y colaborativas"
        ],
        "FORMACIÓN, MEDIACIÓN Y EDUCACIÓN": [
            "Formación artística", "Mediación artística", 
            "Educación artística en la escuela", "Pedagogías críticas y comunitarias"
        ],
        "INVESTIGACIÓN Y DOCUMENTACIÓN": [
            "Investigación-creación", "Estudios críticos", 
            "Archivos y memoria", "Publicaciones"
        ]
    }

    print("--- Iniciando carga de categorías ---")
    
    for linea_nom, generos in data.items():
        linea, _ = LineaArtistica.objects.get_or_create(nombre=linea_nom)
        for gen_nom in generos:
            Genre.objects.get_or_create(nombre=gen_nom, linea=linea)

    print("--- Carga de categorías finalizada con éxito ---")

if __name__ == "__main__":
    run_setup()
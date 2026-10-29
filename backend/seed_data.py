"""
seed_data.py — Popula o MongoDB com produtos de exemplo realistas.
Execute: python seed_data.py
"""
import asyncio
import sys
import os
from decimal import Decimal

# Garante que o diretório atual seja o backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from database import get_motor_client, init_db
from models import Product

PRODUTOS = [
    # ─── Informática ─────────────────────────────────────────────────────
    {
        "name": "Notebook Dell Inspiron 15 3000",
        "description": (
            "Notebook ideal para estudos e trabalho do dia a dia. "
            "Processador Intel Core i5-1135G7, 8GB RAM DDR4, SSD 256GB, "
            "tela 15.6\" Full HD, Windows 11 Home. Ótimo custo-benefício."
        ),
        "category": "Informática",
        "brand": "Dell",
        "price": Decimal("2499.00"),
        "stock_quantity": 15,
        "image_url": "https://placehold.co/300x200/1a73e8/white?text=Dell+Inspiron+15",
        "product_url": "#produto-1",
    },
    {
        "name": "Notebook Lenovo IdeaPad 3",
        "description": (
            "Excelente para estudantes e uso cotidiano. "
            "AMD Ryzen 5 5500U, 8GB RAM, SSD 512GB, tela 15.6\" Full HD, "
            "bateria de longa duração, Windows 11."
        ),
        "category": "Informática",
        "brand": "Lenovo",
        "price": Decimal("2299.00"),
        "stock_quantity": 22,
        "image_url": "https://placehold.co/300x200/e84335/white?text=Lenovo+IdeaPad+3",
        "product_url": "#produto-2",
    },
    {
        "name": "Notebook Acer Aspire 5",
        "description": (
            "Performance e portabilidade para estudos e multimedia. "
            "Intel Core i5-1235U, 8GB RAM, SSD 512GB, tela 15.6\" IPS Full HD, "
            "design slim, leitor de impressão digital."
        ),
        "category": "Informática",
        "brand": "Acer",
        "price": Decimal("2799.00"),
        "stock_quantity": 10,
        "image_url": "https://placehold.co/300x200/34a853/white?text=Acer+Aspire+5",
        "product_url": "#produto-3",
    },
    {
        "name": "Mouse Logitech MX Master 3",
        "description": (
            "Mouse sem fio premium para produtividade. "
            "Sensor Darkfield 4000 DPI, scroll eletromagnético, "
            "conexão USB-C, compatível com Windows e Mac, autonomia 70 dias."
        ),
        "category": "Informática",
        "brand": "Logitech",
        "price": Decimal("549.00"),
        "stock_quantity": 30,
        "image_url": "https://placehold.co/300x200/fbbc04/black?text=MX+Master+3",
        "product_url": "#produto-4",
    },
    {
        "name": "Teclado Mecânico Redragon Kumara K552",
        "description": (
            "Teclado mecânico compacto TKL (87 teclas). "
            "Switches Red lineares, retroiluminação RGB, estrutura metálica, "
            "anti-ghosting, ideal para games e digitação."
        ),
        "category": "Informática",
        "brand": "Redragon",
        "price": Decimal("249.00"),
        "stock_quantity": 45,
        "image_url": "https://placehold.co/300x200/ea4335/white?text=Teclado+K552",
        "product_url": "#produto-5",
    },
    {
        "name": "Headset Logitech H390",
        "description": (
            "Headset com fio USB para home office e aulas online. "
            "Microfone com cancelamento de ruído, controles de volume no cabo, "
            "almofadas acolchoadas, plug-and-play."
        ),
        "category": "Informática",
        "brand": "Logitech",
        "price": Decimal("189.00"),
        "stock_quantity": 60,
        "image_url": "https://placehold.co/300x200/4285f4/white?text=H390+Headset",
        "product_url": "#produto-6",
    },
    # ─── Smartphones ─────────────────────────────────────────────────────
    {
        "name": "Samsung Galaxy A54 5G",
        "description": (
            "Smartphone intermediário com câmera tripla de 50MP. "
            "Processador Exynos 1380, 8GB RAM, 256GB armazenamento, "
            "tela Super AMOLED 6.4\" 120Hz, bateria 5000mAh, Android 13."
        ),
        "category": "Smartphones",
        "brand": "Samsung",
        "price": Decimal("1799.00"),
        "stock_quantity": 25,
        "image_url": "https://placehold.co/300x200/1565c0/white?text=Galaxy+A54",
        "product_url": "#produto-7",
    },
    {
        "name": "Xiaomi Redmi Note 12",
        "description": (
            "Custo-benefício excepcional. Câmera tripla 50MP, "
            "tela AMOLED 6.67\" 120Hz, bateria 5000mAh com carga 33W, "
            "4GB RAM, 128GB, MIUI 14."
        ),
        "category": "Smartphones",
        "brand": "Xiaomi",
        "price": Decimal("1199.00"),
        "stock_quantity": 40,
        "image_url": "https://placehold.co/300x200/ff6f00/white?text=Redmi+Note+12",
        "product_url": "#produto-8",
    },
    {
        "name": "iPhone 14 128GB",
        "description": (
            "Flagship da Apple com chip A15 Bionic. "
            "Câmera dupla 12MP, tela Super Retina XDR 6.1\", "
            "iOS 16, 5G, resistência à água IP68, carregamento rápido."
        ),
        "category": "Smartphones",
        "brand": "Apple",
        "price": Decimal("4499.00"),
        "stock_quantity": 8,
        "image_url": "https://placehold.co/300x200/37474f/white?text=iPhone+14",
        "product_url": "#produto-9",
    },
    {
        "name": "Motorola Moto G73 5G",
        "description": (
            "5G acessível com câmera de 50MP e tela de 120Hz. "
            "MediaTek Dimensity 930, 8GB RAM, 256GB, bateria 5000mAh, "
            "design premium com traseira de couro vegano."
        ),
        "category": "Smartphones",
        "brand": "Motorola",
        "price": Decimal("1349.00"),
        "stock_quantity": 18,
        "image_url": "https://placehold.co/300x200/00897b/white?text=Moto+G73",
        "product_url": "#produto-10",
    },
    {
        "name": "Samsung Galaxy S23 FE",
        "description": (
            "Fan Edition do Galaxy S23 com câmera tripla 50MP. "
            "Snapdragon 8 Gen 1, 8GB RAM, 256GB, tela Dynamic AMOLED 6.4\" 120Hz, "
            "bateria 4500mAh, Android 13."
        ),
        "category": "Smartphones",
        "brand": "Samsung",
        "price": Decimal("2699.00"),
        "stock_quantity": 12,
        "image_url": "https://placehold.co/300x200/283593/white?text=Galaxy+S23+FE",
        "product_url": "#produto-11",
    },
    # ─── Móveis para Escritório ───────────────────────────────────────────
    {
        "name": "Cadeira Gamer ThunderX3 TC3",
        "description": (
            "Cadeira ergonômica com apoio lombar ajustável. "
            "Reclinável até 180°, braços 3D, rodízios silenciosos, "
            "espuma de alta densidade, suporta até 120kg."
        ),
        "category": "Móveis para Escritório",
        "brand": "ThunderX3",
        "price": Decimal("899.00"),
        "stock_quantity": 7,
        "image_url": "https://placehold.co/300x200/b71c1c/white?text=Cadeira+TC3",
        "product_url": "#produto-12",
    },
    {
        "name": "Mesa para Computador MadeiraMadeira Work",
        "description": (
            "Mesa compacta para home office. "
            "Tampo em MDF 15mm, estrutura metálica, suporte para CPU, "
            "passa-cabos, dimensões: 120x50x75cm, cor branca."
        ),
        "category": "Móveis para Escritório",
        "brand": "MadeiraMadeira",
        "price": Decimal("449.00"),
        "stock_quantity": 14,
        "image_url": "https://placehold.co/300x200/5d4037/white?text=Mesa+Work",
        "product_url": "#produto-13",
    },
    {
        "name": "Suporte Monitor Ergonômico Multilaser",
        "description": (
            "Suporte articulado para monitor de até 32\". "
            "Braço giratório 360°, inclinação ajustável, fixação por grampo, "
            "passa-cabo integrado, suporta até 8kg."
        ),
        "category": "Móveis para Escritório",
        "brand": "Multilaser",
        "price": Decimal("179.00"),
        "stock_quantity": 35,
        "image_url": "https://placehold.co/300x200/455a64/white?text=Suporte+Monitor",
        "product_url": "#produto-14",
    },
    {
        "name": "Cadeira Escritório Presidente Anatômica",
        "description": (
            "Cadeira de escritório profissional com base giratória. "
            "Encosto anatômico, assento almofadado, braços fixos, "
            "regulagem de altura a gás, rodízios de nylon, até 110kg."
        ),
        "category": "Móveis para Escritório",
        "brand": "Pelegrin",
        "price": Decimal("399.00"),
        "stock_quantity": 20,
        "image_url": "https://placehold.co/300x200/1b5e20/white?text=Cadeira+Pres.",
        "product_url": "#produto-15",
    },
    {
        "name": "Luminária LED de Mesa Recarregável",
        "description": (
            "Luminária de mesa com 3 modos de cor e dimmer. "
            "Bateria interna recarregável via USB-C, pescoço flexível 360°, "
            "ideal para leitura e home office, 5W, 400 lúmens."
        ),
        "category": "Móveis para Escritório",
        "brand": "Baseus",
        "price": Decimal("129.00"),
        "stock_quantity": 50,
        "image_url": "https://placehold.co/300x200/f57f17/black?text=Luminaria+LED",
        "product_url": "#produto-16",
    },
    # ─── Acessórios ───────────────────────────────────────────────────────
    {
        "name": "Carregador Turbo Samsung 25W USB-C",
        "description": (
            "Carregador original Samsung com tecnologia Super Fast Charging. "
            "25W, saída USB-C, compatível com Galaxy S e A Series, "
            "proteção contra sobretensão e superaquecimento."
        ),
        "category": "Acessórios",
        "brand": "Samsung",
        "price": Decimal("89.00"),
        "stock_quantity": 80,
        "image_url": "https://placehold.co/300x200/0d47a1/white?text=Carregador+25W",
        "product_url": "#produto-17",
    },
    {
        "name": "Cabo USB-C para USB-C 2m Anker",
        "description": (
            "Cabo de alta velocidade com transferência de até 480Mbps. "
            "Suporta carga de até 60W, revestimento em nylon trançado durável, "
            "2 metros de comprimento, compatível com notebooks e smartphones."
        ),
        "category": "Acessórios",
        "brand": "Anker",
        "price": Decimal("59.00"),
        "stock_quantity": 100,
        "image_url": "https://placehold.co/300x200/212121/white?text=Cabo+USB-C",
        "product_url": "#produto-18",
    },
    {
        "name": "Película Vidro Temperado Galaxy A54",
        "description": (
            "Proteção de tela com vidro temperado 9H para Samsung Galaxy A54. "
            "Cobertura total, borda curva, instalação fácil com kit incluído, "
            "pacote com 2 películas."
        ),
        "category": "Acessórios",
        "brand": "Capinhas Brasil",
        "price": Decimal("29.00"),
        "stock_quantity": 200,
        "image_url": "https://placehold.co/300x200/616161/white?text=Pelicula+A54",
        "product_url": "#produto-19",
    },
    {
        "name": "Hub USB-C 7 em 1 Baseus",
        "description": (
            "Hub multifuncional com 7 portas: HDMI 4K, USB-A 3.0 x3, "
            "SD/MicroSD, USB-C PD 100W. Ideal para notebooks com poucas portas, "
            "design compacto, plug-and-play."
        ),
        "category": "Acessórios",
        "brand": "Baseus",
        "price": Decimal("199.00"),
        "stock_quantity": 45,
        "image_url": "https://placehold.co/300x200/4a148c/white?text=Hub+7em1",
        "product_url": "#produto-20",
    },
]


async def seed():
    """Popula os produtos no MongoDB."""
    client = get_motor_client()
    await init_db(client)

    count = await Product.count()
    if count > 0:
        print(f"⚠️  Já existem {count} produtos no MongoDB.")
        resposta = input("Deseja recriar os dados de exemplo? (s/N): ").strip().lower()
        if resposta != "s":
            print("❌ Seeding cancelado.")
            client.close()
            return
        await Product.delete_all()
        print("🗑️  Produtos anteriores removidos.")

    # Insere documentos
    for dados in PRODUTOS:
        p = Product(**dados)
        await p.insert()

    print(f"✅ {len(PRODUTOS)} produtos cadastrados com sucesso no MongoDB!")
    categorias = set(p["category"] for p in PRODUTOS)
    for cat in sorted(categorias):
        qtd = sum(1 for p in PRODUTOS if p["category"] == cat)
        print(f"  • {cat}: {qtd} produto(s)")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())

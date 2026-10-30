"""
seed_data.py — Popula o MongoDB Atlas com materiais de construção reais da Nikkei.
Categorias:
- Básico & Alvenaria
- Pintura & Impermeabilização
- Hidráulica & Elétrica
- Pisos & Acabamentos
- Ferramentas & Equipamentos
"""
import asyncio
import sys
import os
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from database import get_motor_client, init_db
from models import Product

MATERIAIS_CONSTRUCAO = [
    # ─── Básico & Alvenaria ──────────────────────────────────────────────
    {
        "name": "Cimento Votoran Todas as Obras CP II-E-32 50kg",
        "description": (
            "Cimento Portland de uso geral indicado para reboco, contrapiso, calçadas, "
            "argamassa de assentamento e concreto estrutural. Secagem uniforme e alta resistência."
        ),
        "category": "Básico & Alvenaria",
        "brand": "Votoran",
        "price": Decimal("38.90"),
        "stock_quantity": 250,
        "image_url": "https://placehold.co/300x200/d5232a/white?text=Cimento+Votoran+50kg",
        "product_url": "#produto-cimento-votoran",
    },
    {
        "name": "Cimento Cauê Estrutural Alta Resistência CP V-ARI 50kg",
        "description": (
            "Cimento de alta resistência inicial para lajes, pilares, vigas e pré-moldados. "
            "Desforma rápida e máxima resistência para obras pesadas."
        ),
        "category": "Básico & Alvenaria",
        "brand": "Cauê",
        "price": Decimal("44.50"),
        "stock_quantity": 120,
        "image_url": "https://placehold.co/300x200/1d1d1f/white?text=Cimento+Caue+CPV",
        "product_url": "#produto-cimento-caue",
    },
    {
        "name": "Argamassa AC-II Cinza Votoran 20kg",
        "description": (
            "Argamassa colante multiuso para áreas internas e externas. Indicada para "
            "assentamento de pisos cerâmicos e revestimentos em paredes e lajes."
        ),
        "category": "Básico & Alvenaria",
        "brand": "Votoran",
        "price": Decimal("19.90"),
        "stock_quantity": 180,
        "image_url": "https://placehold.co/300x200/86868b/white?text=Argamassa+AC2+20kg",
        "product_url": "#produto-argamassa-ac2",
    },
    {
        "name": "Argamassa AC-III Branca Quartzolit Especial Porcelanato 20kg",
        "description": (
            "Alta aderência e flexibilidade para porcelanatos, pedras naturais, piscinas e "
            "fachadas. Uso interno e externo de alta performance."
        ),
        "category": "Básico & Alvenaria",
        "brand": "Quartzolit",
        "price": Decimal("36.90"),
        "stock_quantity": 90,
        "image_url": "https://placehold.co/300x200/d5232a/white?text=Quartzolit+AC3",
        "product_url": "#produto-quartzolit-ac3",
    },
    {
        "name": "Tijolo Cerâmico Baiano 8 Furos 9x19x19cm",
        "description": (
            "Tijolo furado cerâmico para alvenaria de vedação. Proporciona isolamento térmico e acústico, "
            "ótimo alinhamento para assentamento de paredes. Rendimento: ~25 un/m²."
        ),
        "category": "Básico & Alvenaria",
        "brand": "Cerâmica Regional",
        "price": Decimal("1.85"),
        "stock_quantity": 5000,
        "image_url": "https://placehold.co/300x200/a4181e/white?text=Tijolo+Baiano+8F",
        "product_url": "#produto-tijolo-baiano",
    },
    {
        "name": "Areia Média Lavada Ensacada 20kg",
        "description": (
            "Areia limpa e lavada pronta para uso, livre de impurezas. Perfeita para preparo "
            "de argamassa de emboço, reboco e concreto."
        ),
        "category": "Básico & Alvenaria",
        "brand": "Nikkei Mineradora",
        "price": Decimal("7.50"),
        "stock_quantity": 300,
        "image_url": "https://placehold.co/300x200/d2d2d7/black?text=Areia+Media+20kg",
        "product_url": "#produto-areia-media",
    },
    {
        "name": "Pedra Brita 1 Lavada Ensacada 20kg",
        "description": (
            "Brita graduationada número 1 ideal para concreto de fundação, colunas, vigas e calçadas. "
            "Saco prático e limpo para pequenas reformas e obras."
        ),
        "category": "Básico & Alvenaria",
        "brand": "Nikkei Mineradora",
        "price": Decimal("8.00"),
        "stock_quantity": 250,
        "image_url": "https://placehold.co/300x200/515154/white?text=Pedra+Brita+1",
        "product_url": "#produto-brita-1",
    },

    # ─── Pintura & Impermeabilização ─────────────────────────────────────
    {
        "name": "Impermeabilizante Vedacit Balde 18 Litros",
        "description": (
            "Aditivo impermeabilizante para concreto e argamassa de assentamento e reboco. "
            "Protege contra umidade de solo, baldrames, muros de arrimo e caixas d'água."
        ),
        "category": "Pintura & Impermeabilização",
        "brand": "Vedacit",
        "price": Decimal("149.00"),
        "stock_quantity": 40,
        "image_url": "https://placehold.co/300x200/d5232a/white?text=Vedacit+18L",
        "product_url": "#produto-vedacit-18l",
    },
    {
        "name": "Pintura Asfáltica Neutrol Vedacit 18 Litros",
        "description": (
            "Tinta asfáltica impermeabilizante de alta aderência para alicerces, baldrames, "
            "muros de contenção e estruturas enterradas de alvenaria e concreto."
        ),
        "category": "Pintura & Impermeabilização",
        "brand": "Vedacit",
        "price": Decimal("189.00"),
        "stock_quantity": 35,
        "image_url": "https://placehold.co/300x200/111113/white?text=Neutrol+18L",
        "product_url": "#produto-neutrol-18l",
    },
    {
        "name": "Tinta Acrílica Fosca Suvinil Rende Muito Branco Neve 18L",
        "description": (
            "Tinta super concentrada de altíssimo rendimento para paredes internas e externas. "
            "Baixo odor, acabamento fosco suave e excelente cobertura (rende até 500m² por demão)."
        ),
        "category": "Pintura & Impermeabilização",
        "brand": "Suvinil",
        "price": Decimal("349.90"),
        "stock_quantity": 28,
        "image_url": "https://placehold.co/300x200/d5232a/white?text=Suvinil+Rende+Muito+18L",
        "product_url": "#produto-suvinil-18l",
    },
    {
        "name": "Tinta Coral Proteção Sol & Chuva Impermeabilizante 18L",
        "description": (
            "Tinta acrílica elástica impermeabilizante para fachadas e muros externos. "
            "Previne e cobre microfissuras de até 0,5mm, resiste a mofo e intempéries."
        ),
        "category": "Pintura & Impermeabilização",
        "brand": "Coral",
        "price": Decimal("419.00"),
        "stock_quantity": 22,
        "image_url": "https://placehold.co/300x200/1d1d1f/white?text=Coral+Sol+Chuva+18L",
        "product_url": "#produto-coral-sol-chuva",
    },
    {
        "name": "Massa Corrida PVA Coral 25kg",
        "description": (
            "Massa para nivelamento e correção de superfícies internas de alvenaria e gesso. "
            "Fácil de aplicar e lixar, proporciona acabamento liso e requintado."
        ),
        "category": "Pintura & Impermeabilização",
        "brand": "Coral",
        "price": Decimal("69.90"),
        "stock_quantity": 45,
        "image_url": "https://placehold.co/300x200/e8e8ed/black?text=Massa+Corrida+25kg",
        "product_url": "#produto-massa-coral",
    },

    # ─── Hidráulica & Elétrica ───────────────────────────────────────────
    {
        "name": "Tubo PVC Esgoto 100mm (4 Polegadas) Barra 6 Metros Tigre",
        "description": (
            "Tubo reforçado para condução de esgoto sanitário e águas pluviais prediais. "
            "Fabricado em PVC de alta durabilidade com selo Tigre de qualidade."
        ),
        "category": "Hidráulica & Elétrica",
        "brand": "Tigre",
        "price": Decimal("78.50"),
        "stock_quantity": 55,
        "image_url": "https://placehold.co/300x200/d2d2d7/black?text=Tubo+Esgoto+100mm+Tigre",
        "product_url": "#produto-tubo-esgoto-100",
    },
    {
        "name": "Tubo PVC Soldável Água Fria 25mm (3/4\") Barra 6 Metros Tigre",
        "description": (
            "Tubo marrom de alta pressão para condução de água potável em instalações prediais. "
            "Conexão soldável rápida e segura contra vazamentos."
        ),
        "category": "Hidráulica & Elétrica",
        "brand": "Tigre",
        "price": Decimal("29.90"),
        "stock_quantity": 110,
        "image_url": "https://placehold.co/300x200/515154/white?text=Tubo+Agua+25mm+Tigre",
        "product_url": "#produto-tubo-25mm",
    },
    {
        "name": "Caixa d'Água Polietileno 1000 Litros com Tampa Fortlev",
        "description": (
            "Reservatório de água com tampa rosqueável de 1/4 de volta e travamento total. "
            "Proteção UV, superfície interna lisa e antimicrobiana fácil de limpar."
        ),
        "category": "Hidráulica & Elétrica",
        "brand": "Fortlev",
        "price": Decimal("389.00"),
        "stock_quantity": 15,
        "image_url": "https://placehold.co/300x200/1d1d1f/white?text=Caixa+Dagua+1000L",
        "product_url": "#produto-caixa-1000l",
    },
    {
        "name": "Cabo Flexível 2.5mm² 750V Antichama Rolo 100 Metros Sil",
        "description": (
            "Fio elétrico condutor de cobre puro para tomadas residenciais de uso geral (10A). "
            "Isolação termoplástica antichama e certificação Inmetro."
        ),
        "category": "Hidráulica & Elétrica",
        "brand": "Sil",
        "price": Decimal("219.00"),
        "stock_quantity": 38,
        "image_url": "https://placehold.co/300x200/d5232a/white?text=Fio+Sil+2.5mm+100m",
        "product_url": "#produto-fio-25mm",
    },
    {
        "name": "Cabo Flexível 4.0mm² 750V Antichama Rolo 100 Metros Sil",
        "description": (
            "Condutor ideal para chuveiros elétricos, ar-condicionado e circuitos de maior potência (20A/32A). "
            "Cobre 100% eletrolítico e flexibilidade extra para passar em conduítes."
        ),
        "category": "Hidráulica & Elétrica",
        "brand": "Sil",
        "price": Decimal("349.00"),
        "stock_quantity": 25,
        "image_url": "https://placehold.co/300x200/d5232a/white?text=Fio+Sil+4.0mm+100m",
        "product_url": "#produto-fio-4mm",
    },

    # ─── Pisos & Acabamentos ─────────────────────────────────────────────
    {
        "name": "Porcelanato Esmaltado Elizabeth Polido 60x60cm (Caixa 1.44m²)",
        "description": (
            "Revestimento nobre retificado com brilho espelhado polido para salas, quartos e corredores. "
            "Junta mínima de 1.5mm para paginação uniforme e sofisticada."
        ),
        "category": "Pisos & Acabamentos",
        "brand": "Elizabeth",
        "price": Decimal("89.90"),
        "stock_quantity": 85,
        "image_url": "https://placehold.co/300x200/f5f5f7/black?text=Porcelanato+60x60+Elizabeth",
        "product_url": "#produto-porcelanato-elizabeth",
    },
    {
        "name": "Telha Cerâmica Romana Resinada Vermelha (Unidade)",
        "description": (
            "Telha romana tradicional com acabamento resinado que repele água e fungos. "
            "Encaixe perfeito contra infiltrações. Consumo médio: 16 telhas por m² de telhado."
        ),
        "category": "Pisos & Acabamentos",
        "brand": "Cerâmica Paulistinha",
        "price": Decimal("3.20"),
        "stock_quantity": 2400,
        "image_url": "https://placehold.co/300x200/a4181e/white?text=Telha+Romana+Resinada",
        "product_url": "#produto-telha-romana",
    },

    # ─── Ferramentas & Equipamentos ──────────────────────────────────────
    {
        "name": "Carrinho de Mão Caçamba Metálica 65 Litros Reforçado Tramontina",
        "description": (
            "Chassi de aço reforçado com pneu e câmara de alta tração. Perfeito para transporte "
            "de terra, areia, cimento e entulho em canteiros de obra."
        ),
        "category": "Ferramentas",
        "brand": "Tramontina",
        "price": Decimal("259.00"),
        "stock_quantity": 20,
        "image_url": "https://placehold.co/300x200/d5232a/white?text=Carrinho+Mao+Tramontina",
        "product_url": "#produto-carrinho-tramontina",
    },
    {
        "name": "Furadeira e Parafusadeira de Impacto Bosch GSB 550W 1/2\" com Maleta",
        "description": (
            "Motor de 550W com função de impacto para perfurar alvenaria, concreto, metal e madeira. "
            "Acompanha maleta plástica e kit de brocas essenciais."
        ),
        "category": "Ferramentas",
        "brand": "Bosch",
        "price": Decimal("329.00"),
        "stock_quantity": 18,
        "image_url": "https://placehold.co/300x200/1d1d1f/white?text=Furadeira+Bosch+550W",
        "product_url": "#produto-furadeira-bosch",
    },
    {
        "name": "Colher de Pedreiro Canto Redondo 8\" Tramontina",
        "description": (
            "Lâmina forjada em aço carbono especial com cabo de madeira envernizado. "
            "Equilíbrio ideal e durabilidade extrema para aplicação de argamassa e reboco."
        ),
        "category": "Ferramentas",
        "brand": "Tramontina",
        "price": Decimal("34.90"),
        "stock_quantity": 60,
        "image_url": "https://placehold.co/300x200/86868b/white?text=Colher+Pedreiro+Tramontina",
        "product_url": "#produto-colher-pedreiro",
    },
]


async def seed():
    """Popula os materiais de construção no MongoDB."""
    print("🚀 Conectando ao MongoDB Atlas...")
    client = get_motor_client()
    await init_db(client)

    count = await Product.count()
    if count > 0:
        print(f"🗑️  Removendo {count} produtos antigos de teste...")
        await Product.delete_all()

    print(f"📦 Inserindo {len(MATERIAIS_CONSTRUCAO)} materiais de construção reais no catálogo...")
    for dados in MATERIAIS_CONSTRUCAO:
        p = Product(**dados)
        await p.insert()

    print(f"✅ {len(MATERIAIS_CONSTRUCAO)} materiais cadastrados com sucesso!")
    categorias = set(p["category"] for p in MATERIAIS_CONSTRUCAO)
    for cat in sorted(categorias):
        qtd = sum(1 for p in MATERIAIS_CONSTRUCAO if p["category"] == cat)
        print(f"  • {cat}: {qtd} produto(s)")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())

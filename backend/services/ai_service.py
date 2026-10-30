"""
ai_service.py — Assistente Virtual Especialista em Materiais de Construção (Nikkei).
A IA "Nini" orienta clientes sobre obras, reformas, produtos de construção e orçamentos.
"""
import json
from decimal import Decimal
from typing import List, Optional

from groq import AsyncGroq

from config import settings
from services.product_service import search_products
from schemas import ProductCard

# ─── Cliente Groq ─────────────────────────────────────────────────────────────
_groq_client = AsyncGroq(api_key=settings.groq_api_key)

# ─── Prompt de sistema especializado em Construção Civil ─────────────────────
SYSTEM_PROMPT = """Você é a Nini, consultora técnica e vendedora virtual da loja Nikkei Materiais de Construção.
Sua missão é atender clientes, mestres de obras, pedreiros, arquitetos e pessoas reformando ou construindo,
oferecendo orientação técnica precisa e recomendando materiais reais do catálogo da loja.

CONHECIMENTO TÉCNICO & ESPECIALIDADE:
- Fases da obra: Fundação, alvenaria, cobertura/telhado, hidráulica, elétrica, impermeabilização, pisos/revestimentos e pintura.
- Tipos de cimento (CP II, CP III, CP IV, CP V) e argamassas (AC-I para áreas internas, AC-II para externas, AC-III para porcelanatos e piscinas).
- Tintas e acabamentos (acrílica fosca/acetinada para paredes, esmalte para madeiras/metais, impermeabilizantes para lajes, baldrames e umidade).
- Hidráulica (tubos soldáveis de água fria/quente, esgoto) e Elétrica (bitolas de fios 1.5mm², 2.5mm², 4mm², disjuntores).
- Cálculos práticos de consumo de materiais (ex: quantidade de sacos de cimento, rendimento de latas de tinta por m², etc.).

REGRAS DE CONDUTA:
1. Responda em português brasileiro, com tom amigável, acolhedor e profissional.
2. NUNCA invente produtos, marcas, preços ou estoques que não estejam no catálogo retornado pela busca.
3. SEMPRE use a ferramenta `search_products` quando o cliente perguntar sobre materiais, cimento, tintas, tubos, ferramentas, pisos, etc.
4. Quando recomendar produtos, explique brevemente o PORQUÊ técnico da indicação (ex: 'Para porcelanato em área externa, a argamassa AC-III é a mais indicada devido à aderência reforçada').
5. Incentive o cliente a adicionar os itens recomendados ao orçamento clicando no botão '+ Orçamento' no card de cada produto.
6. Informe sobre vantagens: frete grátis em compras elegíveis e desconto de 10% para compras acima de R$ 500,00.
7. Se o cliente tiver uma necessidade complexa, faça perguntas para entender a metragem (m²), se é área interna ou externa, e o tipo de superfície."""

# ─── Ferramentas disponíveis para a IA ───────────────────────────────────────
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": (
                "Busca materiais de construção no catálogo real da Nikkei. "
                "Use esta função sempre que o cliente procurar por cimento, argamassa, tintas, "
                "impermeabilizantes, tubos, fios, ferramentas, pisos, telhas, blocos, etc."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Termo de busca (ex: cimento 50kg, tinta acrílica externa, argamassa AC3, tubo 100mm, fio 2.5mm)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Categoria (ex: Básico & Alvenaria, Pintura & Impermeabilização, Hidráulica & Elétrica, Pisos & Acabamentos, Ferramentas)"
                    },
                    "min_price": {
                        "type": "number",
                        "description": "Preço mínimo em reais"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Preço máximo em reais (orçamento do cliente)"
                    },
                    "brand": {
                        "type": "string",
                        "description": "Marca (ex: Votoran, Suvinil, Tigre, Vedacit, Bosch, Tramontina, Fortlev)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Quantidade máxima de resultados (padrão: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    }
]


async def _execute_tool_call(
    tool_name: str,
    tool_args: dict
) -> tuple[str, List[ProductCard]]:
    """Executa a busca de materiais no MongoDB."""
    if tool_name == "search_products":
        products = await search_products(
            q=tool_args.get("query"),
            category=tool_args.get("category"),
            min_price=Decimal(str(tool_args["min_price"])) if tool_args.get("min_price") else None,
            max_price=Decimal(str(tool_args["max_price"])) if tool_args.get("max_price") else None,
            brand=tool_args.get("brand"),
            limit=min(tool_args.get("limit", 5), settings.max_products_per_response),
        )

        if not products:
            return "Nenhum produto encontrado com esses critérios no catálogo.", []

        result_text = f"Encontrei {len(products)} produto(s) no estoque da loja:\n"
        for p in products:
            status = f"Em estoque ({p.stock_quantity} un)" if p.in_stock else "Esgotado no momento"
            result_text += (
                f"- ID {p.id}: {p.name} | Marca: {p.brand} | "
                f"R$ {p.price:.2f} | {status} | Descrição: {p.description}\n"
            )
        return result_text, products

    return "Ferramenta não reconhecida.", []


async def process_message(
    session_id: str,
    user_message: str,
    history: List[dict],
) -> tuple[str, List[ProductCard]]:
    """
    Processa a mensagem do cliente com o modelo da Groq.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-settings.max_history_messages:])
    messages.append({"role": "user", "content": user_message})

    found_products: List[ProductCard] = []

    response = await _groq_client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.6,
        max_tokens=1024,
    )

    choice = response.choices[0]

    if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
        tool_results_messages = list(messages)
        tool_results_messages.append(choice.message)

        for tool_call in choice.message.tool_calls:
            try:
                args = json.loads(tool_call.function.arguments)
                tool_result, products = await _execute_tool_call(
                    tool_call.function.name, args
                )
                found_products.extend(products)
            except Exception as e:
                tool_result = f"Erro ao consultar catálogo de construção: {str(e)}"

            tool_results_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result,
            })

        final_response = await _groq_client.chat.completions.create(
            model=settings.groq_model,
            messages=tool_results_messages,
            temperature=0.6,
            max_tokens=1024,
        )
        ai_text = final_response.choices[0].message.content or ""
    else:
        ai_text = choice.message.content or ""

    seen_ids = set()
    unique_products = []
    for p in found_products:
        if p.id not in seen_ids:
            seen_ids.add(p.id)
            unique_products.append(p)

    return ai_text.strip(), unique_products[:settings.max_products_per_response]

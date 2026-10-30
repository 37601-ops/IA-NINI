# 🏗️ Nikkei Materiais de Construção — IA Especialista em Obras e Reformas

Assistente virtual inteligente (Nini) com IA generativa integrada ao catálogo real de materiais de construção,
base de dados no MongoDB Atlas e calculadora de orçamento para obras em tempo real.

## 🛠️ Especialidades da IA Nini

- **Fases da Obra:** Fundação, alvenaria, cobertura, hidráulica, elétrica, impermeabilização, revestimentos e pintura.
- **Consultoria Técnica:**
  - Indicação do cimento correto (CP II para uso geral vs CP V-ARI para estruturas pesadas).
  - Tipos de argamassa (AC-I interna, AC-II externa e AC-III para porcelanatos e piscinas).
  - Tintas para áreas externas resistentes a intempéries e umidade (Coral Sol & Chuva, Suvinil Rende Muito).
  - Impermeabilizantes (Vedacit, Neutrol) para alicerces, baldrames e caixas d'água.
- **Calculadora Integrada:** Adição de produtos ao orçamento, cálculo de frete e desconto automático de 10% para pedidos acima de R$ 500,00.

---

## 🚀 Como Executar

### 1. No ambiente local:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py
uvicorn main:app --reload
```

### 2. Deploy na Vercel:
O projeto já conta com `vercel.json` e `api/index.py` prontos. Suba para o GitHub e importe na Vercel com as variáveis:
- `GROQ_API_KEY`
- `MONGODB_URL`
- `MONGODB_DB_NAME`
- `SECRET_KEY`
- `GROQ_MODEL=qwen/qwen3.8-27b`

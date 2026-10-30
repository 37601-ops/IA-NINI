/*
==============================================================================
FRONTEND DESATIVADO (MANTIDO EM COMENTÁRIO)
==============================================================================

/**
 * budget.js — Calculadora de orçamento integrada ao chat
 * Gerencia adição/remoção de itens e exibe totais validados pelo servidor.
 * /

// ── Elementos do DOM ────────────────────────────────────────────────────────
const budgetItemsList = document.getElementById('budget-items-list');
const budgetEmpty     = document.getElementById('budget-empty');
const budgetFooter    = document.getElementById('budget-footer');
const budgetCountBadge = document.getElementById('budget-count-badge');

// ── Estado ───────────────────────────────────────────────────────────────────
let isBudgetLoading = false;

// ── Adicionar ao orçamento ───────────────────────────────────────────────────
async function addToBudget(productId, productName) {
  if (isBudgetLoading) return;
  isBudgetLoading = true;

  const sessionId = window.getSessionId();
  try {
    const res = await fetch(`${window.API_BASE}/budget/${sessionId}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId, quantity: 1 }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Erro ao adicionar ao orçamento.');
    }

    const budget = await res.json();
    updateBudgetUI(budget);
    updateBudgetBadge(budget.items.length);

    window.showToast(`✅ "${productName}" adicionado ao orçamento!`);

    // Muda para a aba de orçamento automaticamente
    window.switchTab('orcamento');

  } catch (error) {
    window.showToast(`❌ ${error.message}`);
  } finally {
    isBudgetLoading = false;
  }
}

// ── Atualizar quantidade de item ─────────────────────────────────────────────
async function updateItemQty(itemId, newQty) {
  if (isBudgetLoading || newQty < 1) return;
  isBudgetLoading = true;

  const sessionId = window.getSessionId();
  try {
    const res = await fetch(`${window.API_BASE}/budget/${sessionId}/item/${itemId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quantity: newQty }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Erro ao atualizar quantidade.');
    }

    const budget = await res.json();
    updateBudgetUI(budget);
    updateBudgetBadge(budget.items.length);

  } catch (error) {
    window.showToast(`❌ ${error.message}`);
  } finally {
    isBudgetLoading = false;
  }
}

// ── Remover item ─────────────────────────────────────────────────────────────
async function removeItem(itemId) {
  if (isBudgetLoading) return;
  isBudgetLoading = true;

  const sessionId = window.getSessionId();
  try {
    const res = await fetch(`${window.API_BASE}/budget/${sessionId}/item/${itemId}`, {
      method: 'DELETE',
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Erro ao remover item.');
    }

    const budget = await res.json();
    updateBudgetUI(budget);
    updateBudgetBadge(budget.items.length);
    window.showToast('🗑️ Item removido do orçamento.');

  } catch (error) {
    window.showToast(`❌ ${error.message}`);
  } finally {
    isBudgetLoading = false;
  }
}

// ── Limpar orçamento ─────────────────────────────────────────────────────────
async function clearBudget() {
  if (!confirm('Deseja limpar todos os itens do orçamento?')) return;
  if (isBudgetLoading) return;
  isBudgetLoading = true;

  const sessionId = window.getSessionId();
  try {
    await fetch(`${window.API_BASE}/budget/${sessionId}`, { method: 'DELETE' });
    clearBudgetUI();
    window.showToast('🗑️ Orçamento limpo.');
  } catch {
    window.showToast('❌ Erro ao limpar o orçamento.');
  } finally {
    isBudgetLoading = false;
  }
}

// ── Carregar orçamento (ao abrir aba) ────────────────────────────────────────
async function renderBudget() {
  const sessionId = window.getSessionId();
  try {
    const res = await fetch(`${window.API_BASE}/budget/${sessionId}`);
    if (!res.ok) return;
    const budget = await res.json();
    updateBudgetUI(budget);
    updateBudgetBadge(budget.items.length);
  } catch {}
}

// ── Atualizar interface do orçamento ─────────────────────────────────────────
function updateBudgetUI(budget) {
  if (!budget.items || budget.items.length === 0) {
    clearBudgetUI();
    return;
  }

  budgetEmpty.style.display = 'none';
  budgetItemsList.style.display = 'flex';
  budgetFooter.style.display = 'block';

  // Renderiza os itens
  budgetItemsList.innerHTML = '';
  budget.items.forEach(item => {
    const div = document.createElement('div');
    div.className = 'budget-item';
    div.innerHTML = `
      <img class="budget-item-img"
           src="${item.product.image_url || 'https://placehold.co/50x50?text=?'}"
           alt="${escapeHtml(item.product.name)}"
           onerror="this.src='https://placehold.co/50x50?text=?'">
      <div class="budget-item-info">
        <div class="budget-item-name" title="${escapeHtml(item.product.name)}">
          ${escapeHtml(item.product.name)}
        </div>
        <div class="budget-item-price">
          ${window.formatCurrency(item.unit_price)} / un.
        </div>
        <div class="budget-item-subtotal">
          ${window.formatCurrency(item.subtotal)}
        </div>
      </div>
      <div class="qty-controls">
        <button class="qty-btn" onclick="updateItemQty('${item.id}', ${item.quantity - 1})"
                ${item.quantity <= 1 ? 'disabled style="opacity:0.4"' : ''}>−</button>
        <span class="qty-value">${item.quantity}</span>
        <button class="qty-btn" onclick="updateItemQty('${item.id}', ${item.quantity + 1})">+</button>
      </div>
      <button class="budget-remove-btn" onclick="removeItem('${item.id}')" title="Remover">🗑️</button>
    `;
    budgetItemsList.appendChild(div);
  });

  // Rodapé com totais
  const descontoHtml = parseFloat(budget.discount_total) > 0 ? `
    <div class="budget-line">
      <span>Subtotal bruto</span>
      <span class="valor">${window.formatCurrency(budget.subtotal)}</span>
    </div>
    ${budget.discount_info ? `<div class="budget-discount-info">🏷️ ${escapeHtml(budget.discount_info)}</div>` : ''}
    <div class="budget-line budget-desconto">
      <span>Desconto</span>
      <span class="valor">−${window.formatCurrency(budget.discount_total)}</span>
    </div>
  ` : `
    <div class="budget-line">
      <span>Subtotal</span>
      <span class="valor">${window.formatCurrency(budget.subtotal)}</span>
    </div>
  `;

  const freteHtml = `
    ${budget.shipping_info ? `<div class="budget-shipping-info">🚚 ${escapeHtml(budget.shipping_info)}</div>` : ''}
    <div class="budget-line">
      <span>Frete</span>
      <span class="valor">${parseFloat(budget.shipping) === 0 ? '🎉 Grátis' : window.formatCurrency(budget.shipping)}</span>
    </div>
  `;

  budgetFooter.innerHTML = `
    ${descontoHtml}
    ${freteHtml}
    <div class="budget-line total">
      <span>Total</span>
      <span class="valor">${window.formatCurrency(budget.grand_total)}</span>
    </div>
    ${budget.is_estimate ? '<div class="budget-estimativa">⚠️ Valores estimados. Frete confirma-se no checkout.</div>' : ''}
    <div class="budget-actions">
      <button class="btn-limpar-orcamento" onclick="clearBudget()">🗑️ Limpar</button>
      <button class="btn-ir-produtos" onclick="irParaProdutos()">🛒 Ir para produtos</button>
    </div>
  `;
}

// ── Limpar UI do orçamento ────────────────────────────────────────────────────
function clearBudgetUI() {
  budgetEmpty.style.display = 'flex';
  budgetItemsList.style.display = 'none';
  budgetItemsList.innerHTML = '';
  if (budgetFooter) budgetFooter.innerHTML = '';
  budgetFooter.style.display = 'none';
  updateBudgetBadge(0);
}

// ── Badge de contagem ────────────────────────────────────────────────────────
function updateBudgetBadge(count) {
  if (!budgetCountBadge) return;
  budgetCountBadge.textContent = count;
  budgetCountBadge.classList.toggle('visible', count > 0);
}

// ── Ir para produtos ─────────────────────────────────────────────────────────
function irParaProdutos() {
  const container = document.getElementById('products-grid') || document.getElementById('produtos-destaque');
  container?.scrollIntoView({ behavior: 'smooth' });
  if (typeof window.fecharChat === 'function') {
    window.fecharChat();
  }
}

// ── Helper ───────────────────────────────────────────────────────────────────
function escapeHtml(str) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(str || ''));
  return div.innerHTML;
}

// ── Exportações globais ──────────────────────────────────────────────────────
window.addToBudget     = addToBudget;
window.updateItemQty   = updateItemQty;
window.removeItem      = removeItem;
window.clearBudget     = clearBudget;
window.renderBudget    = renderBudget;
window.clearBudgetUI   = clearBudgetUI;
window.irParaProdutos  = irParaProdutos;


*/

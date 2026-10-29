/**
 * chat.js — Lógica do chat com a IA Nini
 * Gerencia sessão, envia mensagens, renderiza respostas e cards de produto.
 */

const API_BASE = 'http://127.0.0.1:8000/api';

// ── Estado global ───────────────────────────────────────────────────────────
let sessionId = null;
let isLoading = false;

// ── Elementos do DOM ────────────────────────────────────────────────────────
const chatWindow    = document.getElementById('chat-window');
const chatMessages  = document.getElementById('chat-messages');
const chatInput     = document.getElementById('chat-input');
const sendBtn       = document.getElementById('send-btn');
const typingIndicator = document.getElementById('typing-indicator');
const chatFab       = document.getElementById('chat-fab');
const tabChat       = document.getElementById('tab-chat');
const tabOrcamento  = document.getElementById('tab-orcamento');
const chatPanel     = document.getElementById('chat-panel');
const budgetPanel   = document.getElementById('budget-panel');
const toast         = document.getElementById('toast');

// ── Inicialização ───────────────────────────────────────────────────────────
function init() {
  // Recupera ou cria session_id
  sessionId = localStorage.getItem('nini_session_id');
  if (!sessionId || sessionId.length !== 36) {
    sessionId = generateUUID();
    localStorage.setItem('nini_session_id', sessionId);
  }

  // Carrega histórico da sessão
  loadHistory();

  // Event listeners
  sendBtn.addEventListener('click', handleSend);
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  });
  chatInput.addEventListener('input', autoResizeTextarea);
}

// ── Abrir / fechar chat ─────────────────────────────────────────────────────
function toggleChat() {
  chatWindow.classList.toggle('aberto');
  if (chatWindow.classList.contains('aberto')) {
    chatInput.focus();
    scrollToBottom();
  }
}

function fecharChat() {
  chatWindow.classList.remove('aberto');
}

// ── Tabs (Chat / Orçamento) ─────────────────────────────────────────────────
function switchTab(tab) {
  if (tab === 'chat') {
    tabChat.classList.add('ativo');
    tabOrcamento.classList.remove('ativo');
    chatPanel.style.display = 'flex';
    chatPanel.style.flexDirection = 'column';
    budgetPanel.classList.remove('ativo');
    scrollToBottom();
  } else {
    tabOrcamento.classList.add('ativo');
    tabChat.classList.remove('ativo');
    chatPanel.style.display = 'none';
    budgetPanel.classList.add('ativo');
    window.renderBudget && window.renderBudget();
  }
}

// ── Enviar mensagem ─────────────────────────────────────────────────────────
async function handleSend() {
  const text = chatInput.value.trim();
  if (!text || isLoading) return;

  appendMessage('usuario', text);
  chatInput.value = '';
  autoResizeTextarea();
  showTyping(true);
  setLoading(true);

  try {
    const res = await fetch(`${API_BASE}/chat/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message: text }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Erro ${res.status}`);
    }

    const data = await res.json();
    showTyping(false);
    appendMessage('bot', data.response, data.products || []);

  } catch (error) {
    showTyping(false);
    const isConnectionError = error.message.includes('Failed to fetch') || error.message.includes('NetworkError');
    appendMessage('bot',
      isConnectionError
        ? '❌ Não consegui me conectar ao servidor. Verifique se o backend está rodando e tente novamente.'
        : `❌ Ocorreu um erro: ${error.message}`
    );
  } finally {
    setLoading(false);
  }
}

// ── Renderização de mensagens ────────────────────────────────────────────────
function appendMessage(role, text, products = []) {
  const wrapper = document.createElement('div');
  wrapper.className = `msg-wrapper ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = role === 'bot' ? '🤖' : '👤';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';

  // Texto da mensagem (preserva quebras de linha)
  const textNode = document.createElement('div');
  textNode.innerHTML = formatMessage(text);
  bubble.appendChild(textNode);

  // Horário
  const time = document.createElement('div');
  time.className = 'msg-time';
  time.textContent = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  bubble.appendChild(time);

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  chatMessages.appendChild(wrapper);

  // Cards de produtos (se houver)
  if (products && products.length > 0) {
    const carousel = renderProductCards(products);
    const carouselWrapper = document.createElement('div');
    carouselWrapper.className = 'msg-wrapper bot';
    const carouselBubble = document.createElement('div');
    carouselBubble.style.maxWidth = '100%';
    carouselBubble.appendChild(carousel);
    carouselWrapper.appendChild(carouselBubble);
    chatMessages.appendChild(carouselWrapper);
  }

  scrollToBottom();
}

function formatMessage(text) {
  // Escapa HTML básico e formata markdown simples
  return text
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}

// ── Cards de produto ─────────────────────────────────────────────────────────
function renderProductCards(products) {
  const carousel = document.createElement('div');
  carousel.className = 'products-carousel';

  products.forEach(product => {
    const card = document.createElement('div');
    card.className = 'product-chat-card';

    const inStock = product.in_stock !== false && product.stock_quantity > 0;
    const precoFormatado = formatCurrency(product.price);

    card.innerHTML = `
      <img src="${product.image_url || 'https://placehold.co/300x200?text=Produto'}"
           alt="${escapeHtml(product.name)}"
           onerror="this.src='https://placehold.co/300x200?text=Sem+Imagem'">
      <div class="product-chat-card-body">
        <div class="product-chat-card-name">${escapeHtml(product.name)}</div>
        <div class="product-chat-card-brand">${escapeHtml(product.brand)}</div>
        <div class="product-chat-card-price">${precoFormatado}</div>
        <div class="product-chat-card-stock ${inStock ? '' : 'sem-estoque'}">
          ${inStock ? '✅ Em estoque' : '❌ Fora de estoque'}
        </div>
        <div class="product-chat-card-btns">
          <button class="btn-ver-produto" onclick="window.open('${product.product_url || '#'}', '_blank')">
            Ver produto
          </button>
          <button class="btn-add-orcamento"
                  onclick="window.addToBudget('${product.id}', '${escapeHtml(product.name)}')"
                  ${inStock ? '' : 'disabled'}>
            + Orçamento
          </button>
        </div>
      </div>
    `;
    carousel.appendChild(card);
  });

  return carousel;
}

// ── Carregar histórico ───────────────────────────────────────────────────────
async function loadHistory() {
  try {
    const res = await fetch(`${API_BASE}/chat/history/${sessionId}`);
    if (!res.ok) return;

    const data = await res.json();
    if (data.messages && data.messages.length > 0) {
      data.messages.forEach(msg => {
        appendMessage(msg.role === 'user' ? 'usuario' : 'bot', msg.content);
      });
    } else {
      // Mensagem de boas-vindas
      appendMessage('bot',
        '👋 Olá! Sou a **Nini**, sua assistente virtual de compras!\n\n' +
        'Posso ajudar você a encontrar produtos do nosso catálogo, comparar opções ' +
        'e montar um orçamento completo.\n\nComo posso te ajudar hoje?'
      );
    }
  } catch {
    appendMessage('bot',
      '👋 Olá! Sou a **Nini**, sua assistente virtual!\n\nComo posso te ajudar hoje?'
    );
  }
}

// ── Nova conversa ────────────────────────────────────────────────────────────
async function novaConversa() {
  if (!confirm('Deseja iniciar uma nova conversa? O histórico atual será apagado.')) return;

  try {
    await fetch(`${API_BASE}/chat/session/${sessionId}`, { method: 'DELETE' });
  } catch {}

  sessionId = generateUUID();
  localStorage.setItem('nini_session_id', sessionId);
  chatMessages.innerHTML = '';
  appendMessage('bot',
    '✨ Nova conversa iniciada! Como posso te ajudar hoje?'
  );

  // Limpa o orçamento na UI
  window.clearBudgetUI && window.clearBudgetUI();
}

// ── Helpers ──────────────────────────────────────────────────────────────────
function setLoading(state) {
  isLoading = state;
  sendBtn.disabled = state;
  chatInput.disabled = state;
}

function showTyping(show) {
  typingIndicator.classList.toggle('visivel', show);
  if (show) scrollToBottom();
}

function scrollToBottom() {
  setTimeout(() => {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }, 50);
}

function autoResizeTextarea() {
  chatInput.style.height = 'auto';
  chatInput.style.height = Math.min(chatInput.scrollHeight, 100) + 'px';
}

function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(str || ''));
  return div.innerHTML;
}

function showToast(message, duration = 3000) {
  toast.textContent = message;
  toast.classList.add('visivel');
  setTimeout(() => toast.classList.remove('visivel'), duration);
}

// ── Exportações globais ──────────────────────────────────────────────────────
window.toggleChat    = toggleChat;
window.fecharChat    = fecharChat;
window.switchTab     = switchTab;
window.novaConversa  = novaConversa;
window.showToast     = showToast;
window.formatCurrency = formatCurrency;
window.API_BASE      = API_BASE;
window.getSessionId  = () => sessionId;

// ── Inicia ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', init);

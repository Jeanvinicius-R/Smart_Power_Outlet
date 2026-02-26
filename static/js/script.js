// ===== TEMA =====
function toggleTheme() {
    var html = document.documentElement;
    var atual = html.getAttribute('data-theme');
    var novo = atual === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', novo);
    document.getElementById('theme-icon').textContent = novo === 'dark' ? '☀' : '☾';
    localStorage.setItem('tema', novo);
}

// Carrega tema salvo
(function() {
    var temaSalvo = localStorage.getItem('tema') || 'dark';
    document.documentElement.setAttribute('data-theme', temaSalvo);
    var icone = document.getElementById('theme-icon');
    if (icone) icone.textContent = temaSalvo === 'dark' ? '☀' : '☾';
})();

// ===== STATUS =====
setInterval(atualizarStatus, 5000);
atualizarStatus();

function atualizarStatus() {
    fetch('/api/status')
        .then(function(response) { return response.json(); })
        .then(function(data) {
            var textoStatus = document.getElementById('status-texto');
            var ring = document.getElementById('power-ring');

            if (data.ligada) {
                textoStatus.textContent = 'Ligada';
                textoStatus.className = 'status-value ligada';
                ring.className = 'power-ring ligada';
            } else {
                textoStatus.textContent = 'Desligada';
                textoStatus.className = 'status-value desligada';
                ring.className = 'power-ring desligada';
            }

            document.getElementById('watts').textContent   = data.watts;
            document.getElementById('volts').textContent   = data.volts;
            document.getElementById('amperes').textContent = data.amperes;
        })
        .catch(function(erro) {
            console.log('Erro ao buscar status:', erro);
        });
}

// ===== CONTROLE =====
function ligar() {
    fetch('/api/ligar', { method: 'POST' })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            adicionarHistorico('Tomada ligada', 'on');
            atualizarStatus();
        });
}

function desligar() {
    fetch('/api/desligar', { method: 'POST' })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            adicionarHistorico('Tomada desligada', 'off');
            atualizarStatus();
        });
}

// ===== HISTÓRICO =====
function adicionarHistorico(acao, tipo) {
    var lista = document.getElementById('historico');

    // Remove mensagem vazia se existir
    var vazio = lista.querySelector('.historico-empty');
    if (vazio) lista.removeChild(vazio);

    var item = document.createElement('li');
    var agora = new Date();
    var hora = agora.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    item.innerHTML =
        '<span class="hist-dot ' + tipo + '"></span>' +
        '<span>' + acao + '</span>' +
        '<span class="hist-hora" style="margin-left:auto">' + hora + '</span>';

    lista.insertBefore(item, lista.firstChild);

    if (lista.children.length > 10) {
        lista.removeChild(lista.lastChild);
    }
}
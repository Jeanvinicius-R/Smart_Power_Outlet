# 🔌 Smart Power Outlet — Tomada Inteligente

Interface web para controlar uma tomada inteligente **Tuya** via API, com monitoramento em tempo real de potência, tensão e corrente.

---

## 📋 Pré-requisitos

- Python 3.8+
- pip
- Uma tomada inteligente compatível com a **plataforma Tuya**
- Credenciais de API Tuya (Access Key, Secret Key e Device ID)

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/Smart_Power_Outlet.git
cd Smart_Power_Outlet
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install flask requests
```

---

## 🔑 Configuração das credenciais Tuya

Abra o arquivo `services/tuya_service.py` e preencha com as suas credenciais:

```python
ACCESS_KEY = "sua_access_key_aqui"
SECRET_KEY = "sua_secret_key_aqui"
DEVICE_ID  = "seu_device_id_aqui"
BASE_URL   = "https://openapi.tuyaus.com"  # Altere a região se necessário
```

> **Onde encontrar essas informações?**
> Acesse o [Tuya IoT Platform](https://iot.tuya.com), crie um projeto Cloud, vincule o seu dispositivo e copie as credenciais geradas.

> **Região da API:** Se o seu dispositivo estiver registrado em outra região, altere o `BASE_URL`:
> - EUA: `https://openapi.tuyaus.com`
> - Europa: `https://openapi.tuyaeu.com`
> - China: `https://openapi.tuyacn.com`

---

## ▶️ Executando o app

```bash
python app.py
```

O servidor Flask irá iniciar em modo debug. Acesse no navegador:

```
http://localhost:5000
```

---

## 🖥️ Como usar a interface

### Status da tomada
Ao abrir o app, o status é carregado automaticamente e **atualizado a cada 5 segundos**. O anel central muda de cor:
- 🟢 **Verde** → Tomada ligada
- 🔴 **Vermelho** → Tomada desligada

### Ligar e Desligar
Use os botões **Ligar** e **Desligar** para controlar a tomada remotamente.

### Métricas em tempo real
A tela exibe três métricas da tomada:
| Métrica | Descrição |
|---------|-----------|
| **W** (Watts) | Potência consumida |
| **V** (Volts) | Tensão da rede |
| **A** (Amperes) | Corrente elétrica |

### Histórico de ações
Cada vez que você liga ou desliga a tomada, o evento é registrado no painel de **Histórico** com o horário exato. Os últimos 10 eventos são mantidos.

### Tema claro/escuro
Clique no botão ☀/☾ no canto superior direito para alternar entre os temas. A preferência é salva automaticamente no navegador.

---

## 📡 Endpoints da API

Você também pode controlar a tomada diretamente via requisições HTTP:

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/status` | Retorna status e métricas da tomada |
| `POST` | `/api/ligar` | Liga a tomada |
| `POST` | `/api/desligar` | Desliga a tomada |

**Exemplo com curl:**

```bash
# Verificar status
curl http://localhost:5000/api/status

# Ligar
curl -X POST http://localhost:5000/api/ligar

# Desligar
curl -X POST http://localhost:5000/api/desligar
```

**Resposta do `/api/status`:**

```json
{
  "ligada": true,
  "watts": 55.3,
  "volts": 220.1,
  "amperes": 0.251
}
```

---

## 🗂️ Estrutura do projeto

```
Smart_Power_Outlet/
│
├── app.py                  # Servidor Flask e rotas
├── services/
│   ├── __init__.py
│   └── tuya_service.py     # Integração com a API Tuya
├── static/
│   ├── css/
│   │   └── style.css       # Estilos da interface
│   └── js/
│       └── script.js       # Lógica do frontend
└── templates/
    └── index.html          # Página principal
```

---

## ⚠️ Observações

- As credenciais no arquivo `tuya_service.py` ficam expostas no código. Para produção, utilize **variáveis de ambiente**.
- O `debug=True` no `app.py` é adequado apenas para desenvolvimento. Em produção, use um servidor como **Gunicorn**.
- A API Tuya pode ter latência variável dependendo da região configurada.


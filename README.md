# 🚀 LogAllytics – Pipeline de Logs Automático com Interface Gráfica

**Resumo:**  
O *LogAllytics* é um sistema interativo que automatiza o processamento e a análise de logs de vendas. Ele permite aplicar filtros dinâmicos, gerar gráficos informativos e detectar anomalias de forma inteligente, tudo por meio de uma interface gráfica moderna construída com CustomTkinter.

---

## 🎯 Objetivo

Este projeto tem como objetivo principal facilitar a análise de registros de vendas através de um pipeline automatizado com visualização de dados e detecção de comportamentos anômalos. A motivação é oferecer uma solução prática que una fundamentos de banco de dados, ciência de dados, IHM e machine learning, promovendo a aprendizagem aplicada das disciplinas do curso.

---

## 👨‍💻 Tecnologias Utilizadas

- **Python 3.12**
- **CustomTkinter** – Interface moderna com suporte a temas
- **SQLite3** – Banco de dados relacional leve
- **pandas** – Manipulação de dados
- **matplotlib** – Geração de gráficos
- **scikit-learn** – Detecção de anomalias com Isolation Forest
- **regex** – Classificação textual de categorias

---

## 🗂️ Estrutura do Projeto

```
📦 logallytics
├── App.py
├── README.md
├── README_modelo_Mostra.md
├── requirements.txt
├── 📁 assets
├── 📁 data
│   ├── vendas.db
├── 📁 logs
│   └── vendas_10000.log
├── 📁 modules
│   ├── deteccao_anomalia.py
│   ├── filtros.py
│   ├── graficos.py
│   └── processamento.py
├── 📁 ui
│   ├── dashboard.py
│   └── interface_principal.py
```

---

## ⚙️ Como Executar

### ✅ Rodando Localmente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/logallytics.git
cd logallytics
```

2. Crie o ambiente virtual e ative:

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python App.py
```

---

## 📸 Demonstrações

- Interface gráfica principal com filtros dinâmicos
- Gráficos de barra e pizza com total por categoria
- Impressão de anomalias no console
- Carregamento automático de logs para o banco

---

## 👥 Equipe

| Nome              | GitHub                               |
|-------------------|---------------------------------------|
| Cesar [Seu Nome]  | [@seuusuario](https://github.com/seuusuario) |

---

## 🧠 Disciplinas Envolvidas

- Banco de Dados
- Estrutura de Dados
- Engenharia de Software
- Introdução à Inteligência Artificial
- Interface Homem-Máquina (IHM)

---

## 🏫 Informações Acadêmicas

- Universidade: **Universidade Braz Cubas**
- Curso: **Análise e Desenvolvimento de Sistemas**
- Semestre: **4º**
- Período: **Noite**
- Professora orientadora: **Dra. Andréa Ono Sakai**
- Evento: **Mostra de Tecnologia 1º Semestre de 2025**
- Local: **Laboratório 12**
- Datas: **05 e 06 de junho de 2025**

---

## 📄 Licença

MIT License — sinta-se à vontade para utilizar, estudar e adaptar este projeto.
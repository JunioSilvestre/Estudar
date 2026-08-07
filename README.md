# 🚀 Technical Certification & Study Hub (Menu de Estudos DevOps)

<p align="center">
  <img src="https://img.shields.io/badge/Status-Ativo%20%26%20Completo-emerald?style=for-the-badge&logo=github" alt="Status">
  <img src="https://img.shields.io/badge/Módulos-36%20Certificações-blue?style=for-the-badge&logo=devicon" alt="Módulos">
  <img src="https://img.shields.io/badge/Painéis-9%20Famílias%20(Grid%202x2)-purple?style=for-the-badge&logo=docker" alt="Painéis">
  <img src="https://img.shields.io/badge/Multi--SO-macOS%20|%20Windows%20|%20Linux-amber?style=for-the-badge&logo=linux" alt="Multi-SO">
</p>

---

## 📌 Visão Geral

O **Technical Certification & Study Hub** é uma plataforma web interativa, responsiva e completa criada para preparação de exames e estudos focados em **DevOps, Linux, Cloud Computing (Azure & AWS), Containers, Infraestrutura como Código (IaC), Observabilidade e Automação**.

Desenvolvida com **Vanilla HTML5, Tailwind CSS, FontAwesome e JavaScript ES6+**, a plataforma roda direto no navegador sem necessidade de dependências complexas ou servidor backend.

---

## ✨ Recursos & Funcionalidades Principais

* **🎛️ 9 Painéis Simétricos com Grid 2x2 (36 Cards Compactos):** Visual limpo, organizado e responsivo inspirado no protótipo de cards compactos.
* **🎯 Modo de Estudo Focado (`#study-view`):** Ao selecionar qualquer card, o Hub principal é ocultado para dar lugar a uma área de estudos limpa com botão topo `← Voltar ao Hub de Módulos`.
* **🔄 Retomada Automática de Progresso (Auto-Resume):** Salva no `localStorage` a página e questão onde você parou. Ao reabrir o módulo, retoma automaticamente (ex.: *▶️ Continuando da Questão #50*).
* **📖 Leitor de Texto Longo & Guia de Estudo (`material.md`):** Integração com **Marked JS** para renderização de documentações, cheatsheets e resumos técnicos em Markdown.
* **📄 Biblioteca de PDFs por Módulo:** Visualização e download de PDFs oficiais anexados na pasta de cada módulo.
* **🛠️ Gerador & Editor Visual de JSON (`builder.html`):** Ferramenta inclusa para criar, validar e exportar novos simulados e questões de estudo.
* **🇧🇷 / 🇺🇸 Suporte Multilíngue (i18n):** Alternância instantânea entre Português e Inglês.
* **🌗 Modo Escuro / Claro (Dark & Light Mode):** Suporte nativo com alternância manual e detecção de preferências do sistema.
* **🖨️ Estilos Otimizados para Impressão:** Folha de estilos `@media print` para exportar simulados e justificativas em PDF.

---

## 🗺️ Matriz Curricular Completa (9 Painéis × 4 Cards)

```text
               ┌─────────────────────────────────────────────────────────┐
               │    TECHNICAL CERTIFICATION & STUDY HUB (36 CARDS)       │
               └────────────────────────────┬────────────────────────────┘
                                            │
   ┌───────────────────┬────────────────────┼────────────────────┬───────────────────┐
   │                   │                    │                    │                   │
🐧 LPI Essentials   🐧 LPIC-1 Linux       ☁️ Azure Cloud        ☁️ AWS Cloud        🐳 Containers
  ├── 010-160         ├── 101-500           ├── AZ-900           ├── CLF-C02         ├── DCA (Docker)
  ├── 020-100         ├── 102-500           ├── AZ-104           ├── SAA-C03         ├── CKA (K8s)
  ├── 030-100         ├── LP1-DOC           ├── AZ-400           ├── DOP-C02         ├── CKAD (K8s)
  └── 040-100         └── SHELL             └── AZ-DOC           └── AWS-DOC         └── K8S-DOC
   
   ┌───────────────────┬────────────────────┼────────────────────┐
   │                   │                    │                    │
🔀 IaC & CI/CD       📈 Monitoring        🐍 Python DevOps     ⚙️ Scripting & Auto
  ├── 003 (Terraform) ├── GCA (Grafana)     ├── PyDev (DevOps)   ├── BASH (Shell)
  ├── CI-CD (Git)     ├── PCA (Prometheus)  ├── PyAuto (Scripts) ├── PWSH (PowerShell)
  ├── EX294 (Ansible) ├── OTel (Tracing)    ├── PySDK (boto3)    ├── PY-CLI (Python CLI)
  └── IaC-DOC         └── MON-DOC           └── PY-DOC           └── AUTO-DOC
```

### 📋 Detalhamento dos Módulos

| # | Painel / Família | Módulo / Exame | Código | Tag | Ícone | Cor Accent |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **01** | 🐧 **LPI Essentials** | Linux Essentials | `010-160` | `LPI` | `fa-brands fa-linux` | `#f0ad4e` |
| **01b**| 🐧 **LPI Essentials** | Security Essentials | `020-100` | `LPI` | `fa-solid fa-shield-halved` | `#f87171` |
| **01c**| 🐧 **LPI Essentials** | Web Development Essentials | `030-100` | `LPI` | `fa-solid fa-code` | `#38bdf8` |
| **01d**| 🐧 **LPI Essentials** | Open Source Essentials | `040-100` | `LPI` | `fa-solid fa-code-branch` | `#4ade80` |
| **02** | 🐧 **LPIC-1 Linux** | LPIC-1 Exam 101 | `101-500` | `LPI` | `fa-solid fa-terminal` | `#10b981` |
| **03** | 🐧 **LPIC-1 Linux** | LPIC-1 Exam 102 | `102-500` | `LPI` | `fa-solid fa-server` | `#059669` |
| **02c**| 🐧 **LPIC-1 Linux** | Material & Guia LPIC-1 | `LP1-DOC` | `LPI` | `fa-solid fa-book` | `#34d399` |
| **02d**| 🐧 **LPIC-1 Linux** | Shell Scripting & Prática | `SHELL` | `LPI` | `fa-solid fa-square-terminal` | `#6ee7b7` |
| **04** | ☁️ **Azure Cloud** | Azure Fundamentals | `AZ-900` | `AZURE` | `fa-solid fa-cloud` | `#38bdf8` |
| **05** | ☁️ **Azure Cloud** | Azure Administrator | `AZ-104` | `AZURE` | `fa-solid fa-user-gear` | `#2563eb` |
| **13** | ☁️ **Azure Cloud** | DevOps Engineer Expert | `AZ-400` | `AZURE` | `fa-solid fa-diagram-project` | `#1d4ed8` |
| **05d**| ☁️ **Azure Cloud** | Material & Cheatsheet Azure | `AZ-DOC` | `AZURE` | `fa-solid fa-book-bookmark` | `#60a5fa` |
| **06** | ☁️ **AWS Cloud** | Cloud Practitioner | `CLF-C02` | `AWS` | `fa-solid fa-cloud-bolt` | `#fbbf24` |
| **07** | ☁️ **AWS Cloud** | Solutions Architect | `SAA-C03` | `AWS` | `fa-solid fa-sitemap` | `#f59e0b` |
| **14** | ☁️ **AWS Cloud** | DevOps Engineer Professional | `DOP-C02` | `AWS` | `fa-solid fa-infinity` | `#d97706` |
| **07d**| ☁️ **AWS Cloud** | Material & Well-Architected | `AWS-DOC` | `AWS` | `fa-solid fa-book-atlas` | `#fcd34d` |
| **08** | 🐳 **Containers & K8s** | Docker Certified Associate | `DCA` | `DOCKER` | `fa-brands fa-docker` | `#0db7ed` |
| **09** | 🐳 **Containers & K8s** | Kubernetes Administrator | `CKA` | `CNCF` | `fa-solid fa-dharmachakra` | `#326ce5` |
| **09b**| 🐳 **Containers & K8s** | Kubernetes Application Dev | `CKAD` | `CNCF` | `fa-solid fa-cube` | `#60a5fa` |
| **09c**| 🐳 **Containers & K8s** | Material & Guia Containers | `K8S-DOC` | `CNCF` | `fa-solid fa-box-archive` | `#93c5fd` |
| **10** | 🔀 **IaC & CI/CD** | Terraform Associate | `003` | `HASHICORP`| `fa-solid fa-cubes` | `#a855f7` |
| **11** | 🔀 **IaC & CI/CD** | GitHub Actions / GitLab CI | `CI-CD` | `CI/CD` | `fa-brands fa-github` | `#6366f1` |
| **10b**| 🔀 **IaC & CI/CD** | Ansible Specialist | `EX294` | `REDHAT` | `fa-solid fa-gears` | `#ec4899` |
| **11c**| 🔀 **IaC & CI/CD** | Material & Guia IaC/CI-CD | `IaC-DOC` | `DEVOPS` | `fa-solid fa-file-code` | `#c084fc` |
| **12** | 📈 **Monitoring** | Grafana Associate | `GCA` | `GRAFANA` | `fa-solid fa-chart-pie` | `#f97316` |
| **12b**| 📈 **Monitoring** | Prometheus Associate | `PCA` | `PROMETHEUS`| `fa-solid fa-fire` | `#ef4444` |
| **12c**| 📈 **Monitoring** | OpenTelemetry Observability | `OTel` | `OTEL` | `fa-solid fa-eye` | `#fb923c` |
| **12d**| 📈 **Monitoring** | Material & Guia Observab. | `MON-DOC` | `MONITOR` | `fa-solid fa-chart-simple` | `#fdba74` |
| **15** | 🐍 **Python DevOps** | Python for DevOps | `PyDev` | `PYTHON` | `fa-brands fa-python` | `#38bdf8` |
| **15b**| 🐍 **Python DevOps** | Python Automation & Scripts | `PyAuto` | `PYTHON` | `fa-solid fa-robot` | `#34d399` |
| **15c**| 🐍 **Python DevOps** | Python Cloud SDK (boto3) | `PySDK` | `PYTHON` | `fa-solid fa-cloud-arrow-up` | `#a78bfa` |
| **15d**| 🐍 **Python DevOps** | Material & Guia Python | `PY-DOC` | `PYTHON` | `fa-solid fa-book-open-reader`| `#818cf8` |
| **16** | ⚙️ **Scripting & Auto** | Bash Scripting & Terminal | `BASH` | `BASH` | `fa-solid fa-terminal` | `#4ade80` |
| **16b**| ⚙️ **Scripting & Auto** | PowerShell & Automation | `PWSH` | `PWSH` | `fa-solid fa-square-terminal` | `#38bdf8` |
| **16c**| ⚙️ **Scripting & Auto** | Python System Scripting | `PY-CLI` | `PY-CLI` | `fa-brands fa-python` | `#f59e0b` |
| **16d**| ⚙️ **Scripting & Auto** | Material & Guia Automação | `AUTO-DOC` | `AUTO-DOC` | `fa-solid fa-robot` | `#a855f7` |

---

## 📂 Arquitetura de Diretórios do Dataset

```text
dataset/
├── modules.json                         # Catálogo mestre dos 36 módulos
├── Linux/
│   ├── LPI-Essentials/                  # 4 módulos da família LPI Essentials
│   └── LPIC-1/                          # 4 módulos LPIC-1, guias e shell
├── Azure/                               # 4 módulos Azure (AZ-900, 104, 400 e Guia)
├── AWS/                                 # 4 módulos AWS (CLF-C02, SAA-C03, DOP-C02 e Guia)
├── Containers/                          # 4 módulos Docker, CKA, CKAD e Guia
├── Automation/                          # 4 módulos Terraform, CI/CD, Ansible e Guia
├── Monitoring/                          # 4 módulos Grafana, Prometheus, OTel e Guia
├── Python/                              # 4 módulos Python DevOps, Auto, SDK e Guia
└── Automation-Shell/                    # 4 módulos Bash, PowerShell, Python CLI e Guia
```

Cada subpasta contém:
- `BR-mod-XX.json`: Banco de questões com enunciado, opções, resposta correta e explicação detalhada.
- `material.md`: Texto longo de apoio e guia técnico em Markdown.
- `pdfs.json`: Índice de PDFs disponíveis para download e leitura.

---

## 🌐 Compatibilidade Cross-Platform (Multi-SO)

O repositório foi configurado para rodar e ser editado perfeitamente no **macOS, Windows e Linux**:

- **[.gitattributes](.gitattributes):** Força `eol=lf` em arquivos de texto, evitando inconsistências de final de linha entre `CRLF` (Windows) e `LF` (macOS/Linux).
- **[.gitignore](.gitignore):** Descarta lixos de sistema como `.DS_Store`, `Thumbs.db` e diretórios locais de IDE.

---

## 🛠️ Como Executar Localmente

Como a aplicação é 100% Client-Side, não é necessário compilar nem instalar pacotes Node:

1. Clone o repositório:
```bash
git clone git@github.com:JunioSilvestre/Estudar.git
cd Estudar
```

2. Abra o arquivo [index.html](index.html) em qualquer navegador moderno (Chrome, Firefox, Edge, Safari):
   - No macOS: `open index.html`
   - No Linux: `xdg-open index.html`
   - No Windows: `start index.html`

3. Para criar ou editar arquivos JSON de questões, acesse [builder.html](builder.html).

---

## 📄 Licença

Este projeto é disponibilizado para fins educacionais e de estudo pessoal. Sinta-se à vontade para contribuir, personalizar módulos e adicionar novos materiais!

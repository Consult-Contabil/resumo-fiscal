# Resumo Fiscal 📊

Uma aplicação web para extrair e analisar débitos fiscais de relatórios em PDF da Receita Federal do Brasil.

## 📋 Descrição

O **Resumo Fiscal** é uma ferramenta desenvolvida para facilitar a leitura e análise de débitos fiscais presentes em relatórios oficiais da Receita Federal. A aplicação processa arquivos PDF e extrai automaticamente informações sobre:

- **Débitos em aberto (SIEF)**
- **Débitos com exigibilidade suspensa**
- **Pendências diversas**
- **Informações da empresa** (CNPJ, nome, data do relatório)

## ✨ Funcionalidades

- 🔍 **Extração automática** de débitos fiscais de PDFs
- 📊 **Cálculo automático** de totais por categoria
- 🏢 **Identificação** de dados da empresa (CNPJ e nome)
- 📱 **Interface responsiva** para desktop e mobile
- 🖨️ **Funcionalidade de impressão** dos resultados
- 🎨 **Interface moderna** com Tailwind CSS

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.x**
- **Flask** - Framework web
- **pdfplumber** - Extração de texto de PDFs
- **gunicorn** - Servidor WSGI para produção

### Frontend
- **HTML5/CSS3**
- **Tailwind CSS** - Framework CSS
- **JavaScript** - Interatividade
- **Alpine.js** - Framework JavaScript minimalista

### Deploy
- **Heroku** - Plataforma de hospedagem
- **Procfile** - Configuração para Heroku

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)
- Node.js (para compilar Tailwind CSS)

### Passos para instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd resumo-fiscal
   ```

2. **Instale as dependências Python**
   ```bash
   pip install -r requirements.txt
   ```

3. **Instale as dependências Node.js**
   ```bash
   npm install
   ```

4. **Compile o CSS do Tailwind**
   ```bash
   npm run tailwind
   ```

5. **Execute a aplicação**
   ```bash
   python app.py
   ```

A aplicação estará disponível em `http://localhost:5000`

## 📖 Como Usar

1. **Acesse a aplicação** no navegador
2. **Selecione um arquivo PDF** do relatório fiscal da Receita Federal
3. **Clique em "Extrair Débitos"**
4. **Visualize os resultados** organizados por categoria
5. **Imprima os resultados** se necessário

### Formatos Suportados
- Arquivos PDF de relatórios oficiais da Receita Federal
- Relatórios com status "DEVEDOR" para extração de débitos

### Limitações
- Alguns formatos de PDF podem não ser suportados
- Quando isso ocorre, o nome da empresa e CNPJ podem não aparecer

## 📁 Estrutura do Projeto

```
resumo-fiscal/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── package.json          # Dependências Node.js
├── Procfile             # Configuração Heroku
├── runtime.txt          # Versão Python para Heroku
├── tailwind.config.js   # Configuração Tailwind CSS
├── static/
│   ├── input.css        # CSS de entrada Tailwind
│   └── output.css       # CSS compilado
└── templates/
    ├── index.html       # Página principal
    └── resultado.html   # Página de resultados
```

## 🔧 Desenvolvimento

### Executar em modo desenvolvimento
```bash
# Terminal 1 - Compilar CSS
npm run tailwind

# Terminal 2 - Executar Flask
python app.py
```

### Estrutura do Código

O arquivo `app.py` contém as principais funções:

- `converter_pdf_para_texto()` - Extrai texto e dados da empresa do PDF
- `buscar_valores_debitos()` - Identifica débitos em aberto
- `extrair_debitos_exigibilidade_suspensa()` - Processa débitos suspensos
- `somar_pendencias()` - Calcula totais por categoria

## 🌐 Deploy

### Heroku
A aplicação está configurada para deploy no Heroku:

1. **Crie uma conta no Heroku**
2. **Instale o Heroku CLI**
3. **Deploy automático** via GitHub ou manual:
   ```bash
   heroku create
   git push heroku main
   ```

### Variáveis de Ambiente
- `PORT` - Porta do servidor (configurada automaticamente no Heroku)

## 🤝 Contribuição

Este projeto está em fase de desenvolvimento. Contribuições são bem-vindas!

### Como contribuir:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença ISC. Veja o arquivo `package.json` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através dos canais oficiais da Consult Contábil.

---

**Desenvolvido por** Consult Contábil  
**Versão** 1.0.0  
**Status** Em desenvolvimento 
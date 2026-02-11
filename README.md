# 💻 Dispositivos Ffex

**Dispositivos Ffex** é uma aplicação desktop robusta desenvolvida em **Python** para o controle e inventário de equipamentos eletrônicos. Utilizando uma interface gráfica (GUI) intuitiva e armazenamento local, o sistema permite gerenciar o ciclo de vida de ativos tecnológicos com facilidade e segurança.

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.x
* **Interface Gráfica:** `Tkinter` (com `ttk.Combobox` para melhor UX)
* **Banco de Dados:** `SQLite3` (armazenamento local via arquivo `.db`)
* **Manipulação de Dados:** `Pandas` (utilizado para estruturar e exportar relatórios)
* **Exportação:** `Openpyxl` (engine para geração de arquivos `.xlsx`)

---

## ✨ Funcionalidades

O sistema oferece um fluxo completo de gerenciamento (CRUD) e exportação:

1. **Cadastro Inteligente:** Registro de dispositivos (Laptop, Teclado, Mouse, Fone) com validação de regras de negócio (ex: número de série obrigatório com 9 caracteres).
2. **Persistência Local:** Os dados são salvos em um banco de dados SQLite (`cadastro.db`), garantindo que as informações não sejam perdidas ao fechar o app.
3. **Listagem de Ativos:** Visualização rápida de todos os itens cadastrados diretamente em janelas de mensagem.
4. **Edição por Série:** Permite atualizar o estado e as observações de um dispositivo buscando-o pelo seu número de série único.
5. **Exportação para Excel:** Gera um arquivo `dispositivos_cadastrados.xlsx` com um único clique, facilitando auditorias e compartilhamento de relatórios.
6. **Limpeza de Campos:** Função integrada para resetar o formulário rapidamente.

---

## 🚀 Como Instalar e Rodar

### Pré-requisitos

Certifique-se de ter o Python instalado e as bibliotecas necessárias:

```bash
pip install pandas openpyxl

```

### Execução

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/dispositivos-ffex.git

```


2. Navegue até a pasta:
```bash
cd dispositivos-ffex

```


3. Execute o script principal:
```bash
python nome_do_seu_arquivo.py

```



---

## 📊 Estrutura do Banco de Dados

O sistema cria automaticamente uma tabela chamada `usuarios` com a seguinte estrutura:

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `id` | INTEGER | Chave primária autoincrementada |
| `dispositivo` | TEXT | Tipo do eletrônico (ex: Laptop) |
| `serie` | TEXT | Número de série único (9 dígitos) |
| `estado` | TEXT | Status atual (Ativo, Manutenção, etc) |
| `observacao` | TEXT | Notas adicionais |
| `data_cadastro` | TIMESTAMP | Data e hora automática do registro |

---

## ⚖️ Licença

Este projeto é de código aberto. Sinta-se à vontade para clonar, modificar e melhorar o sistema conforme sua necessidade.

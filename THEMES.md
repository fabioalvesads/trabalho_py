README - temas e aparência

Onde alterar
- O dicionário `THEME` em [main.py](main.py) contém as configurações principais de aparência.
- Campos disponíveis:
  - `bg`: cor de fundo da janela (hex, ex: `#ffffff`)
  - `fg`: cor do texto
  - `accent`: cor de destaque (não aplicada automaticamente em todos os widgets)
  - `button_bg`: cor de fundo dos botões
  - `button_fg`: cor do texto dos botões
  - `entry_bg`: cor de fundo de entradas e listas
  - `font`: tupla com nome da fonte e tamanho (ex: `("Segoe UI", 10)`)

Como usar
- Edite os valores no dicionário `THEME` e salve o arquivo.
- Execute o programa (`python main.py`) — as alterações serão aplicadas ao iniciar.

Personalização adicional
- Para temas mais complexos, crie variações do dicionário `THEME` (ex: `THEME_DARK`) e modifique `apply_theme` para alternar entre eles.
- Para alterar estilos do `ttk`, edite a seção `style.configure` em `apply_theme` dentro de `main.py`.

Exemplo rápido
- Mudar para tema escuro:
  - `bg: #2b2b2b`
  - `fg: #eaeaea`
  - `button_bg: #4a6fa5`
  - `entry_bg: #3a3a3a`

Se quiser, eu crio paletas prontas (claro/escuro/material).

  Paletas prontas

  As paletas disponíveis no `main.py` (variável `PALETTES`) são:

  - `light`: aparência clara padrão.
  - `dark`: tema escuro com campos escuros e texto claro.
  - `material`: paleta inspirada no Material Design (acento verde água).

  Como alternar em tempo de execução

  1. Inicie o programa: `python main.py`.
  2. No topo da janela há um seletor "Tema" — escolha `light`, `dark` ou `material`.

  Se quiser, eu já aplicei essas paletas no código. Para adicionar outra paleta, abra [main.py](main.py) e adicione uma nova entrada em `PALETTES`.
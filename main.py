# -*- coding: utf-8 -*-
import csv
import json
import os

# Comentario de teste para o git

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALUNOS_FILE = os.path.join(BASE_DIR, 'alunos.csv')
DISCIPLINAS_FILE = os.path.join(BASE_DIR, 'disciplinas.csv')
NOTAS_FILE = os.path.join(BASE_DIR, 'notas.csv')
EXPORT_FILE = os.path.join(BASE_DIR, 'dados.json')

PALETTES = {
    'Default': {'bg': '#f0f0f0', 'fg': '#000000', 'card': '#ffffff', 'accent': '#0078d7'},
    'Dark': {'bg': '#2d2d2d', 'fg': '#f5f5f5', 'card': '#3c3c3c', 'accent': '#4a90e2'},
    'Solarized': {'bg': '#fdf6e3', 'fg': '#657b83', 'card': '#eee8d5', 'accent': '#b58900'},
}
CURRENT_THEME = 'Default'
lista_aluno_ids = []
lista_disc_ids = []
lista_nota_ids = []


def ensure_file(path, headers):
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()


def criar_tabelas():
    ensure_file(ALUNOS_FILE, ['id', 'nome', 'data_nascimento'])
    ensure_file(DISCIPLINAS_FILE, ['id', 'nome', 'turno', 'sala', 'professor'])
    ensure_file(NOTAS_FILE, ['id', 'aluno_id', 'disciplina_id', 'nota'])


def normalize_row(path, row):
    if path == ALUNOS_FILE:
        if 'matricula' in row and 'id' not in row:
            row['id'] = row['matricula']
    if path == NOTAS_FILE:
        if 'valor' in row and 'nota' not in row:
            row['nota'] = row['valor']
        if 'matricula' in row and 'aluno_id' not in row:
            row['aluno_id'] = row['matricula']
    return row


def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [normalize_row(path, row) for row in reader]


def save_csv(path, rows, fieldnames):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def get_next_id(rows):
    if not rows:
        return '1'
    ids = [int(row['id']) for row in rows if row.get('id', '').isdigit()]
    return str(max(ids, default=0) + 1)


def find_row(rows, row_id):
    for row in rows:
        if row.get('id') == str(row_id):
            return row
    return None


def parse_id_from_value(value):
    if not value:
        return None
    return value.split(' - ', 1)[0].strip()


def show_error(message):
    messagebox.showerror('Erro', message)


def show_info(message):
    messagebox.showinfo('Mensagem', message)


def get_theme():
    return PALETTES.get(CURRENT_THEME, PALETTES['Default'])


def apply_theme(window):
    theme = get_theme()
    style = ttk.Style(window)
    try:
        style.theme_use('clam')
    except Exception:
        pass

    style.configure('TFrame', background=theme['bg'])
    style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
    style.configure('TButton', background=theme['card'], foreground=theme['fg'])
    style.configure('Accent.TButton', background=theme['accent'], foreground='#ffffff')
    style.configure('Card.TLabelframe', background=theme['card'], foreground=theme['fg'])
    style.configure('Card.TLabelframe.Label', background=theme['card'], foreground=theme['fg'])
    style.configure('TCombobox', fieldbackground=theme['card'], background=theme['card'], foreground=theme['fg'])
    if hasattr(window, 'configure'):
        window.configure(bg=theme['bg'])


def switch_theme(name, root):
    global CURRENT_THEME
    if name not in PALETTES:
        return
    CURRENT_THEME = name
    apply_theme(root)
    rebuild_ui(CURRENT_LAYOUT)


def listar_alunos():
    alunos = load_csv(ALUNOS_FILE)
    lista_aluno.delete(0, tk.END)
    lista_aluno_ids.clear()
    for aluno in alunos:
        lista_aluno_ids.append(aluno['id'])
        lista_aluno.insert(tk.END, f"{aluno['nome']} ({aluno['data_nascimento']})")
    cb_aluno['values'] = [f"{aluno['id']} - {aluno['nome']}" for aluno in alunos]


def inserir_aluno():
    nome = ent_nome.get().strip()
    data = ent_data.get().strip()
    if not nome:
        show_error('Informe o nome do aluno.')
        return
    alunos = load_csv(ALUNOS_FILE)
    alunos.append({'id': get_next_id(alunos), 'nome': nome, 'data_nascimento': data})
    save_csv(ALUNOS_FILE, alunos, ['id', 'nome', 'data_nascimento'])
    ent_nome.delete(0, tk.END)
    ent_data.delete(0, tk.END)
    listar_alunos()
    show_info('Aluno incluído com sucesso.')


def alterar_aluno():
    selection = lista_aluno.curselection()
    if not selection:
        show_error('Selecione um aluno para alterar.')
        return
    aluno_id = lista_aluno_ids[selection[0]]
    nome = ent_nome.get().strip()
    data = ent_data.get().strip()
    if not nome:
        show_error('Informe o nome do aluno.')
        return
    alunos = load_csv(ALUNOS_FILE)
    aluno = find_row(alunos, aluno_id)
    if aluno:
        aluno['nome'] = nome
        aluno['data_nascimento'] = data
        save_csv(ALUNOS_FILE, alunos, ['id', 'nome', 'data_nascimento'])
        listar_alunos()
        show_info('Aluno alterado com sucesso.')


def excluir_aluno():
    selection = lista_aluno.curselection()
    if not selection:
        show_error('Selecione um aluno para excluir.')
        return
    aluno_id = lista_aluno_ids[selection[0]]
    alunos = [a for a in load_csv(ALUNOS_FILE) if a['id'] != aluno_id]
    save_csv(ALUNOS_FILE, alunos, ['id', 'nome', 'data_nascimento'])
    notas = [n for n in load_csv(NOTAS_FILE) if n['aluno_id'] != aluno_id]
    save_csv(NOTAS_FILE, notas, ['id', 'aluno_id', 'disciplina_id', 'nota'])
    ent_nome.delete(0, tk.END)
    ent_data.delete(0, tk.END)
    listar_alunos()
    listar_notas()
    show_info('Aluno excluído com sucesso.')


def selecionar_aluno(event=None):
    selection = lista_aluno.curselection()
    if not selection:
        return
    aluno_id = lista_aluno_ids[selection[0]]
    aluno = find_row(load_csv(ALUNOS_FILE), aluno_id)
    if aluno:
        ent_nome.delete(0, tk.END)
        ent_nome.insert(0, aluno['nome'])
        ent_data.delete(0, tk.END)
        ent_data.insert(0, aluno['data_nascimento'])


def listar_disc():
    disciplinas = load_csv(DISCIPLINAS_FILE)
    lista_disc.delete(0, tk.END)
    lista_disc_ids.clear()
    for disc in disciplinas:
        lista_disc_ids.append(disc['id'])
        lista_disc.insert(tk.END, f"{disc['nome']} - {disc['turno']} - {disc['sala']}")
    cb_disc['values'] = [f"{disc['id']} - {disc['nome']}" for disc in disciplinas]


def inserir_disciplina():
    nome = ent_disc.get().strip()
    turno = ent_turno.get().strip()
    sala = ent_sala.get().strip()
    professor = ent_prof.get().strip()
    if not nome:
        show_error('Informe o nome da disciplina.')
        return
    disciplinas = load_csv(DISCIPLINAS_FILE)
    disciplinas.append({'id': get_next_id(disciplinas), 'nome': nome, 'turno': turno, 'sala': sala, 'professor': professor})
    save_csv(DISCIPLINAS_FILE, disciplinas, ['id', 'nome', 'turno', 'sala', 'professor'])
    ent_disc.delete(0, tk.END)
    ent_turno.delete(0, tk.END)
    ent_sala.delete(0, tk.END)
    ent_prof.delete(0, tk.END)
    listar_disc()
    show_info('Disciplina incluída com sucesso.')


def alterar_disciplina():
    selection = lista_disc.curselection()
    if not selection:
        show_error('Selecione uma disciplina para alterar.')
        return
    disc_id = lista_disc_ids[selection[0]]
    nome = ent_disc.get().strip()
    turno = ent_turno.get().strip()
    sala = ent_sala.get().strip()
    professor = ent_prof.get().strip()
    if not nome:
        show_error('Informe o nome da disciplina.')
        return
    disciplinas = load_csv(DISCIPLINAS_FILE)
    disc = find_row(disciplinas, disc_id)
    if disc:
        disc.update({'nome': nome, 'turno': turno, 'sala': sala, 'professor': professor})
        save_csv(DISCIPLINAS_FILE, disciplinas, ['id', 'nome', 'turno', 'sala', 'professor'])
        listar_disc()
        show_info('Disciplina alterada com sucesso.')


def excluir_disciplina():
    selection = lista_disc.curselection()
    if not selection:
        show_error('Selecione uma disciplina para excluir.')
        return
    disc_id = lista_disc_ids[selection[0]]
    disciplinas = [d for d in load_csv(DISCIPLINAS_FILE) if d['id'] != disc_id]
    save_csv(DISCIPLINAS_FILE, disciplinas, ['id', 'nome', 'turno', 'sala', 'professor'])
    notas = [n for n in load_csv(NOTAS_FILE) if n['disciplina_id'] != disc_id]
    save_csv(NOTAS_FILE, notas, ['id', 'aluno_id', 'disciplina_id', 'nota'])
    ent_disc.delete(0, tk.END)
    ent_turno.delete(0, tk.END)
    ent_sala.delete(0, tk.END)
    ent_prof.delete(0, tk.END)
    listar_disc()
    listar_notas()
    show_info('Disciplina excluída com sucesso.')


def selecionar_disciplina(event=None):
    selection = lista_disc.curselection()
    if not selection:
        return
    disc_id = lista_disc_ids[selection[0]]
    disc = find_row(load_csv(DISCIPLINAS_FILE), disc_id)
    if disc:
        ent_disc.delete(0, tk.END)
        ent_disc.insert(0, disc['nome'])
        ent_turno.delete(0, tk.END)
        ent_turno.insert(0, disc['turno'])
        ent_sala.delete(0, tk.END)
        ent_sala.insert(0, disc['sala'])
        ent_prof.delete(0, tk.END)
        ent_prof.insert(0, disc['professor'])


def listar_notas():
    notas = load_csv(NOTAS_FILE)
    alunos = load_csv(ALUNOS_FILE)
    disciplinas = load_csv(DISCIPLINAS_FILE)
    lista_nota.delete(0, tk.END)
    lista_nota_ids.clear()
    for nota in notas:
        aluno = find_row(alunos, nota['aluno_id'])
        disc = find_row(disciplinas, nota['disciplina_id'])
        aluno_nome = aluno['nome'] if aluno else 'Aluno removido'
        disc_nome = disc['nome'] if disc else 'Disciplina removida'
        lista_nota_ids.append(nota['id'])
        lista_nota.insert(tk.END, f"{aluno_nome} - {disc_nome}: {nota['nota']}")


def inserir_nota():
    aluno_value = cb_aluno.get()
    disc_value = cb_disc.get()
    nota_text = ent_nota.get().strip()
    if not aluno_value or not disc_value or not nota_text:
        show_error('Preencha aluno, disciplina e nota.')
        return
    aluno_id = parse_id_from_value(aluno_value)
    disc_id = parse_id_from_value(disc_value)
    if not aluno_id or not disc_id:
        show_error('Selecione aluno e disciplina válidos.')
        return
    notas = load_csv(NOTAS_FILE)
    notas.append({'id': get_next_id(notas), 'aluno_id': aluno_id, 'disciplina_id': disc_id, 'nota': nota_text})
    save_csv(NOTAS_FILE, notas, ['id', 'aluno_id', 'disciplina_id', 'nota'])
    ent_nota.delete(0, tk.END)
    listar_notas()
    show_info('Nota registrada com sucesso.')


def alterar_nota():
    selection = lista_nota.curselection()
    if not selection:
        show_error('Selecione uma nota para alterar.')
        return
    nota_id = lista_nota_ids[selection[0]]
    aluno_value = cb_aluno.get()
    disc_value = cb_disc.get()
    nota_text = ent_nota.get().strip()
    if not aluno_value or not disc_value or not nota_text:
        show_error('Preencha aluno, disciplina e nota.')
        return
    aluno_id = parse_id_from_value(aluno_value)
    disc_id = parse_id_from_value(disc_value)
    if not aluno_id or not disc_id:
        show_error('Selecione aluno e disciplina válidos.')
        return
    notas = load_csv(NOTAS_FILE)
    nota = find_row(notas, nota_id)
    if nota:
        nota.update({'aluno_id': aluno_id, 'disciplina_id': disc_id, 'nota': nota_text})
        save_csv(NOTAS_FILE, notas, ['id', 'aluno_id', 'disciplina_id', 'nota'])
        listar_notas()
        show_info('Nota alterada com sucesso.')


def excluir_nota():
    selection = lista_nota.curselection()
    if not selection:
        show_error('Selecione uma nota para excluir.')
        return
    nota_id = lista_nota_ids[selection[0]]
    notas = [n for n in load_csv(NOTAS_FILE) if n['id'] != nota_id]
    save_csv(NOTAS_FILE, notas, ['id', 'aluno_id', 'disciplina_id', 'nota'])
    ent_nota.delete(0, tk.END)
    listar_notas()
    show_info('Nota excluída com sucesso.')


def exportar_dados():
    alunos = load_csv(ALUNOS_FILE)
    disciplinas = load_csv(DISCIPLINAS_FILE)
    notas = load_csv(NOTAS_FILE)
    export_data = {
        'alunos': alunos,
        'disciplinas': disciplinas,
        'notas': notas,
    }
    with open(EXPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    show_info(f'Dados exportados para {EXPORT_FILE}')

criar_tabelas()
root = tk.Tk()
root.title('Sistema Escolar')
root.geometry('950x550')
apply_theme(root)

top_bar = tk.Frame(root, bg=get_theme()['bg'])
top_bar.pack(fill='x', padx=10, pady=(10, 0))

ttk.Label(top_bar, text='Tema:').pack(side='left')
theme_selector = ttk.Combobox(top_bar, state='readonly', values=list(PALETTES.keys()))
theme_selector.set(CURRENT_THEME)
theme_selector.pack(side='left', padx=6)

def on_theme_change(event=None):
    name = theme_selector.get()
    switch_theme(name, root)

theme_selector.bind('<<ComboboxSelected>>', on_theme_change)

content_container = tk.Frame(root, bg=get_theme()['bg'])
content_container.pack(fill='both', expand=True, padx=10, pady=10)

def populate_cards(p_alunos, p_disc, p_notas):
    global ent_nome, ent_data, lista_aluno, ent_disc, ent_turno, ent_sala, ent_prof, lista_disc
    global cb_aluno, cb_disc, ent_nota, lista_nota

    f1 = ttk.LabelFrame(p_alunos, text='Alunos', style='Card.TLabelframe', padding=(10, 10))
    f1.pack(fill='both', expand=True, padx=5, pady=5)

    ttk.Label(f1, text='Nome').pack(anchor='w')
    ent_nome = tk.Entry(f1)
    ent_nome.pack(fill='x', pady=2)

    ttk.Label(f1, text='Data de Nascimento').pack(anchor='w')
    ent_data = tk.Entry(f1)
    ent_data.pack(fill='x', pady=2)

    ttk.Button(f1, text='Incluir', command=inserir_aluno, style='Accent.TButton').pack(fill='x', pady=2)
    ttk.Button(f1, text='Alterar', command=alterar_aluno, style='Accent.TButton').pack(fill='x', pady=2)
    ttk.Button(f1, text='Excluir', command=excluir_aluno, style='Accent.TButton').pack(fill='x', pady=2)

    lista_aluno = tk.Listbox(f1)
    lista_aluno.pack(fill='both', expand=True, pady=5)
    lista_aluno.bind('<<ListboxSelect>>', selecionar_aluno)

    f2 = ttk.LabelFrame(p_disc, text='Disciplinas', style='Card.TLabelframe', padding=(10, 10))
    f2.pack(fill='both', expand=True, padx=5, pady=5)

    ttk.Label(f2, text='Nome').pack(anchor='w')
    ent_disc = tk.Entry(f2)
    ent_disc.pack(fill='x', pady=2)

    ttk.Label(f2, text='Turno').pack(anchor='w')
    ent_turno = tk.Entry(f2)
    ent_turno.pack(fill='x', pady=2)

    ttk.Label(f2, text='Sala').pack(anchor='w')
    ent_sala = tk.Entry(f2)
    ent_sala.pack(fill='x', pady=2)

    ttk.Label(f2, text='Professor').pack(anchor='w')
    ent_prof = tk.Entry(f2)
    ent_prof.pack(fill='x', pady=2)

    ttk.Button(f2, text='Incluir', command=inserir_disciplina, style='Accent.TButton').pack(fill='x', pady=2)
    ttk.Button(f2, text='Alterar', command=alterar_disciplina, style='Accent.TButton').pack(fill='x', pady=2)
    ttk.Button(f2, text='Excluir', command=excluir_disciplina, style='Accent.TButton').pack(fill='x', pady=2)

    lista_disc = tk.Listbox(f2)
    lista_disc.pack(fill='both', expand=True, pady=5)
    lista_disc.bind('<<ListboxSelect>>', selecionar_disciplina)

    f3 = ttk.LabelFrame(p_notas, text='Notas', style='Card.TLabelframe', padding=(10, 10))
    f3.pack(fill='both', expand=True, padx=5, pady=5)

    ttk.Label(f3, text='Aluno').pack(anchor='w')
    cb_aluno = ttk.Combobox(f3, state='readonly')
    cb_aluno.pack(fill='x')

    ttk.Label(f3, text='Disciplina').pack(anchor='w')
    cb_disc = ttk.Combobox(f3, state='readonly')
    cb_disc.pack(fill='x')

    ttk.Label(f3, text='Nota').pack(anchor='w')
    ent_nota = tk.Entry(f3)
    ent_nota.pack(fill='x')

    ttk.Button(f3, text='Incluir', command=inserir_nota, style='Accent.TButton').pack(fill='x', pady=2)
    ttk.Button(f3, text='Alterar', command=alterar_nota, style='Accent.TButton').pack(fill='x', pady=2)
    ttk.Button(f3, text='Excluir', command=excluir_nota, style='Accent.TButton').pack(fill='x', pady=2)

    lista_nota = tk.Listbox(f3)
    lista_nota.pack(fill='both', expand=True, pady=5)


def rebuild_ui():
    for child in content_container.winfo_children():
        child.destroy()
    notebook = ttk.Notebook(content_container)
    notebook.pack(fill='both', expand=True)
    p1 = ttk.Frame(notebook)
    p2 = ttk.Frame(notebook)
    p3 = ttk.Frame(notebook)
    notebook.add(p1, text='Alunos')
    notebook.add(p2, text='Disciplinas')
    notebook.add(p3, text='Notas')
    populate_cards(p1, p2, p3)

export_btn = ttk.Button(root, text='Exportar Dados', command=exportar_dados, style='Accent.TButton')
export_btn.pack(fill='x', padx=10, pady=10)

rebuild_ui()
listar_alunos()
listar_disc()
listar_notas()

root.mainloop()
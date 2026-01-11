import tkinter as tk
import pygame
from PIL import Image, ImageTk
import pandas as pd
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
import os

# CONFIGURAÇÕES

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_PATH = os.path.join(BASE_DIR, "img", "bg.png")

# BACKGROUND

bg_label = None
bg_image = None

def set_background(janela, image_path):
    global bg_label, bg_image

    if bg_label is None:
        bg_label = tk.Label(janela)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()

        janela.bind("<Configure>", resize_bg)

    bg_image = Image.open(image_path)
    resize_bg()

def resize_bg(event=None):
    if bg_label is None or not bg_label.winfo_exists():
        return

    w = root.winfo_width()
    h = root.winfo_height()

    resized = bg_image.resize((w, h), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(resized)

    bg_label.config(image=bg_photo)
    bg_label.image = bg_photo
        
BG_MENU = os.path.join(BASE_DIR, "img", "bg.png")
BG_QUIZ = os.path.join(BASE_DIR, "img", "bg_quiz.png")
BG_RESULT = os.path.join(BASE_DIR, "img", "bg_quiz.png")

def clear_screen():
    for widget in root.winfo_children():
        if widget != bg_label:
            widget.destroy()

# DADOS

df = pd.read_excel("questions.xlsx")

root = None
current_question = 0
score = 0
questions = []
correct_answer = None
user_name = ""
leaderboard = {}

# AUDIO

pygame.mixer.init()
current_music = None

def play_menu_music():
    global current_music
    if current_music != "menu":
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music/menu.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        current_music = "menu"

def play_quiz_music():
    global current_music
    if current_music != "quiz":
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music/quiz.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        current_music = "quiz"

# INICIAL

def create_interface():
    global root
    root = tk.Tk()
    root.title("Quiz App")
    root.geometry("450x600")
    play_menu_music()
    create_main_interface()
    root.mainloop()

# QUIZ

def load_questions():
    global questions
    questions = df.sample(n=10).values.tolist()
    random.shuffle(questions)
    
def reset_game(name):
    global current_question, score, user_name

    user_name = name
    score = 0
    current_question = 0

    load_questions()
    create_third_page(user_name)

# MENU

def create_main_interface():
    play_menu_music()

    for widget in root.winfo_children():
        if widget != bg_label:
            widget.destroy()

    root.geometry("450x600")
    set_background(root, BG_MENU)

    button_frame = tk.Frame(root)
    button_frame.pack(expand=True)

    tk.Button(
        root,
        text="INICIAR QUIZ",
        font=("Arial", 16, "bold"),
        bg="white",
        width=12,
        height=1,
        command=create_quiz_page
    ).pack(pady=1)

    tk.Button(
        root,
        text="TUTORIAL",
        font=("Arial", 14, "bold"),
        bg="white",
        width=10,
        height=1,
        command=create_tutorial_page
    ).pack(pady=10)

    footer = tk.Frame(root)
    footer.pack(side=tk.BOTTOM, fill="x", pady=10)

    tk.Button(
        root,
        text="SISTEMA",
        font=("Arial", 12, "bold"),
        bg="white",
        width=10,
        command=create_system_page
    ).pack(side=tk.LEFT, padx=20)

    tk.Button(
        root,
        text="PROBLEMAS",
        font=("Arial", 12, "bold"),
        bg="white",
        width=10,
        command=create_problem_page
    ).pack(side=tk.RIGHT, padx=20)

# NOME

def create_quiz_page():
    clear_screen()
    set_background(root, BG_PATH)

    frame = tk.Frame(root)
    frame.pack(expand=True)

    box = tk.Frame(frame, bg="white", padx=30, pady=30)
    box.pack()

    tk.Label(
        box,
        text="DIGITE SEU NOME",
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(pady=10)

    entry = tk.Entry(box, font=("Arial", 14), justify="center")
    entry.pack(pady=10)
    entry.focus()

    tk.Button(
        box,
        text="JOGAR",
        font=("Arial", 16, "bold"),
        bg="#90EE90",
        width=15,
        command=lambda: create_third_page(entry.get().strip())
    ).pack(pady=10)

    tk.Button(
        root,
        text="VOLTAR",
        font=("Arial", 12, "bold"),
        bg="#FF6347",
        command=create_main_interface
    ).place(x=10, y=10)

# QUIZ TELA

def create_third_page(name):
    global user_name, correct_answer

    if not name:
        return

    user_name = name
    play_quiz_music()
    correct_answer = tk.IntVar()

    clear_screen()
    set_background(root, BG_PATH)

    start_game()

def start_game():
    global current_question, score
    load_questions()
    score = 0
    current_question = 0
    display_question()
    
def check_answer(selected):
    global current_question, score

    if selected == correct_answer.get():
        score += 1

    current_question += 1
    display_question()

def display_question():
    global current_question

    if current_question >= len(questions):
        show_results()
        return

    clear_screen()
    set_background(root, BG_RESULT)

    frame = tk.Frame(root)
    frame.pack(expand=True)

    box = tk.Frame(frame, bg="white", padx=30, pady=30)
    box.pack()

    question, o1, o2, o3, o4, answer = questions[current_question]
    correct_answer.set(answer)

    tk.Label(
        box,
        text=f"Pergunta {current_question + 1}\n\n{question}",
        font=("Arial", 12, "bold"),
        bg="white",
        wraplength=350,
        justify="center"
    ).pack(pady=15)

    for i, opt in enumerate([o1, o2, o3, o4], start=1):

        tk.Button(
            box,
            text=opt,
            font=("Arial", 12, "bold"),
            bg="#90EE90",
            relief="flat",
            bd=0,
            wraplength=300,          # 🔹 QUEBRA DE LINHA
            justify="center",        # 🔹 TEXTO CENTRALIZADO
            padx=15,
            pady=10,
            command=lambda i=i: check_answer(i)
        ).pack(fill="x", pady=6)

# RESULTADO

def show_results():
    global leaderboard, user_name, score

    clear_screen()

    # Garantir nome válido
    if not user_name:
        user_name = "Jogador"

    # Atualizar ranking
    leaderboard[user_name] = leaderboard.get(user_name, 0) + score

    frame = tk.Frame(root)
    frame.pack(expand=True)

    tk.Label(
        frame,
        text=f"{user_name}, você acertou {score} de {len(questions)}!",
        font=("Arial", 14, "bold"),
        bg="white"
    ).pack(pady=10)

    tk.Label(
        frame,
        text="🏆 RANKING 🏆",
        font=("Arial", 16, "bold"),
        bg="white"
    ).pack(pady=10)

    # Mostrar ranking
    for name, pts in sorted(leaderboard.items(), key=lambda x: x[1], reverse=True):
        tk.Label(
            frame,
            text=f"{name}: {pts} pontos",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack()

    tk.Button(
        frame,
        text="Jogar Novamente",
        font=("Arial", 14, "bold"),
        bg="#90EE90",
        command=lambda: reset_game(user_name)
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Voltar ao Início",
        font=("Arial", 12, "bold"),
        bg="#FF6347",
        command=create_main_interface
    ).pack(pady=5)


# OUTRAS TELAS

def create_problem_page():
    global root
    
    # Limpar a janela atual
    clear_screen()
    
    root.configure(bg="#FFFFFF")
    
    # Título
    title_label = tk.Label(
        root,
        text="ESCREVA SEU NOME E RELATE UM FEEDBACK",
        font=("Arial", 12, "bold"),
        bg="#FFFFFF",
        fg="black"
    )
    title_label.pack(pady=20)
    
    # Caixa de entrada para o problema
    problem_entry = tk.Text(root, font=("Arial", 12), height=10, width=40, wrap="word")
    problem_entry.pack(pady=20)
    
    # Botão de Enviar
    send_button = tk.Button(
        root,
        text="Enviar",
        font=("Arial", 12, "bold"),
        bg="#90EE90",
        fg="black",
        width=15,
        height=2,
        command=lambda: send_problem(problem_entry.get("1.0", "end-1c"))
    )
    send_button.pack(pady=10)
    
    # Botão de Voltar
    back_button = tk.Button(
        root,
        text="Voltar",
        font=("Arial", 12, "bold"),
        bg="#FF6347",
        fg="black",
        width=15,
        height=2,
        command=create_main_interface
    )
    back_button.pack(pady=10)

def send_problem(problem_text):
    if problem_text.strip():
        try:
            # Configurações do e-mail
            sender_email = "inglesfluentemente011@gmail.com"
            sender_password = "jfaj eldo ljix fbam"  # Substitua pela senha do e-mail
            recipient_email = "diegobigode1010@gmail.com"  # Substitua pelo e-mail do destinatário

            # Configurar a mensagem
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = "Relato de Problema - Quiz App"
            
            # Corpo do e-mail
            message.attach(MIMEText(f"Relato enviado:\n\n{problem_text}", "plain"))

            # Enviar e-mail
            with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Use o servidor SMTP do seu provedor
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, message.as_string())

            # Exibir mensagem de sucesso
            messagebox.showinfo("Sucesso", "Problema enviado com sucesso!")
        except Exception as e:
            # Exibir erro, caso ocorra
            messagebox.showerror("Erro", f"Não foi possível enviar o problema.\nErro: {str(e)}")
    else:
        messagebox.showwarning("Aviso", "Por favor, escreva o problema antes de enviar.")

# Função para criar página do tutorial
tutorial_images = ["img/123.png", "img/456.png", "img/789.png", "img/101112.png"]
current_image_index = 0  # Índice da imagem atual

def create_tutorial_page():
    global root, current_image_index, tutorial_images

    # Limpar a janela atual
    clear_screen()

    # Título
    title_label = tk.Label(
        root,
        text="TUTORIAL",
        font=("Berlin sans", 14, "bold"),
        bg="#FFFFFF",
        fg="black"
    )
    title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

    # Quadro para imagem
    tutorial_image_frame = tk.Frame(root, bg="#FFFFFF")
    tutorial_image_frame.grid(row=1, column=0, columnspan=3)

    # Carregar e exibir a imagem do tutorial
    try:
        tutorial_image = Image.open(tutorial_images[current_image_index])  # Imagem atual
        tutorial_image = tutorial_image.resize((350, 500))  # Ajuste o tamanho conforme necessário
        tutorial_photo = ImageTk.PhotoImage(tutorial_image)
        tutorial_label = tk.Label(tutorial_image_frame, image=tutorial_photo, bg="#FFFFFF")
        tutorial_label.image = tutorial_photo  # Manter referência da imagem
        tutorial_label.pack()
    except Exception as e:
        tutorial_label = tk.Label(
            tutorial_image_frame,
            text="[Imagem do tutorial não disponível]",
            font=("Arial", 12, "italic"),
            bg="#FFFFFF",
            fg="black"
        )
        tutorial_label.pack()

    # Botão "Voltar"
    back_button = tk.Button(
        root,
        text="VOLTAR",
        font=("Arial", 10, "bold"),
        bg="#90EE90",
        fg="black",
        width=15,
        height=2,
        command=previous_tutorial_image  # Função para voltar
    )
    back_button.grid(row=2, column=0, sticky="w", padx=10, pady=10)

    # Botão "Avançar"
    next_button = tk.Button(
        root,
        text="AVANÇAR",
        font=("Arial", 10, "bold"),
        bg="#90EE90",
        fg="black",
        width=15,
        height=2,
        command=next_tutorial_image  # Função para avançar
    )
    next_button.grid(row=2, column=2, sticky="e", padx=10, pady=10)

def next_tutorial_image():
    global current_image_index, tutorial_images

    # Avançar para a próxima imagem
    if current_image_index < len(tutorial_images) - 1:
        current_image_index += 1
    create_tutorial_page()  # Recarregar a página do tutorial

def previous_tutorial_image():
    global current_image_index, tutorial_images

    # Voltar para a imagem anterior ou para a página inicial
    if current_image_index > 0:
        current_image_index -= 1
        create_tutorial_page()  # Recarregar a página do tutorial
    else:
        create_main_interface()  # Voltar para a página inicial do jogo
        
def create_system_page():
    global root

    # Informações do sistema
    info_text = (
        "VERSÃO DO APLICATIVO:\n"
        "- Versão 1.5.0 - Atualizada em [04/01/2026]\n\n"
        "DESENVOLVEDOR:\n"
        "- DIEGO MARQUES DE SENA\n\n"
        "- TECNOLOGIAS UTILIZADAS:\n"
        "LINGUAGENS: PYTHON\n\n"
        "BIBLIOTECAS:\n- TKINTER, PYGAME, PIL, PANDAS, RANDOM, SMTPLIB, MIMEText, MIMEMultipart, MESSAGEBOX\n\n"
        "LICENSA E TERMOS DE USO:\n"
        "- SOFTWARE GRATUITO PARA FINS EDUCACIONAIS.\n\n"
        "PARA ATUALIZAÇÕES FUTURAS CONSULTE O REPOSITÓRIO NO GITHUB:\n"
        "- https://github.com/Di3go0011/Quiz"
    )

    # Atualizar o conteúdo da janela atual
    clear_screen()

    # Ajustar layout responsivo
    root.geometry("450x600")

    info_label = tk.Label(root, text=info_text, justify="left", font=("Arial", 14, "bold"),bg="white", wraplength=400, anchor="nw")
    info_label.pack(pady=20, padx=20, fill="both", expand=True)

    # Botão de voltarr
    back_button = tk.Button(root, text="Voltar", font=("Arial", 12, "bold"), bg="#FF6347", fg="black", command=create_main_interface)
    back_button.pack(pady=10)


# START

if __name__ == "__main__":
    create_interface()
# Jogo.py - A Lenda do Cavaleiro do Castelo
import tkinter as tk   # Importa a biblioteca tkinter para a interface gráfica
from tkinter import messagebox # Importa a caixa de diálogo de mensagens
from PIL import Image, ImageTk # Importa a biblioteca PIL para manipulação de imagens
import os  # Importa a biblioteca os para manipulação de arquivos e diretórios

class Respostas:
    def __init__(self,texto_da_resposta, proximo_no):
        self.texto = texto_da_resposta
        self.proximo_no = proximo_no

class Perguntas:
    def __init__(self, start_end_no, texto_do_no, caminho_imagem=None):
        self.id = start_end_no
        self.texto = texto_do_no
        self.caminho_imagem = caminho_imagem
        self.respostas = []
        
    def adicionar_resposta(self, texto_da_resposta, proximo_no):
        self.respostas.append(Respostas(texto_da_resposta, proximo_no))
              
class Castle:
    def __init__(self):
        self.nos = {}
        
    def adicionar_no(self, start_end_no, texto_do_no, caminho_imagem=None):
        if start_end_no not in self.nos:
            self.nos[start_end_no] = Perguntas(start_end_no, texto_do_no, caminho_imagem)
            
    def adicionar_escolha(self, id_no_origem, texto_da_resposta, id_no_destino):
        if id_no_origem in self.nos and id_no_destino in self.nos:
            self.nos[id_no_origem].adicionar_resposta(texto_da_resposta, id_no_destino)

class CASTLEGUI(tk.Tk):
    def __init__(self, jogo):
        # Chama o construtor da classe pai (tk.Tk) para iniciar a janela
        super().__init__()
        
        self.jogo = jogo
        self.title("A Lenda do Cavaleiro do Castelo")
        self.geometry("600x650")

        # Widget para exibir a imagem da cena
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=10)

        # Widget para exibir o texto da história
        self.text_label = tk.Label(self, text="", wraplength=550, justify="center", font=("Garamond", 14))
        self.text_label.pack(pady=10, padx=10)

        # Frame que agrupa os botões de escolha para melhor organização
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=20, padx=20, fill="x")

    def iniciar_jogo(self, id_no_inicial):
        """Começa a aventura a partir da cena inicial."""
        self.mostrar_no(id_no_inicial)

    def mostrar_no(self, id_no):
        """Atualiza a tela inteira (imagem, texto e botões) para a cena atual."""
        no_atual = self.jogo.nos[id_no]

        # 1. Chama o método para carregar e exibir a imagem correta
        self.carregar_imagem(no_atual.caminho_imagem)

        # 2. Atualiza o texto da história
        self.text_label.config(text=no_atual.texto)

        # 3. Limpa os botões da escolha anterior para dar lugar aos novos
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        # 4. Cria os novos botões ou a mensagem de fim de jogo
        if not no_atual.respostas:
            # Se for uma cena final (sem respostas)
            fim_label = tk.Label(self.buttons_frame, text="--- FIM DA JORNADA ---", font=("Arial", 12, "bold"))
            fim_label.pack()
            botao_fechar = tk.Button(self.buttons_frame, text="Fechar Aventura", command=self.quit)
            botao_fechar.pack(pady=10, fill="x")
        else:
            # Se ainda houver escolhas, cria um botão para cada uma
            for resposta in no_atual.respostas:
                # O uso de 'lambda' aqui é crucial para garantir que cada botão
                # chame a função com o 'proximo_no' correto.
                command = lambda prox_no=resposta.proximo_no: self.mostrar_no(prox_no)
                button = tk.Button(self.buttons_frame, text=resposta.texto, command=command, font=("Arial", 11))
                button.pack(pady=5, fill="x")

    def carregar_imagem(self, caminho_imagem):
        """
        Carrega e exibe uma imagem na tela.
        Este método foi corrigido para funcionar corretamente com o Tkinter.
        """
        # Define um caminho padrão para o caso da imagem da cena não ser encontrada
        caminho_real = caminho_imagem if caminho_imagem and os.path.exists(caminho_imagem) else "imagens/default.png"
        
        try:
            img = Image.open(caminho_real)
            # Redimensiona a imagem para caber na tela, mantendo a proporção
            img.thumbnail((500, 350)) 
            photo = ImageTk.PhotoImage(img)

            self.image_label.config(image=photo)
            

            # O Python pode "esquecer" da imagem e ela não aparecer.
            # Guardamos uma referência dela no próprio widget para garantir que ela fique na tela.
            self.image_label.image = photo

        except FileNotFoundError:
            messagebox.showerror("Erro de Imagem", f"Não foi possível encontrar o arquivo: {caminho_real}\nVerifique a pasta 'imagens'.")
            self.image_label.config(text=f"Imagem não encontrada:\n{caminho_real}", image='')
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao carregar a imagem: {e}")

def montar_aventura():
    """Cria o objeto do jogo e popula com todas as cenas e escolhas."""
    jogo = Castle()

    # --- Definindo as Cenas (Nós) da Aventura do Cavaleiro ---
    jogo.adicionar_no("entrada",
                    "Você, nobre cavaleiro, chega à entrada do imponente Castelo das Sombras para salvar a princesa. A grande porta de carvalho está trancada.",
                    "imagens/castelo_entrada.png")
    
    jogo.adicionar_no("salao_principal",
                    "Você adentra o vasto salão principal. Tapeçarias antigas adornam as paredes. Há duas passagens: um corredor escuro à esquerda e uma grande escadaria à direita.",
                    "imagens/salao_principal.png")

    jogo.adicionar_no("corredor_armadilha",
                    "Você avança pelo corredor escuro, mas pisa em uma placa de pressão! Uma rede cai do teto, prendendo você! Sua jornada termina aqui.",
                    "imagens/fim_triste.png")

    jogo.adicionar_no("escadaria_torre",
                    "Você sobe a imponente escadaria e chega ao topo de uma torre. Lá, você avista uma cela com uma figura familiar...",
                    "imagens/torre.png")
    
    jogo.adicionar_no("cela_dragao",
                    "Ao se aproximar da cela, um rugido ecoa! Um temível dragão surge das sombras, guardando a princesa!",
                    "imagens/dragao_feroz.png")

    jogo.adicionar_no("vitoria",
                    "Com coragem e aço, você derrota o dragão! A Princesa está livre e segura. Vocês fogem do castelo juntos, vitoriosos!",
                    "imagens/princesa_feliz.png")

    # --- Definindo as Escolhas (Arestas) que conectam as cenas ---
    jogo.adicionar_escolha("entrada", "Usar sua força para arrombar a porta.", "salao_principal")
    jogo.adicionar_escolha("entrada", "Procurar por uma entrada secreta nos arredores.", "salao_principal")

    jogo.adicionar_escolha("salao_principal", "Seguir pelo corredor escuro à direita.", "corredor_armadilha")
    jogo.adicionar_escolha("salao_principal", "Subir a grande escadaria à esquerda .", "escadaria_torre")
    
    jogo.adicionar_escolha("escadaria_torre", "Aproximar-se da cela para investigar.", "cela_dragao")
    
    jogo.adicionar_escolha("cela_dragao", "Lutar contra o dragão com sua espada!", "vitoria")
    jogo.adicionar_escolha("cela_dragao", "Tentar fugir do dragão.", "corredor_armadilha")
    
    return jogo

if __name__ == "__main__":
    # 1. Cria a instância do jogo com toda a história dentro
    meu_jogo = montar_aventura()
    
    # 2. Cria e inicia a nossa interface gráfica, que controlará o jogo
    app = CASTLEGUI(meu_jogo)
    
    # 3. Começa o jogo na cena "entrada"
    app.iniciar_jogo("entrada")
    
    # 4. Inicia o loop principal da interface, que a mantém aberta e esperando por cliques
    app.mainloop()
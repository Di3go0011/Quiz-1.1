import pandas as pd

# Lista de perguntas
questions = [
    ["Qual é a capital da França?", "Paris", "Londres", "Berlim", "Roma", 1],
    ["Qual é o resultado de 8 + 5?", "12", "13", "15", "18", 2],
    ["Quem pintou a Mona Lisa?", "Picasso", "Da Vinci", "Van Gogh", "Warhol", 2],
    ["Quanto é 6 multiplicado por 7?", "36", "42", "48", "54", 2],
    ["Qual é o maior planeta do sistema solar?", "Marte", "Saturno", "Júpiter", "Vênus", 3],
    ["Quem escreveu a obra 'Dom Quixote'?", "Machado de Assis", "Miguel de Cervantes", "Jorge Luis Borges", "Gabriel García Márquez", 2],
    ["Qual é a fórmula química da água?", "H2O", "CO2", "NaCl", "CH4", 1],
    ["Quem foi o primeiro presidente dos Estados Unidos?", "George Washington", "Abraham Lincoln", "Thomas Jefferson", "John F. Kennedy", 1],
    ["Qual é o resultado de 4 ao cubo?", "16", "32", "64", "128", 3],
    ["Qual é a capital da Rússia?", "Moscou", "São Petersburgo", "Kiev", "Varsóvia", 1],
    ["Quem descobriu a teoria da relatividade?", "Isaac Newton", "Galileu Galilei", "Albert Einstein", "Nikola Tesla", 3],
    ["Qual é o símbolo químico do ouro?", "Au", "Ag", "Cu", "Fe", 1],
    ["Quem foi o autor da obra 'Romeu e Julieta'?", "William Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen", 1],
    ["Qual é a capital do Brasil?", "Rio de Janeiro", "Brasília", "São Paulo", "Salvador", 2],
    ["Qual é o resultado de 9 dividido por 3?", "1", "2", "3", "4", 3],
    ["Quem pintou a obra 'A Noite Estrelada'?", "Leonardo da Vinci", "Michelangelo", "Salvador Dalí", "Vincent van Gogh", 4],
    ["Qual é o maior oceano do mundo?", "Atlântico", "Índico", "Pacífico", "Ártico", 3],
    ["Qual é o resultado de 2 elevado a 8?", "8", "16", "64", "256", 4],
    ["Quem escreveu a obra '1984'?", "George Orwell", "Aldous Huxley", "Ernest Hemingway", "F. Scott Fitzgerald", 1],
    ["Qual é o resultado de 15 menos 7?", "5", "6", "7", "8", 3],
    ["Quem foi o pintor do quadro 'A Última Ceia'?", "Pablo Picasso", "Salvador Dalí", "Michelangelo", "Leonardo da Vinci", 4]
    ["Normalmente, quantos litros de sangue uma pessoa tem? Em média, quantos são retirados numa doação de sangue?", "Tem entre 2 a 4 litros. São retirados 450 mililitros", "Tem entre 4 a 6 litros. São retirados 450 mililitros", "Tem 10 litros. São retirados 2 litros", "Tem 7 litros. São retirados 1,5 litros", 2],
    ["De quem é a famosa frase 'Penso, logo existo'?", "Platão", "Galileu Galilei", "Sócrates", "Descartes", 4],
    ["De onde é a invenção do chuveiro elétrico?", "França", "Inglaterra", "Brasil", "Austrália", 3],
    ["Quais o menor e o maior país do mundo?", "Vaticano e Rússia", "Nauru e China", "Mônaco e Canadá", "Malta e Estados Unidos", 1],
    ["Qual o nome do presidente do Brasil que ficou conhecido como Jango?", "Jânio Quadros", "Getúlio Vargas", "João Goulart", "João Figueiredo", 3],
    ["Qual o grupo em que todas as palavras foram escritas corretamente?", "Asterístico, beneficiente, meteorologia, entertido", "Asterisco, beneficente, meteorologia, entretido", "Asterisco, beneficente, metereologia, entretido", "Asterístico, beneficiente, metereologia, entretido", 2],
    ["Quantas casas decimais tem o número pi?", "Duas", "Centenas", "Infinitas", "Vinte", 3],
    ["Atualmente, quantos elementos químicos a tabela periódica possui?", "113", "118", "109", "92", 2],
    ["O que a palavra legend significa em português?", "Legenda", "Conto", "Lenda", "Legendário", 3],
    ["Quais os principais autores do Barroco no Brasil?", "Gregório de Matos, Bento Teixeira e Manuel Botelho de Oliveira", "Miguel de Cervantes, Gregório de Matos e Danthe Alighieri", "Padre Antônio Vieira, Padre Manuel de Melo e Gregório de Matos", "Castro Alves, Bento Teixeira e Manuel Botelho de Oliveira", 1],
    ["Quais as duas datas que são comemoradas em novembro?", "Independência do Brasil e Dia da Bandeira", "Proclamação da República e Dia Nacional da Consciência Negra", "Black Friday e Dia da Árvore", "Dia do Médico e Dia de São Lucas", 2],
    ["Quanto tempo a luz do Sol demora para chegar à Terra?", "12 minutos", "1 dia", "12 horas", "8 minutos", 4],
    ["Quais são os três predadores do reino animal reconhecidos pela habilidade de caçar em grupo, se camuflar para surpreender as presas e possuir sentidos apurados, respectivamente:", "Tubarão branco, crocodilo e sucuri", "Hiena, urso branco e lobo cinzento", "Leão, tubarão branco e urso cinzento", "Tigre, gavião e orca", 2],
    ["Qual personagem folclórico costuma ser agradado pelos caçadores com a oferta de fumo?", "Caipora", "Lobisomem", "Saci", "Boitatá", 3],
    ["Em que período da pré-história o fogo foi descoberto?", "Neolítico", "Paleolítico", "Idade Média", "Período da Pedra Polida", 2],
    ["Qual das alternativas abaixo apenas contêm classes de palavras?", "Vogais, semivogais e consoantes", "Artigo, verbo transitivo e verbo intransitivo", "Substantivo, verbo e preposição", "Hiatos, ditongos e tritongos", 3],
    ["Qual a montanha mais alta do Brasil?", "Pico da Neblina", "Pico Paraná", "Monte Roraima", "Pico Maior de Friburgo", 1],
    ["Qual a velocidade da luz?", "300 000 000 metros por segundo (m/s)", "150 000 000 metros por segundo (m/s)", "299 792 458 metros por segundo (m/s)", "30 000 000 metros por segundo (m/s)", 3],
    ["Em qual local da Ásia o português é língua oficial?", "Índia", "Portugal", "Macau", "Filipinas", 3],
    ["Como é a conjugação do verbo caber na 1.ª pessoa do singular do presente do indicativo?", "Eu caibo", "Eu cabo", "Ele cabe", "Nenhuma das alternativas", 1],
    ["Qual foi o recurso utilizado inicialmente pelo homem para explicar a origem das coisas?", "A Filosofia", "A Biologia", "A Mitologia", "A Astronomia", 3],
    ["Quais os planetas do sistema solar?", "Terra, Vênus, Saturno, Urano, Júpiter, Marte, Netuno, Mercúrio", "Júpiter, Marte, Mercúrio, Netuno, Plutão, Saturno, Terra, Urano, Vênus", "Júpiter, Marte, Mercúrio, Netuno, Plutão, Saturno, Sol, Terra, Urano, Vênus", "", 1],
    ["Qual o maior animal terrestre?", "Baleia Azul", "Dinossauro", "Elefante africano", "Girafa", 3],
    ["Quem foi o primeiro homem a pisar na Lua? Em que ano aconteceu?", "Yuri Gagarin, em 1961", "Neil Armstrong, em 1969.", "Charles Duke, em 1971", "Buzz Aldrin, em 1969", 2],
    ["Quais são os cromossomos que determinam o sexo masculino?", "Os V", "Os X", "Os Y", "Os Z", 3],
    ["Quantos elementos possui o conjunto dos números naturais?", "Apenas dois (0 e 1)", "100 elementos", "apenas 10, que são os números de 0 a 9", "infinitos elementos", 4],
    ["Em uma operação de fatoração, devemos...", "fabricar peças a serem usadas em jogos infantis", "elevar um número ao quadrado", "decompor um número em fatores primos", "calcular quantas unidades falta para um número chegar a 1000", 3],
    ["O que é um número decimal?", "qualquer número que termina em zero", "um número que passou por 10 multiplicações", "um número expresso em forma de fração", "aquele no qual a parte inteira é separada da parte decimal por uma vírgula", 4],
    ["Qual dos objetos abaixo não possui forma esférica?", "bola de futebol", "bola de vôlei", "bola de ping pong", "bola de futebol americano", 4],
    ["O que é um compasso?", "instrumento usado para medir o tamanho dos passos de uma pessoa", "é uma trena com aproximadamente 3 metros de comprimento", "instrumento de desenho usado para traçar circunferências", "um relógio analógico antigo", 3]
]

# Criar DataFrame do pandas
df = pd.DataFrame(questions, columns=["Pergunta", "Opção 1", "Opção 2", "Opção 3", "Opção 4", "Resposta"])

# Salvar no arquivo do Excel
df.to_excel("questions.xlsx", index=False, engine='openpyxl')

print("Perguntas inseridas com sucesso no arquivo questions.xlsx!")
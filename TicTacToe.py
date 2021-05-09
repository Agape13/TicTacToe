from tkinter import *

def setwindow(win):
    win.title("My window")
    w = win.winfo_reqwidth()
    h = win.winfo_reqheight()
    x = int((win.winfo_screenwidth() - w)/4)
    y = int((win.winfo_screenheight() - h) / 4)
    win.geometry("+{0}+{1}".format(x, y))
    win.resizable(False, False)
    win.config(bg='white')

def setwincolor(event):
    event.widget.config(bg='green')

def resetwincolor(event):
    event.widget.config(bg='#999')

#Array of empty cells
def empty(board):
    e=[]
    for i in range(9):
        if board[i]==0:
            e.append(i)
    return e

#Who is the winner
def is_end(board):
    temp=0
    for i in range(3):
        if board[i*3]==board[i*3+1] and board[i*3]==board[i*3+2]:
            temp=board[i*3]
            break
    for i in range(3):
        if board[i]==board[i+3] and board[i]==board[i+6]:
            temp=board[i]
            break
    if board[0]==board[4] and board[0]==board[8]:
        temp=board[0]
    if board[2]==board[4] and board[2]==board[6]:
        temp=board[2]
    if temp=='c':
        temp=1
    elif temp=='z':
        temp=-1
    return temp

#Minimax
def nextstep(board, player):
    moves = []
    score = []
    empty_cells = empty(board)
    current_score = is_end(board)
    if current_score != 0 or len(empty_cells) == 0:
        return current_score, 9
    else:
        i = 0
        while i < len(empty_cells):
            move = empty_cells[i]
            newboard = []
            for n in board:
                newboard.append(n)
            if player == 'c':
                newboard[move] = 'c'
                result = nextstep(newboard, 'z')[0]
            else:
                newboard[move] = 'z'
                result = nextstep(newboard, 'c')[0]
            score.append(result)
            moves.append(move)
            i += 1
    bestmove = 9
    if player == 'c':
        bestscore = -10000
        i = 0
        while i < len(score):
            if score[i] > bestscore:
                bestmove = moves[i]
                bestscore = score[i]
            i += 1
    else:
        bestscore = 10000
        i = 0
        while i < len(score):
            if score[i] < bestscore:
                bestmove = moves[i]
                bestscore = score[i]
            i += 1
    return bestscore, bestmove

#Start a new game
def restart():
    global elems
    canv.destroy()
    elems = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9):
        buts[i].destroy()
        buts[i] = Button(win, bg='#999')
        buts[i].bind('<Enter>', setwincolor)
        buts[i].bind('<Leave>', resetwincolor)
        buts[i].bind('<Button-1>', setx)
        buts[i].grid(row=i // 3, column=i % 3, ipadx=100, ipady=100, sticky='nesw')

#Message "Game over"
def game_over():
    global canv
    canv=Canvas(win, width=250, height=200, bd=2)
    game_lab=Label(canv, text='Игра окончена!', font='Times 20', fg='Red')
    winner_lab=Label(canv, font='Times 20', fg='Blue')
    result=is_end(elems)
    if result==1:
        winner_lab.config(text='Вы выиграли')
    elif result==-1:
        winner_lab.config(text='Вы проиграли')
    else:
        winner_lab.config(text='Ничья')
    canv.place(relx=0.5, rely=0.5, anchor='center')
    game_lab.place(relx=0.5, rely=0.2, anchor='center')
    winner_lab.place(relx=0.5, rely=0.4, anchor='center')
    but_restart=Button(canv, text='Начать заново', font='Times 18', command=restart)
    but_restart.place(relx=0.5, rely=0.8, anchor='center')

#Place '0'
def setzero():
    if len(empty(elems))>0:
        i = nextstep(elems, 'z')[1]
        if i!=9:
            buts[i].destroy()
            buts[i] = Label(win, image=zero, bd=0)
            buts[i].grid(row=i//3, column=i%3)
            elems[i] = 'z'
        else:
            game_over()
    else:
        game_over()

    end = is_end(elems)
    if end == -1:
        game_over()

#Place 'x'
def setx(event):
    k=0
    for i in range(9):
        if event.widget==buts[i]:
            k=i
    event.widget.destroy()
    buts[k] = Label(win, image=cross, bd=0)
    buts[k].grid(row=k//3, column=k%3)
    elems[k]='c'
    end=is_end(elems)
    if end==0:
        setzero()
    else:
        game_over()

win=Tk()
setwindow(win)

buts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
elems = [0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(9):
    buts[i] = Button(win, bg='#999')
    buts[i].bind('<Enter>', setwincolor)
    buts[i].bind('<Leave>', resetwincolor)
    buts[i].bind('<Button-1>', setx)
    buts[i].grid(row=i // 3, column=i % 3, ipadx=100, ipady=100, sticky='nesw')

cross = PhotoImage(file='files/cross.png')
zero = PhotoImage(file='files/zero.png')

win.mainloop()
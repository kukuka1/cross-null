from random import randint
from tkinter import *
from tkinter import ttk
from time import sleep

def a_bot(mtx_ub):
    # по строкам, по столбцам
    for i in range(3):
        if sum(mtx_ub[i])==3:
            return(True)
    for i in range(3):
        if sum(list(zip(mtx_ub[0],mtx_ub[1],mtx_ub[2]))[i])==3:
            return(True)
    # диаг 1
    s=0
    for i in range(3):
        s+=mtx_ub[i][i]
    if s==3:
        return(True)
    # диаг 2
    s=0
    j = 2
    for i in range(3):
        s+=mtx_ub[j][i]
        j-=1
        if s==3:
            return(True)
    return(False)
        
def b_bot(st_ub):
    # промежуток по строкам, столбцам
    k = -1
    dd = []
    for n in st_ub:
        k+=1
        for m in st_ub[:k:]+st_ub[k+1::]:
            if n[0]==m[0] and ([n[0],3-(n[1]+m[1])] in mtx_space):
                return([n[0],3-(n[1]+m[1])])
            elif n[1]==m[1] and ([3-(n[0]+m[0]),n[1]] in mtx_space):
                return([3-(n[0]+m[0]),n[1]])
            elif n[0]==n[1] and m[0]==m[1] and ([3-(n[0]+m[0]),3-(n[1]+m[1])] in mtx_space):
                return([3-(n[0]+m[0]),3-(n[1]+m[1])])
            elif n[0]+m[0]==2 and n[1]+m[1]==2 and ([3-(n[0]+m[0]),3-(n[1]+m[1])] in mtx_space):
                return([3-(n[0]+m[0]),3-(n[1]+m[1])])
    return(False)

root = Tk()
canv = Canvas(root,width=400,height=400,bg='WHITE')
c = PhotoImage(file="c.gif")
n = PhotoImage(file="n.gif")
canv.create_line(400/3,0,400/3,400,width=5,fill='BLUE')
canv.create_line(400*2/3,0,400*2/3,400,width=5,fill='BLUE')
canv.create_line(0,400/3,400,400/3,width=5,fill='BLUE')
canv.create_line(0,400*2/3,400,400*2/3,width=5,fill='BLUE')
strt_x=ttk.Button(root,text="Играть крестиками")
strt_o=ttk.Button(root,text="Играть ноликами")
for i in range(4)[1::]:
	for j in range(4)[1::]:
		canv.create_rectangle(400/3*i-400/3,400/3*j-400/3,400/3*i,400/3*j,fill='',tag='r'+str(i-1)+str(j-1),width=0)

def stp_u(event):
    global go
    it = event.widget.find_withtag('current')
    if [int(canv.gettags(it)[0][1]),int(canv.gettags(it)[0][2])] in mtx_space:
        go=event.widget.find_withtag('current')
    
def x(event):
    global tread
    tread = 1
    strt_x.grid_remove()
    strt_o.grid_remove()

def o(event):
    global tread
    tread = 0
    strt_x.grid_remove()
    strt_o.grid_remove()
    
mtx_space=mtx_space=[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
strt_o.grid()
strt_x.grid()
canv.grid(row=0,column=0,columnspan=2)
strt_x.grid(row=0,column=0)
strt_o.grid(row=0,column=1)
strt_x.bind('<Button-1>', x)
strt_o.bind('<Button-1>', o)
canv.bind('<Button-1>',stp_u)

win = 0
go = 0
tread=2
root.update()
        
while True:
    while tread==2:
        root.update()
    if tread==1:
        im1 = c
        im2 = n
    else:
        im1 = n
        im2 = c
    canv.delete('im','text')
    steps = []
    steps_u = []
    steps_b = []
    mtx_space=[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    mtx = [[0,0,0],[0,0,0],[0,0,0]]
    mtx_u = [[0,0,0],[0,0,0],[0,0,0]]
    mtx_b = [[0,0,0],[0,0,0],[0,0,0]]
    st = []
    for l in range(9):
        print(tread)
        if a_bot(mtx_u):
            canv.create_image(st[0]*400/3+400/6,st[1]*400/3+400/6,image=im1,tag='im')
            win=1
        elif tread==1:
            go = 0
            while go==0:
                root.update()
            item = go
            go=0
            st = [int(canv.gettags(item)[0][1]),int(canv.gettags(item)[0][2])]
            #print(st)
            steps_u.append(st)
            mtx[st[0]][st[1]] = 1
            mtx_u[st[0]][st[1]] = 1
            canv.create_image(st[0]*400/3+400/6,st[1]*400/3+400/6,image=im1,tag='im')
        elif tread==0:
            st = b_bot(steps_b)
            if not st:
                st = b_bot(steps_u)
                if not st:
                    st = mtx_space[randint(0,8-len(steps))]
            else:
                win = 2
            steps_b.append(st)
            mtx[st[0]][st[1]] = 1
            mtx_b[st[0]][st[1]] = 1
            canv.create_image(st[0]*400/3+400/6,st[1]*400/3+400/6,image=im2,tag='im')
        root.update()
        tread = ~tread + 2
        if st in mtx_space:
            steps.append(st)
            mtx_space.remove(st)
        if win==1:
            canv.create_text(200,200,text='USER\nWIN!',fill='RED',font=('Arial',70,'bold'),justify='center',tag='text')
            break
        elif win==2:
            canv.create_text(200,200,text='BOT\nWIN!',fill='RED',font=('Arial',70,'bold'),justify='center',tag='text')
            break
    tread = 2
    go = 0
    win = 0
    strt_o.grid()
    strt_x.grid()


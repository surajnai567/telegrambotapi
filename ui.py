from tkinter import Tk, Button , Label, Text, Entry, \
    Listbox, VERTICAL, Scrollbar, StringVar

import schedule



def delete_add_fun(status,image, button_url, button_text, time, lab):
    lab['bg'] = 'red'
    status.set('stoped')
    image.set('')
    button_url.set('')
    button_text.set('')
    time.set('')


def start_add_fun(status, image, button_url_1, button_url_2, time, lab):
    if button_url_1.get()!="" and button_url_2.get() !="" and image.get()!="" and time.get() !="":
        lab['bg'] = 'green'
        status.set('sending...')
        button = [['order', button_url_1], ['service', button_url_2]]
     #   schedule.every(time.get()).seconds.\
      #      do(lambda :bot.send_image_with_button_caption(image_url=image.get(), caption='pass'))
    else:
        status.set("please enter correct detail..")


def main():

    bot=Tk()
    bot.title('telegram bot')
    bot.geometry("500x200")

    # string var
    st = StringVar()
    img = StringVar()
    btex = StringVar()
    burl = StringVar()
    tim = StringVar()
    st.set('please submit details..')


    image = Label(bot, text='image location')
    image.grid(row=0, column=0, padx=5, pady=5)
    image_loc = Entry(bot, textvariable = img)
    image_loc.grid(row=0, column=1, padx=5, pady=5)

    button = Label(bot, text='button text')
    button.grid(row=1, column=0, padx=5, pady=5)
    button_text = Entry(bot, textvariable = btex)
    button_text.grid(row=1, column=1, padx=5, pady=5)

    button_u = Label(bot, text='button url')
    button_u.grid(row=2, column=0, padx=5, pady=5)
    button_url = Entry(bot, textvariable = burl)
    button_url.grid(row=2, column=1, padx=5, pady=5)

    time = Label(bot, text='time')
    time.grid(row=3, column=0, padx=5, pady=5)
    time_mint = Entry(bot, textvariable = tim)
    time_mint.grid(row=3, column=1, padx=5, pady=5)


    submit_add=Button(bot, text="Submit add", width=10, command=lambda :start_add_fun(st,img,burl,btex,tim, status))
    submit_add.grid(row=5,column=1, padx=10, pady=10)

    status = Label(bot, textvariable=st, bg = 'blue', fg='white')
    status.grid(row=0, column=4, padx=0, pady=5)

    delete_add=Button(bot, text="Delete add",width=10, command=lambda :delete_add_fun(st,img,burl,btex,tim, status))
    delete_add.grid(row=1,column=4, padx=10,pady=10)

    lab = Label(bot, text='Status:-')
    lab.grid(row=0, column=3, padx=20, pady=5)

    txt = Label(bot, text = 'text')
    txt.grid(row=0, column=4, padx=0, pady=5)

    text=Text(bot, width=10, command=lambda :delete_add_fun(st,img,burl,btex,tim, status))
    text.grid(row=1,column=4, padx=10,pady=10)
    bot.mainloop()

mess = ['order', 'service']
button = ['a.com', 'b.com', 'c.com', 'd.com', 'e.com', 'f.com']


j = 0
for i in range(0, len(button), 2):
    print( mess[j], button[i], button[i+1])
    j = j + 1

def get_buttons(button_text:list, button:list):
    but = []
    j = 0
    for i in range(0, len(button), 2):
        but.append([button_text[j], ])


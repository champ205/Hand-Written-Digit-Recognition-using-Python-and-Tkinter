import tkinter as tk
root = tk()
cwgt=Canvas(root)
cwgt.pack(expand=True, fill=BOTH)
image1=PhotoImage(file="background1.png")
# keep a link to the image to stop the image being garbage collected
cwgt.img=image1
cwgt.create_image(0, 0, anchor=NW, image=image1)
b1=Button(cwgt, text="Hello", bd=0)
cwgt.create_window(20,20, window=b1, anchor=NW)
root.mainloop()

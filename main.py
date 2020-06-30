import one
import webcam
import images
from PIL import ImageTk, Image
from tkinter import *
import os
from tkinter import filedialog,messagebox

root = Tk()
root.title("OBJECT DETECTION AND RECOGNITION")

#root.geometry("500x500")

def extend(fr,row,col):
	a,b=row
	for temp in range(a,b+1):
		Grid.rowconfigure(fr, temp,weight=1)
	a,b=col
	for temp in range(a,b+1):
		Grid.columnconfigure(fr, temp,weight=1)

extend(root,(0,1),(0,0))

#frame1
frame1=Frame(root,bg="grey")
frame1.grid(row=0,column=0,sticky=N+S+W+E)
ima4=PhotoImage(file="WITHC.png")
ima5=PhotoImage(file="WITHG.png")


#frame2
frame2=Frame(root, bg="SKYBLUE")
frame2.grid(row=1,column=0,sticky=N+S+W+E)
extend(frame2,(0,1),(0,1))
var=IntVar()

Rad0=Radiobutton(frame2,image=ima4,variable=var,value=0,bg="white")
Rad0.grid(row=0,column=0,padx=60,pady=50,sticky=N+S+W+E)
Rad1=Radiobutton(frame2,image=ima5,variable=var,value=1,bg="white")
Rad1.grid(row=0,column=1,padx=60,pady=50,sticky=N+S+W+E)

#variables
submit=0
outdir=""
names=[]
ext=[]



def out(a):
	global outdir
	outdir=""
	outdir=a
	
def dis():
	but0["state"]="disabled"
	but1["state"]="disabled"
	but2["state"]="disabled"
	Rad0["state"]="disabled"
	Rad1["state"]="disabled"


def en():
	but0["state"]="active"
	but1["state"]="active"
	but2["state"]="active"
	Rad0["state"]="active"
	Rad1["state"]="active"


#image
def img():
	#img1=PhotoImage(file="seimage.png")
	top = Toplevel()
	gpu=var.get()
	top.title("WORK ON IMAGES")
	global Rad1,Rad0 ,dis,en,extend,names,submit
	
	
	def temp():
		print("[INFO] GPU IS >>"+ str(gpu))
		realList=[]
			
		for a in range(len(names)):
			if ext[a]:
				realList.append(names[a])
			else:
				continue
		images.img(realList,gpu,0.5,0.3,outdir)#img(imgs,gpu,conf,thres,outpath)
		lab=Label(top,text="SAVED SUCCESSFULLY...")
		lab.grid(row=4,column=0,sticky=N+S+W+E,columnspan=2)
	
	def PROCEED():
		global outdir, submit
		submit=1
		
		if outdir=="":
			messagebox.showerror("ERROR..","Please select an output directory to save the result..")
		else:

			temp()
		
	def end():
		en()
		top.destroy()
	def bid():
		global submit, names,ext
		if submit!=0:
			submit=0
			names=[]
			ext=[]	
			
		def workon():
			
			for a in names:
				if a.lower().endswith(('jpg','jpeg','png','tiff','gif')):
					ext.append(1)
				else:
					ext.append(0)
			for a in range(len(names)):
				if ext[a]:
					lab=Label(framm0,text=names[a]).grid(row=a,column=0,sticky=N+S+W+E)
				else:
					lab=Label(framm0,text=names[a],fg="red").grid(row=a,column=0,sticky=N+S+W+E)
		while True:
			files=filedialog.askopenfilename()
			if not files: break
			names.append(files)
		workon()
	def out():
		global out
		outdi=filedialog.askdirectory()
		out(str(outdi))
		lab=Label(framm1,text="OUTPUT DIRECTORY: "+outdir).pack()
		
	dis()

	butt0=Button(top,text="Select Images",command=bid,bg="blue",fg="white",font="bold")
	butt0.grid(row=0,column=0,padx=60,pady=50,sticky=N+S+W+E)
	butt1=Button(top,text="Select Output Directory",command=out,bg="blue",fg="white",font="bold")
	butt1.grid(row=0,column=1,padx=60,pady=50,sticky=N+S+W+E)
	framm0=Frame(top)
	framm0.grid(row=1,column=0,sticky=N+S+W+E)
	framm1=Frame(top)
	framm1.grid(row=1,column=1,sticky=N+S+W+E)
	butt2=Button(top,text="SUBMIT",command=PROCEED,bg="blue",fg="white",font="bold")
	butt2.grid(row=2,column=0,padx=60,pady=50,sticky=N+S+W+E,columnspan=2)
	extend(top,(0,4),(0,1))
	top.protocol("WM_DELETE_WINDOW", end)

#webcam
def cam():
	top = Toplevel()
	top.title("WEBCAM")
	gpu=var.get()
	def out():
		global out
		outdi=filedialog.askdirectory()
		out(str(outdi))
		lab=Label(top,text="OUTPUT DIRECTORY: "+outdir).grid(row=1,column=0,columnspan=2)
	
	def bid():
		global outdir
		#diss()
		webcam.video(gpu,0.5,0.3,outdir)
	butt0=Button(top,text="START: Press q to stop once started",command=bid,bg="blue",fg="white",font="bold")
	butt0.grid(row=0,column=1,padx=60,pady=50,sticky=N+S+W+E)
	
	butt1=Button(top,text="SELECT output directory",command=out,bg="blue",fg="white",font="bold")
	butt1.grid(row=0,column=0,padx=60,pady=50,sticky=N+S+W+E)
	
	


#video
def vid():
	top = Toplevel()
	gpu=var.get()
	global Rad1,Rad0 ,dis,en,extend,names,submit
	
	
	def temp():
		print("[INFO] GPU IS >>"+ str(gpu))
		realList=[]
			
		for a in range(len(names)):
			if ext[a]:
				realList.append(names[a])
			else:
				continue
			
		
		one.video(realList,gpu,0.5,0.3,outdir)  #video(list1,gpu,confidence,thresh,outpath)
		
		lab=Label(top,text="SAVED SUCCESSFULLY...")
		lab.grid(row=4,column=0,sticky=N+S+W+E,columnspan=2)
	
	def PROCEED():
		global outdir, submit
		submit=1
		
		if outdir=="":
			messagebox.showerror("ERROR..","Please select an output directory to save the result..")
		else:

			temp()
		
	def end():
		en()
		top.destroy()
	def bid():
		global submit, names,ext
		if submit!=0:
			submit=0
			names=[]
			ext=[]	
			
		def workon():
			
			for a in names:
				if a.lower().endswith(('mp4','mov','wmv','flv','avi','webm','mkv')):
					ext.append(1)
				else:
					ext.append(0)
			for a in range(len(names)):
				if ext[a]:
					lab=Label(framm0,text=names[a]).grid(row=a,column=0,sticky=N+S+W+E)
				else:
					lab=Label(framm0,text=names[a],fg="red").grid(row=a,column=0,sticky=N+S+W+E)
		while True:
			files=filedialog.askopenfilename()
			if not files: break
			names.append(files)
		workon()
	def out():
		global out
		outdi=filedialog.askdirectory()
		out(str(outdi))
		lab=Label(framm1,text="OUTPUT DIRECTORY: "+outdir).pack()
		
	top.title("WORK ON videos")
	dis()
	butt0=Button(top,text="SELECT VIDEOS",command=bid,bg="blue",fg="white",font="bold")
	butt0.grid(row=0,column=0,padx=60,pady=50,sticky=N+S+W+E)
	butt1=Button(top,text="SELECT Output Directory",command=out,bg="blue",fg="white",font="bold")
	butt1.grid(row=0,column=1,padx=60,pady=50,sticky=N+S+W+E)
	framm0=Frame(top)
	framm0.grid(row=1,column=0,sticky=N+S+W+E)
	framm1=Frame(top)
	framm1.grid(row=1,column=1,sticky=N+S+W+E)
	
	butt2=Button(top,text="SUBMIT",command=PROCEED,bg="blue",fg="white",font="bold")
	butt2.grid(row=2,column=0,padx=60,pady=50,sticky=N+S+W+E,columnspan=2)
	extend(top,(0,4),(0,1))
	
	
	
	
	top.protocol("WM_DELETE_WINDOW", end)

#frame1

extend(frame1,(0,2),(0,2))
#BUTTONS

ima1=PhotoImage(file="images.png")
ima2=PhotoImage(file="videos.png")
ima3=PhotoImage(file="webcam.png")

but0=Button(frame1,image=ima1,command=img,fg="white",bg="white")
but0.grid(row=0,column=0,padx=60,pady=50,sticky=N+S+W+E)
but1=Button(frame1,image=ima2,command=vid,fg="white",bg="white")
but1.grid(row=0,column=1,padx=60,pady=50,sticky=N+S+W+E)
but2=Button(frame1,image=ima3,command=cam,fg="white",bg="white")
but2.grid(row=0,column=2,padx=60,pady=50,sticky=N+S+W+E)




root.mainloop()

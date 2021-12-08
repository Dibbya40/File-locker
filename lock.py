import Tkinter
import tkFileDialog
from Tkinter import *
root = Tk()
from Crypto.Cipher import AES
iv = 16 * '\x00'           # Initialization vector: discussed later
mode = AES.MODE_CBC
key = '0123456789abcdef'
my_file = tkFileDialog.askopenfilename()
import os, random, struct
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

i=0
user = input("Number of users: ")
algo = input("Choose algorithm\n 1) RSA   2)AES  : ")
import time
import sys
import getpass

database = [   ]

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.e' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.e'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
    os.remove(in_filename) 

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
            
    os.remove(in_filename) 




def encrypt(file, public_key):
    read_size = 128
    with open(file, 'rb') as original_file:
        e_file = file + '.e'
        with open(e_file, 'wb') as encrypted_file:
            while True:
                file_part = original_file.read(read_size)

                if len(file_part) == 0:
                    break
                cipher = PKCS1_OAEP.new(public_key)
                encrypted_file.write(cipher.encrypt(file_part)) 
                

    os.remove(file) 
    
def decrypt(file, private_key):
    read_size = 128
    with open(file, 'rb') as encrypted_file:
        d_file = file[:-2]
        with open(d_file, 'wb') as decrypted_file:
            while True:
                file_part = encrypted_file.read(read_size)

                if len(file_part) == 0:
                    break
                original = PKCS1_OAEP.new(private_key)
                decrypted_file.write(original.decrypt(file_part))

    os.remove(file)

    

 
def Signup(): # This is the signup definition, 
    global i
    i+=1
    global pwordE # These globals just make the variables global to the entire script, meaning any definition can use them
    global nameE
    global roots
 
    roots = Tk() # This creates the window, just a blank one.
    roots.title('Signup') # This renames the title of said window to 'signup'
    intruction = Label(roots, text='Enter information for file encryption\n') # This puts a label, so just a piece of text saying 'please enter blah'
    intruction.grid(row=0, column=0, sticky=E) # This just puts it in the window, on row 0, col 0. If you want to learn more look up a tkinter tutorial :)
 
    nameL = Label(roots, text='New Username: ') # This just does the same as above, instead with the text new username.
    pwordL = Label(roots, text='New Password: ') # ^^
    nameL.grid(row=1, column=0, sticky=W) # Same thing as the instruction var just on different rows. :) Tkinter is like that.
    pwordL.grid(row=2, column=0, sticky=W) # ^^
 
    nameE = Entry(roots) # This now puts a text box waiting for input.
    pwordE = Entry(roots, show='*') # Same as above, yet 'show="*"' What this does is replace the text with *, like a password box :D
    nameE.grid(row=1, column=1) # You know what this does now :D
    pwordE.grid(row=2, column=1) # ^^
 
    signupButton = Button(roots, text='Signup', command=FSSignup) # This creates the button with the text 'signup', when you click it, the command 'fssignup' will run. which is the def
    signupButton.grid(columnspan=2, sticky=W)
    roots.mainloop() # This just makes the window keep open, we will destroy it soon
 
def FSSignup():
   
    database.append( (nameE.get(), pwordE.get()) )
    
    
    roots.destroy() # This will destroy the signup window. :)
   ##### Login() # This will move us onto the login definition :D
 
def Login():
    global nameEL
    global pwordEL # More globals :D
    global rootA
 
    rootA = Tk() # This now makes a new window.
    rootA.title('Login') # This makes the window title 'login'
 
    intruction = Label(rootA, text='Please login to decrypt file \n') # More labels to tell us what they do
    intruction.grid(sticky=E) # Blahdy Blah
 
    nameL = Label(rootA, text='Username: ') # More labels
    pwordL = Label(rootA, text='Password: ') # ^
    nameL.grid(row=1, sticky=W)
    pwordL.grid(row=2, sticky=W)
 
    nameEL = Entry(rootA) # The entry input
    pwordEL = Entry(rootA, show='*')
    nameEL.grid(row=1, column=1)
    pwordEL.grid(row=2, column=1)
 
    loginB = Button(rootA, text='Login', command=CheckLogin) # This makes the login button, which will go to the CheckLogin def.
    loginB.grid(columnspan=2, sticky=W)
 
    
    rootA.mainloop()
 
def CheckLogin():
    
    #if nameEL.get() == uname and pwordEL.get() == pword: # Checks to see if you entered the correct data.
     if (nameEL.get(), pwordEL.get()) in database:
        if algo == 1:
         decrypt(my_file + '.e', private_key)
        else:
         decrypt_file(key, my_file + '.e', out_filename=None, chunksize=24*1024)   
        r = Tk() # Opens new window
        r.title('Welcome')
        r.geometry('200x100') # Makes the window a certain size
        rlbl = Label(r, text='\nFile successfully decrypted !!') # "logged in" label
        rlbl.pack() # Pack is like .grid(), just different
        r.mainloop()
     else:
        r = Tk()
        r.title('Sorry')
        r.geometry('200x100')
        rlbl = Label(r, text='\n Invalid Login')
        rlbl.pack()
        r.mainloop()
 

 
private_key = RSA.generate(1024)
public_key = RSA.importKey(private_key.publickey().exportKey())



if algo == 1:
 encrypt(my_file, public_key) 
 while i < user:
   Signup()
 Login()
 
else: 
 encrypt_file(key, my_file, out_filename=None, chunksize=64*1024)
 while i < user:
   Signup()
 Login()

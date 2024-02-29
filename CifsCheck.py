import logging
from smbclient import listdir, mkdir, register_session, rmdir, scandir 
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import ftplib
import ftputil

app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

readDirector=rf"\\192.168.1.\t"
readftp="192.168.1."

# Optional - register the server with explicit credentials
register_session(readDirector, "pcName", "password") 

@app.get("/")
def read_root():          
    readDir = read_dir(readDirector)    
    # print(readDir,"readDir")
    return {"Hello": readDir}

@app.get("/ftp")
def read_Rootftp():          
    readDir = read_ftp(readftp)    
    # print(readDir,"read_Rootftp")
    return {"Hello": readDir}


def read_dir(readDirector):     
        items = scandir(readDirector)
        result = [] 
        
        for file_info in items:
            # file_inode = file_info.inode()
            itemPath = os.path.join(readDirector,file_info.name) 
            if file_info.is_dir():      
                # print(itemPath)
                childDirectory = read_dir(itemPath);           
                result.append(
                    {
                        'value': itemPath,
                        'label': file_info.name,
                        'type': 'directory', 
                        'children':childDirectory
                    })
            else: 
                result.append({ "value": itemPath, "type": 'file', "label": file_info.name }) 
        return result

def read_ftp(fname):
    # files = []
    filecheck=[]
    # ftp = ftplib.FTP(readftp,'engineering4','saurabhi')
    # try:
    #     files = ftp.nlst()
    # except ftplib.error_perm as resp:
        # if str(resp) == "550 No files found":
        #     print("No files in this directory")
        # else:
        #     raise

    with ftputil.FTPHost(readftp,"pcName", "password") as ftp_host:  
        # ftp_host.chdir("/{fname}/")       
        list = ftp_host.listdir(ftp_host.curdir)
        for fname in list:
            itemPath = os.path.join(readftp,fname)   
            if ftp_host.path.isdir(fname):           
                # childDirectory = ftp_host.chdir("/{fname}/") 
                print(itemPath + " is a directory")
                filecheck.append(
                    { 
                        "value":itemPath,
                        'label': fname,
                        'type': 'directory',   
                        # 'children':childDirectoryd
                    })
            else:
                print(fname + " is not a directory")
                filecheck.append({ "value": itemPath, "type": 'file', "label": fname }) 

    # for f in files:
    #     itemPath = os.path.join(readftp,f)   
    #     print(f.is_,"itema")
    #     filecheck.append(
    #                 { 
    #                     "value":itemPath,
    #                     'label': f,
    #                     'type': 'directory',  
    #                 })

    # print(filecheck,"files")
    # ftp.quit()      
    return filecheck
        
    

uvicorn.run(app)


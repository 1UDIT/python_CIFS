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

@app.get("/ftp")
def read_Rootftp():          
    readDir = read_ftp()    
    # print(readDir,"read_Rootftp")
    return {"Hello": readDir}



# @app.get("/ftp/{ftp_id}")
# def read_Rootftp(ftp_id):          
#     # ftpDir = read_ftp(ftp_id)    
#     print(ftp_id,"ftp_id")
#     return {"Hello": ftp_id}


def read_ftp():
    filecheck=[] 
    with ftputil.FTPHost(readftp,"pcName", "password") as ftp_host:
        # ftp_host.chdir("/{fname}/")       
        list = ftp_host.listdir(ftp_host.curdir)
        for fname in list:
            itemPath = os.path.join(readFtpIp,fname)   
            if ftp_host.path.isdir(fname):           
                childDirectory = readFtp_dir(rf"/{fname}/")  
                filecheck.append(
                    { 
                        "value":f"{readFtpIp+chr(92)+fname}",
                        'label': fname,
                        'type': 'directory',   
                        'children':childDirectory
                    })
            else: 
                filecheck.append({ "value": f"{readFtpIp+chr(92)+fname}", "type": 'file', "label": fname }) 
    return filecheck

def readFtp_dir(Dir_Name):
    # print(Dir_Name,"Dir_Nane")
    filecheck=[]
    with ftputil.FTPHost(readftp,"pcName", "password") as ftp_host:
    items.chdir(Dir_Name) 
    list = items.listdir(items.curdir) 
    for file_info in list: 
         # file_inode = file_info.inode()
            itemPath = os.path.join(readFtpIp,file_info)
            changePath = os.path.join(Dir_Name,file_info)
            if items.path.isdir(file_info):      
                # log.error("childDirectory error")      
                childDirectory = readFtp_dir(changePath); 
                # print(readFtpIp,changePath,'isdir')    
                filecheck.append(
                    {
                        'value': f"{readFtpIp+changePath}",
                        'label': file_info,
                        'type': 'directory', 
                        'children':childDirectory
                    })
            else:  
                filecheck.append({ "value": f"{readFtpIp+changePath}", "type": 'file', "label": file_info }) 
    return filecheck 

        
    

uvicorn.run(app)


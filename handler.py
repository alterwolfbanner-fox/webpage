import os
import shutil
import asyncio
from pymegatools import Megatools, MegaError

class Handler():
    def __init__(self):
        self.path = './'
    
    async def handler(self, command):
        if command == 'ls':
            data = await self.list_dir()
            return data
        elif command == 'dir':
            return await self.directory() 
        elif 'cd' in command:
            destpath = command.split('cd ')[-1]
            return await self.move_into_directory(destpath)
        elif 'rname' in command:
            names = command.split(' ')
            old_name = names[1]
            new_name = names[2]
            return await self.rename(old_name, new_name)
        elif 'cp' in command:
            data = command.split(' ')
            file = data[1]
            destpath = data[2]
            return await self.copy(file, destpath)
        elif 'mv' in command:
            data = command.split(' ')
            file = data[1]
            destpath = data[2]
            return await self.move(file, destpath)
        elif 'rm' in command:
            data = command.split(' ')
            file = data[1]
            return await self.delete(file)
        elif 'sub' in command:
            data = command.split(' ')
            file = data[1]
            return await self.ffmpeg_command(file)
        elif 'enc' in command:
            data = command.split(' ')
            file = data[1]
            return await self.encode_ffmpeg(file)
        elif 'dl' in command:
            data = command.split(' ')
            url = data[1]
            return await self.DownloadMega(url)
    
    async def list_dir(self):
        lista = os.listdir()
        return sorted(lista)
    
    async def directory(self):
        return [os.getcwd()]
    
    async def move_into_directory(self, destpath):
        actualpath = await self.directory()
        if destpath == '..':
              data = actualpath[0].split('\\')
              data.pop(-1)
              data = "\\".join(data)
              os.chdir(data)
              return await self.directory()
        os.chdir(actualpath[0]+'\\'+destpath)
        return await self.directory()
    
    async def rename(self, old_name, new_name):
        os.rename(old_name, new_name)
        return ["File name has been changed", await self.list_dir()]
    
    async def copy(self, file, destpath):
        shutil.copy("lol.txt", "templates/lol.txt")
        return [f'File/Folder has been copied to {destpath}']
    
    async def move(self, file, destpath):
        shutil.move("lol.txt", "templates")
        return [f'File/Folder has been moved to {destpath}']
    
    async def delete(self, file):
        os.remove(file)
        return [f"File/Folder {file} has been removed from directory."]
    
    async def extract_sub(self, file):
        n_subs = 0
        cmd = ""
        result = ""
        #cmd = "ffmpeg -i tururu.mkv -map 0:s:{nsub} subs[{nsubs}].srt"
        #cmd  = "ffmpeg -i tururu.mkv -map 0:s subs_%d.srt"
        while True:
            if n_subs == 15:
                break            
            result = await run_command(f"ffmpeg -i seija07.mkv -map 0:s:{n_subs} subs[{n_subs}].srt")
            n_subs += 1
        return [f"Subtitle files extracted!"]
    
    async def encode_ffmpeg(self, file):
        result = await run_command(f'ffmpeg -i "Sugar Apple Fairy Tale Part 2 - 08 (20) [720p].mkv" -c:v libx265 -crf 32 output.mp4')
        print(result)
        return ["File encoded!"]
    
    async def DownloadMega(self, url):
        print("entered")
        mega = Megatools()
        print(mega)
        #file_name = mega.filename(url)
        #print(file_name)
        if not os.path.exists('./downloads'):
            os.mkdir('./downloads')
        try:
            # os.chdir(f"./downloads")
            print("Iniciando descarga")
            await mega.download(url, assume_async=True, path='./downloads')#progress=prog.megaprogress, progress_arguments=(msg, start_time), path="./downloads")
            return ['downloaded']
        except MegaError as ex:
            print("Error: ", str(ex))


async def run_command(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return stdout.decode().strip(), stderr.decode().strip()
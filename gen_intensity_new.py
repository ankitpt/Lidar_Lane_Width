import time

start = time.time()

import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import itertools
from PIL import ImageFilter


def getEquidistantPoints(p1, p2, parts):
    
    
    return zip(np.linspace(p1[0], p2[0], parts+1), np.linspace(p1[1], p2[1], parts+1))

def print_point_density(loc,rows,cols,size,cell_siz,num):
    
    os.chdir("//myhome.itap.purdue.edu/myhome/pate1019/ecn.data/Desktop/DPRG_ECN/Pt_density")

    from random import randint
    temp=int(size/cell_siz)
    m=randint(0, rows-temp)
    n=randint(0,cols-temp)

    m_list=range(m,m+temp)
    n_list=range(n,n+temp)
    count=0
    for i in m_list:
        for j in n_list:
            try:
                count=count+len(loc[i,j])
            except:
                
                continue
    print("Point density in point_cloud " ,num, "between locations ",m,n,"and ",i,j,"is, ",count/size,"pts/m^2 \n",file=open("output.txt", "a"))
    


def point_to_image(filename,num,trj,tile):

#Reading the point cloud file
    data=np.zeros([500000,7])

    k=-1

    with open(filename) as infile:
        
        for line in infile:
            
            if(k==-1):
                k=k+1
                continue
        
            line=line.strip('\n').split(' ')
            line=[float(c) for c in line]
            data[k,:]=line
            k=k+1
    
    data=data[0:k,:]
#Finding bounds of the file    
    x_min=np.min(data[:,0])
    x_max=np.max(data[:,0])
    y_min=np.min(data[:,1])                  #tile_25_news_000006
    y_max=np.max(data[:,1])
   # plt.scatter(data[:,0],data[:,1])
    data[:,5]=np.where(data[:,5] > 25, 255, 0)
    #data[:,5]=np.interp(data[:,5], (0, 50), (0, 255))
    #intens=data[:,5]
    #intens[intens < 127] = 0
    #data[:,5]=intens
    cell_siz=0.05

    cols=int((x_max-x_min)/cell_siz)+1
    rows=int((y_max-y_min)/cell_siz)+1
    
    print("No. of rows in this file ",rows)
    print("No. of columns in this file ",cols)

    img=np.zeros([rows,cols])
    
    
    #Finding points falling in a grid cell
    k=0
    loc=dict()
    for pt in data:
        
        x=pt[0]
        y=pt[1]
        
        j=int((x-x_min)/cell_siz)
        i=int((y-y_min)/cell_siz)
        
        loc.setdefault((i,j),[]).append(k)
        k=k+1
   
    cnt=0;    
    for i in range(rows):
        
        for j in range(cols):
            
              try:
                data2=data[loc[i,j]]
                val=np.mean(data2[:,5])
                img[i,j]=val
                cnt=cnt+1
              except:
              
               continue
            
    nfilename=str(num)+".png"
    nfilename2=str(num)+".png"
    
    #Finding trajectory points in this pt cloud file
    img_l=np.zeros([rows,cols])
    
    for j in range(trj.shape[0]):
        
        x=trj[j,0]
        y=trj[j,1]
        #print(x_min,x,x_max)
        #print(y_min,y,y_max)
        if(x_min<x<x_max and y_min<y<y_max):
            
            print("trj found")
            j=int((x-x_min)/cell_siz)
            i=int((y-y_min)/cell_siz)
            img_l[i,j]=255
    
   
    os.chdir("C:/Users/17657/Desktop/DPRG/unet-master/unet-master/data/membrane/test")
    
    img2 = Image.fromarray(img.astype(np.uint8))
    img_l = Image.fromarray(img_l.astype(np.uint8))
    
    #img2=img2.filter(ImageFilter.SMOOTH)
    
    img2 = img2.resize((256,256))
    img_l = img_l.resize((256,256))
    
    img2=img2.rotate(180)
    img2.transpose(Image.FLIP_LEFT_RIGHT).save(nfilename,"PNG")
    
    img_l=img_l.rotate(180)
    
    sfx=cols/256
    sfy=rows/256
    
   # plt.imsave(nfilename, img2, cmap='gray')
    print("Image saved,",nfilename)
    
    os.chdir("C:/Users/17657/Desktop/DPRG")
    #os.chdir("//myhome.itap.purdue.edu/myhome/pate1019/ecn.data/Desktop/DPRG_ECN/Images_"+tile+"_trj")
    img_l.transpose(Image.FLIP_LEFT_RIGHT).save(nfilename,"PNG")
    os.chdir("C:/Users/17657/Desktop/DPRG/georef")
    print( x_min,y_min,x_max,y_max,file=open("georef_"+tile+".txt", "a"))
    os.chdir("C:/Users/17657/Desktop/DPRG/sf")
    print( sfx,sfy,file=open("sf_"+tile+".txt", "a"))
    os.chdir("C:/Users/17657/Desktop/DPRG/Point_Cloud_"+tile)
    
    #return loc




k=0
trj=np.zeros((10000,4))

#reading trajectory file



tile="12"

if os.path.exists("C:/Users/17657/Desktop/DPRG/sf/sf_"+tile+".txt"):
  os.remove("C:/Users/17657/Desktop/DPRG/sf/sf_"+tile+".txt")
else:
  pass

if os.path.exists("C:/Users/17657/Desktop/DPRG/georef/georef_"+tile+".txt"):
  os.remove("C:/Users/17657/Desktop/DPRG/georef/georef_"+tile+".txt")
else:
  pass


with open("export_Mission 1 - Cloud_"+tile+".txt") as infile:
    
    for line in itertools.islice(infile, 140386, 148832):
        
   #     if(k==-1):
    #            k=k+1
     #           continue
        
        line=line.strip('\n').split(' ')
        line=[float(c) for c in line]
        line=line[0:4]
        trj[k,:]=line
        k=k+1

#trj=trj[:,1:3]
trj=trj[~np.all(trj == 0, axis=1)]


        
#for transformed traj
trj=trj[:,0:2]
#trj=trj[:,0:2]
#row_trj=trj.shape[0]
#col_trj=trj.shape[1]
#one=np.ones((row_trj,1))
#trj=np.append(trj,one,1)

#mat=open("tfm_19.mat.txt","r")
#tfm=np.zeros((4,4))
#k=0
#for line in mat:
  #   line=[float(c) for c in line]
#    tfm[k,:]=line
#    k=k+1

#tfm=np.delete(tfm,2,0)
#tfm=np.delete(tfm,2,1)
#trj=np.dot(tfm,trj.T)
#trj=trj.T
#trj=trj[:,0:col_trj]
#trj=trj[1248:1290,0:2]
#trj2=np.zeros([500,2])


#getting interpolated trajectory points
#for j in range(trj.shape[0]-1):
        
 #       p1=trj[j]
  #      p2=trj[j+1]
    
   #     trj2[10*j+j:10*(j+1)+j+1,:]=np.array(list(getEquidistantPoints(p1, p2, 10)))
        
#trj2=trj2[~np.all(trj2 == 0, axis=1)]




os.chdir("C:/Users/17657/Desktop/DPRG/Point_Cloud_"+tile)

directory = os.fsencode("C:/Users/17657/Desktop/DPRG/Point_Cloud_"+tile)
filelist=os.listdir(directory)
filelist = sorted(filelist,key=lambda x: int(os.path.splitext(x)[0][-2:]))



j=0;
#loc_list=list()
    
   

for file in filelist:
    
    filename = os.fsdecode(file)
    print("Processing file ",filename)
    point_to_image(filename,j,trj,tile)
    j=j+1




end = time.time()
print(end - start)


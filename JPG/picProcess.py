import re
from PIL import Image
import numpy as np

def getFileName():
    print("Place the JPG file under the Same Dir")
    inp=input("Enter the fileNmae/nameDir==>: ")#IMG_1455.JPG
    # inp="IMG_1455.JPG"
    return inp
def main():
    try:
        name=getFileName()
        L=np.asarray(Image.open(name).convert('L')).astype('float')#numpy converting to 3-d array
        # print(L.shape,L.dtype)#(1500, 1500, 3) uint8====> 1500*1500(编辑)
        # print(L)像素rgb包（List）
        depth = 40.                               
        grad = np.gradient(L)    #adjacent difference
        # print(grad)
        grad_x, grad_y = grad   #x greyAdjVal 光线x作用
        grad_x = grad_x*depth/100.#y greyAdjVal 光线y作用
        grad_y = grad_y*depth/100.#z greyAdjVal 光线z作用
        A = np.sqrt(grad_x**2 + grad_y**2 + 1.)
        dim_x = grad_x/A
        dim_y = grad_y/A
        dim_z = 1./A

        ele = np.pi/2.5
        ariz = np.pi/20
        dx = np.cos(ele)*np.cos(ariz)
        dy = np.cos(ele)*np.sin(ariz)
        dz = np.sin(ele)

        afterJpg = 300*(dx*dim_x*0.2 + dy*dim_y*0.2 + dz*dim_z)
        afterJpg = afterJpg.clip(0,255) #[less 0]&[more 255] clipped to the interval edges
        new=re.findall("\w*",name)
        print(new[0]+"(edited).jpg has been Generated")
        out=Image.fromarray(afterJpg.astype('uint8'))
        out.save(new[0]+"(edited).jpg")

    except OSError as e:
        print("File not found")
        
       
if __name__ == "__main__":
    main()
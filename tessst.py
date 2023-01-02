def erosion(self):
		ERO = cv2.imread("binary_image.png",0)
		ERO[ERO > 0] = 1
		print("image:",ERO)
		img=self.erosion_fun(ERO,self.kernel_size.value())
		#img=self.conv_erosion(ERO,self.kernel_size.value())
		self.Erosion_img.canvas.axes.clear()
		self.Erosion_img.canvas.axes.imshow(img, cmap=plt .cm.gray)
		self.Erosion_img.canvas.draw()
		

def dilation(self):
    DIL = cv2.imread("binary_image.png",0)
    DIL[DIL > 0] = 1
    img=self.dilation_fun(DIL,self.kernel_size.value())
    #img=self.conv_dilation(DIL,self.kernel_size.value())
    self.Dilation_img.canvas.axes.clear()
    self.Dilation_img.canvas.axes.imshow(img, cmap=plt .cm.gray)
    self.Dilation_img.canvas.draw()

def opening_fun(self):
    #erosion then dilation	
    OPE = cv2.imread("binary_image.png",0)
    OPE[OPE > 0] = 1
    img=self.erosion_fun(OPE,self.kernel_size.value())
    img1=self.dilation_fun(img,self.kernel_size.value())
    #img=self.conv_erosion(OPE,self.kernel_size.value())
    #img1=self.conv_dilation(img,self.kernel_size.value())
    self.Opening_img.canvas.axes.clear()
    self.Opening_img.canvas.axes.imshow(img1, cmap=plt .cm.gray)
    self.Opening_img.canvas.draw()

def closing_fun(self):
    #dilation then erosion
    CLO = cv2.imread("binary_image.png",0)
    CLO[CLO > 0] = 1
    img=self.dilation_fun(CLO,self.kernel_size.value())
    img1=self.erosion_fun(img,self.kernel_size.value())
    #img=self.conv_dilation(CLO,self.kernel_size.value())
    #img1=self.conv_erosion(img,self.kernel_size.value())
    
    self.Closing_img.canvas.axes.clear()
    self.Closing_img.canvas.axes.imshow(img1, cmap=plt .cm.gray)
    self.Closing_img.canvas.draw()

def erosion_fun(self,image,kernel):
    m,n= image.shape
    SE= np.ones((kernel,kernel), dtype=np.uint8)
    q=kernel-1
    SE[0][0]=0
    SE[0][q]=0
    SE[q][0]=0
    SE[q][q]=0
    constant= (kernel-1)//2
    imgErode= np.zeros((m,n), dtype=np.uint8)
    for i in range(constant, m-constant):
        for j in range(constant,n-constant):
            temp= image[i-constant:i+constant+1, j-constant:j+constant+1]
            product= temp*SE
            #changing 
            product=np.array(product)
            SE=np.array(SE)
            if ((product==SE).all()==True): #True means they are similar
                imgErode[i,j]= 1
            else: 
                #print("false")
                imgErode[i,j]= 0
    return imgErode
def dilation_fun(self,image,kernel):
    #Acquire size of the image
    m,n= image.shape 
    # Define the structuring element
    SE= np.ones((kernel,kernel), dtype=np.uint8)
    q=kernel-1
    SE[0][0]=0
    SE[0][q]=0
    SE[q][0]=0
    SE[q][q]=0
    print("SE:",SE)
    constant= (kernel-1)//2
    #Define new image
    imgDilate= np.zeros((m,n), dtype=np.uint8)
    #Dilation operation without using inbuilt CV2 function
    for i in range(constant, m-constant):
        for j in range(constant,n-constant):
            temp= image[i-constant:i+constant+1, j-constant:j+constant+1]
            product= temp*SE
            imgDilate[i,j]= np.max(product)

    return imgDilate


def filter_fun(self):
    #opening 
    #EROSION
    #DILATION

    #closing
    #DILATION
    #EROSION

    image = cv2.imread("binary_image.png",0)
    image[image > 0] = 1
    m,n= image.shape 
    # Define the structuring element
    SE= np.ones((3,3), dtype=np.uint8)
    print("SE:",SE)
    constant= (3-1)//2
    #Define new image
    imgErode= np.zeros((m,n), dtype=np.uint8)
    #Erosion 
    for i in range(constant, m-constant):
        for j in range(constant,n-constant):
            temp= image[i-constant:i+constant+1, j-constant:j+constant+1]
            product= temp*SE
            imgErode[i,j]= np.min(product)

    #dilation
    M,N= imgErode.shape 
    # Define the structuring element
    SED= np.ones((3,3), dtype=np.uint8)
    #SED[0][0]=0
    #SED[0][2]=0
    #SED[2][0]=0
    #SED[2][2]=0
    print("SED:",SED)
    constant1= (3-1)//2
    #Define new image
    imgDilute= np.zeros((M,N), dtype=np.uint8) 
    for x in range(constant1, M-constant1):
        for y in range(constant1,N-constant1):
            temp1= imgErode[x-constant1:x+constant1+1, y-constant1:y+constant1+1]
            product1= temp1*SED
            imgDilute[x,y]= np.max(product1)


    C,V= imgDilute.shape 
    # Define the structuring element
    SED2= np.ones((3,3), dtype=np.uint8)
    #SED2[0][0]=0
    #SED2[0][2]=0
    #SED2[2][0]=0
    #SED2[2][2]=0
    print("SED2:",SED2)
    constant3= (3-1)//2
    #Define new image
    imgDilute1= np.zeros((C,V), dtype=np.uint8) 
    for l in range(constant3, C-constant3):
        for k in range(constant3,V-constant3):
            temp3= imgDilute[l-constant3:l+constant3+1, k-constant3:k+constant3+1]
            product3= temp3*SED2
            imgDilute1[l,k]= np.max(product3)

    #Erosion
    c,v= imgDilute1.shape 
    # Define the structuring element
    SEE= np.ones((3,3), dtype=np.uint8)
    print("SEE:",SEE)
    constant2= (3-1)//2
    #Define new image
    imgErode1= np.zeros((c,v), dtype=np.uint8) 
    for X in range(constant2, m-constant2):
        for Y in range(constant2,n-constant2):
            temp2= imgDilute1[X-constant2:X+constant2+1, Y-constant2:Y+constant2+1]
            product2= temp2*SEE
            imgErode1[X,Y]= np.min(product2)


    


    self.Filter_img.canvas.axes.clear()
    self.Filter_img.canvas.axes.imshow(imgErode1, cmap=plt .cm.gray)
    self.Filter_img.canvas.draw()
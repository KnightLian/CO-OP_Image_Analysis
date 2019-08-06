#Appendix C: Python Code for Analyzing Impact Module Images

import Image                            #Image Libraries
import ImageOps
import ImageFilter
import ImageDraw
import ImageFont
import glob, os
import csv
import time
from pylab import * 
from matplotlib import pyplot, mpl

startTime = time.time()                 #record start time 
frame = 100000

calibA =  - 0.90877/2                   #pressure constant
calibB = (9.73896/16.5)/2               #pressure constant
calibC = - (2.52623/(16.5*16.5))/2      #pressure constant
calibD = - (0.93144/16.5)/2             #pressure constant

calibE = 13*(13/16.5)/2                 #load constant

#slice define-------------------------------------------------------------------------------
boxS = (33,2027)                      #define slice size
widthS = int(boxS[0])                 #with of slice
highS = boxS[1]                       #height of slice
boxR = 0                              #rotation angle of image segment
section =67                           #the number of slice
boxO= []                              #define slices' left top location on original image
startPoint = (263,14)                 #the start point for cut slice on image 
for j in range(section):              #for make boxO tuple
    v = startPoint[0]+boxS[0]*j
    w = (v,startPoint[1])
    boxO.append(w)    
boxesSize = [(a[0], a[1], a[0]+boxS[0], a[1]+boxS[1]) for a in boxO]#define slices' detailed location on image
#---------------------------------------------------------------------------------------------------

for infile in glob.glob("C:\\Documents and Settings\\lili\\Desktop\\test\\resizedPana\\*.jpg"): #address of open images
    filepath, filename = os.path.split(infile)                                                  #give file path and name
    filename, ext = os.path.splitext(filename)                                                  #give extension
    
    #original image bad position covert to 0-------------------------------------------------
    im = Image.open(infile)                        #open image
    im.paste(0,(617*2-17,471*2,659*2,507*2))       #black center box
    im.paste(0,(188*2,469*2,245*2,507*2))          #black left box
    im.paste(0,(1036*2,470*2,1093*2,506*2))        #black right box
    im.paste(0,(620*2,35*2,660*2,92*2))            #black top box
    im.paste(0,(620*2,883*2,660*2,941*2))          #black bottom box
    im.paste(0,(1266,0,1301,943))                  #black up pipe
    im.paste(0,(0,475*2+9,188*2,496*2+9))          #black left pipe
    im.paste(0,(1093*2,486*2-11,2560,505*2-11))    #black right pipe
    im.paste(0,(644*2-25,941*2,663*2-25,2048))     #black bottom pipe
    im.show()
    #------------------------------------------------------------------------------------------

    cmlist = [[] for i in range(len(boxO))]             #define for hold pressure result
    sumHold = []
    areaHold =[]
    avePre =[]
    cnt = 1#define a counter
    holdOriginal = Image.new('RGB', (1240*2, 1017*2-7)) #make a big holder for hold all cut slice
    
    for p in range(0,len(boxO)):
        hold = Image.new('RGB', ((boxS[0]), (boxS[1]))) #make a holder for hold each cut slice
        region = im.rotate(boxR, resample=2)            #rotate image
        region = ImageOps.grayscale(region)             #gray scale the input image covert intensity to single value
        
        edge = region.crop(boxesSize[p])                #cut slice from image
        hold.paste(edge,(0, 0))                         #put slice in hold

#!@#$%^&~~~~~~~~~~~~~~~~~~ edges measurement ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        width,height = edge.size                                       #get the size of the image
        data = list(edge.getdata())                                    #convert image to list of values

        for n in range(height/(height/highS)):                         #loop for run each vertical pixel
            first = 0
            last = 0
            tempsum = 0
            nonzerohold = []
            rge_htx = (0 + (height/highS)*n)
            rge_hty = ((height/highS) + (height/highS)*n)
            temp = [0]*width                                           #define 0 tuple with the slice width
            
            for j in range(width):                                     #loop for covert array to matrix
                for k in range(rge_htx,rge_hty):                       #loop for run from rge_htx to rge_hty
                    temp[j] += float(data[k*width+j])/(height/highS)   #covert 0 in temp to hold the value in matrix
                tempsum += temp[j]*j                                   #give sum of one row
                if temp[j] != 0:
                    nonzerohold.append(temp[j])
                    
            #define the middle line----------------------------------------------------------
            if max(temp)<8 or len(nonzerohold)<2:
                tempwidth = width/2                 #middle point is the middle of slice
            else:        
                tempwidth = tempsum/(sum(temp))     #middle point is vary
                if int(tempwidth)  < 1 :
                    tempwidth = width/2
            #----------------------------------------------------------------------------------
            
            #look for edges--------------------------------------------------------------------  
            peak1 = int(max(temp[0:int(tempwidth)])*1)         #lightest point on left edge
            peak2 = int(max(temp[int(tempwidth):-1])*1)        #lightest point on right edge  
                 
            if peak1 >= 9 and peak2 >=9:                       #tried to avoid the bubble(can be changed)
                
                for k in range(0, int(tempwidth)):             #find left edge
                    if peak1 == temp[k]:                       #find the location of peak1
                        first= k
                        break
                for k in range(width-1, int(tempwidth), -1):   #find right edge
                    if peak2 == temp[k]:                       #find the location of peak2
                        last= k
                        break
            #-----------------------------------------------------------------------------------  
                      
                pixelwidth = (last-first)                                                      #give the object width in pixel
                cmwidth = (calibA + calibB*pixelwidth + calibC *pixelwidth *pixelwidth)/(1+ calibD* pixelwidth)#calculate the pressure
                
                if first == 0 or last == 0:
                    cmlist[p].append(0)
                else:
                    cmlist[p].append(cmwidth)                                                  #hold the pressure result for draw figure image later
                    avePre.append(cmwidth)                                                     #hold the pressure result for calculate the pressure average later
                    areaHold.append(pixelwidth)                                                #hold the width in pixel for calculate the area later
                    
                draw = ImageDraw.Draw(hold)                                                    #draw line on slice
                draw.line(((first,rge_htx), (first,rge_hty)),fill=(0,255,1),width=1)           #draw left edge line
                draw.line(((last,rge_htx),(last,rge_hty)),fill=(198,29,24),width=1)            #draw right edge line
                draw.line(((tempwidth,rge_htx), (tempwidth,rge_hty)),fill=(255,255,0),width=1) #draw middle line
            else:
                 cmlist[p].append(0)

            for m in range(len(cmlist[p])):                                                    #convert negative values to 0
                if cmlist[p][m] < 0:
                    cmlist[p][m] = 0
                   
        draw = ImageDraw.Draw(hold)                                                            #draw text on slice 
        draw.text((4,5),('%d' % cnt))                                                          #draw the section number for each slice
        
        sumHold.append(sum(cmlist[p]))                                                         #hold the total pressure result for one slice
        if cnt >= 90:                                                                          #maximum to run 90 section 
           break
       
        holdOriginal.paste(hold, ((boxesSize[p][0] - startPoint[0]),0))                        #copy each processed slice in big holder
        print "Done for the results of position" + "%s"%cnt + "%s"%filename                    #output on screen
        cnt +=1                                                                                #counter adding
        
    holdOriginal.save('C:\\Documents and Settings\\lili\\Desktop\\test\\figImageOrinalCombine'+"%s"%filename+'.png')#save the total slice holder
   
    
#!@#$%^&*~~~~~~~~~~~~~~~~draw figure image process~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    a = []                                                     #define for holding the maximum results
    for j in range(len(cmlist)):
        a.append(max(cmlist[j]))
    maxPress = max(a)                                          #find maximum
    averageP = average(avePre)                                 #find average
    totalAreaHold = len(areaHold)*calibE                       #find pressure area
    
    holdcombine = Image.new('RGB', (widthS*section+150, highS))#define the holder for keep figure image
    
    #figure image making process--------------------------------------------------------------------------------------------------------------------
    for j in range(len(cmlist)):
        
        listValue = cmlist[j]                                                       #define a variable stand for each array in cmlist
        resultHold = [[] for i in range(len(listValue))]                            #define a [] tuple with length of the defined variable
        imageResult =[]
        
        for i in range(len(listValue)):                                             #make each value in resultHold in a []
            resultHold[i].append(listValue[i])
        for i in range(len(listValue)):                                             #make each value in resultHold with [] have the same length as cropped slice's width
            imageResult.append(resultHold[i]*widthS)
            
        norm = mpl.colors.Normalize(0, 10)                                          #define the colorbar's range
        fig1 = pyplot.figure(figsize=(0.33,20.27))                                  #define a blank figure slice with 33*2027 dimension which has same size as the slice
        im2 = plt.figimage(imageResult, xo=0, yo=0, alpha=1, cmap=cm.jet,norm=norm) #plot the figure image
        
        string = '%s' % int(j+1)                                                    #define the dimension paste on holder 
        infile = "C:\\Documents and Settings\\lili\\Desktop\\test\\figImagetemp"    #define a file name for save
        follow = ".png"                                                             #define a extension
        figurePath = infile+follow                                                  #combine the name with extension
        
        savefig(figurePath)                                                         #save the figure slice
        clf()                                                                       #Clear the current figure
        
        imcombine1 = (Image.open(figurePath))                                       #open the figure slice
        holdcombine.paste(imcombine1, (widthS*j, 0))                                #paste the opened figure slice on holder 
        
        haha = j                                                                    #give the last j's value for defining the dimension on holder
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #colour bar making process-----------------------------------------------------------------------
    fig2 = pyplot.figure(figsize=(1.50,20.27))                                     #define the blank figure image with 150*2027 dimension
    ax1 = fig2.add_axes([0.2, 0.00,0.25, 1])                                       #the colorbar draws on 20% of the width start from left, 0% of height start from bottom, 25% fat of the width, 100% tall of the height
    cd = mpl.colorbar.ColorbarBase(ax1, cmap=cm.jet,alpha=1,
                                   norm=norm,extend='both',spacing='proportional',
                                   orientation='vertical')                         #plot colorbar 
    
    savefig(figurePath)                                                            #save the color bar
    clf()                                                                          #Clear the current figure
    
    imcombine1 = (Image.open(figurePath))
    holdcombine.paste(imcombine1, (widthS*(haha+1), 0))                            #save cropped original
    #------------------------------------------------------------------------------------------------
    
    #text write on figure image-----------------------------------------------------------------------------------------
    draw = ImageDraw.Draw(holdcombine)
    font = ImageFont.truetype("arial.ttf", 40)                                      #text with arial style with size of 40
    string1 = 'The total load = ' +'%1.2f' % (averageP*totalAreaHold/1000)+ '(kN)'  #text
    string2 = 'The total area = ' + '%1.2f' % (totalAreaHold) +'(mm^2)'             #text
    string3 = 'The average pressure = '+'%1.2f' % (averageP) + '(MPa)'              #text
    string4 = 'The max pressure = ' + '%1.2f'%(maxPress) +'(MPa)'                   #text
    draw.text((10,5), string1,font = font)                                          #write text on image
    draw.text((10,40), string2,font = font)                                         #write text on image
    draw.text((10,75), string3,font = font)                                         #write text on image
    draw.text((10,110), string4,font = font)                                        #write text on image
    #----------------------------------------------------------------------------------------------------------------------
    
    holdcombine.save('C:\\Documents and Settings\\lili\\Desktop\\test\\figImageCombinePosition '+ "%s"%filename  + '.png')#save the holder of figure image
    clf()                                                                #Clear the current figure
    
    close('all')                                                         #clean all garbage
endTime = time.time()                                                    #define end time
print 'The time of running the code (second)',  endTime-startTime        #give total time for tuning the program (150s each)

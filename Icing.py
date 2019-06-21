#Appendix A: Python Code for Analyzing Marine Icing Images

import Image                 #PIL Python Image Library
import ImageOps
import ImageFilter
import ImageDraw
import ImageFont
import glob, os
import csv
import time
from pylab import * 

frame = 100000
startTime = time.time()      #record start time 

calib = (0.68, 0.68, 0.68, 0.68, 0.68, 0.68, 0.68, 0.68, 0.68, 0.68, 0.68,
         0.466, 0.495, 0.706, 
         0.95, 0.78, 0.58)   #Calibration for each position

#position define-------------------------------------------------------------------------------------------------------
boxR = [12.6, 12.6, 12.6, 12.5, -9.5, -9.6, -9.6, -9.6, 94, 94, 94, 
        12,101,0, 
        -55, -42, -35]                               #rotation angle of image segment

boxO = [(575,350), (575,400), (575,575), (575,630),
        (950,225), (950,275), (950,425), (950,500),
        (725,1250), (725,1182), (725,1136),          #11 pole structures' dimension
        (1892,1296), (1470,158), (1157,782),         #3 eclipse structures' dimension
        (1406,1173), (1500,1393), (1580,1635)        #3 rail structures' dimension
        ]                                            #location of corner of image segment after rotation image

num = 1                                              #the number of parts for dividing the image 
position = 2                                        #the position number which we choose from 1 to 17

if position in range(1,10):                          #define the cropped size and peak percentage for position 1 to 9 
    boxS = (60,60)                                   #size is 60 pixels height, 60 pixels width
    percentage1 = 0.65                               #define the percentage of the left actual edge to the left peak value 
    percentage2 = 0.65                               #define the percentage of the right actual edge to the right peak value 
if position == 9:                                    #define the cropped size and peak percentage for position 9
    boxS = (60,40)
if position == 10:                                   #define the cropped size and peak percentage for position 10
    boxS = (60,20)
if position == 11:                                   #define the cropped size and peak percentage for position 11
    boxS = (60,25)
if position == 12:                                   #define the cropped size and peak percentage for position 12
    boxS = (140,40)#300,200)
    percentage1 = 0.6
    percentage2 = 0.6
    num = 1#only 
if position == 13:                                   #define the cropped size and peak percentage for position 13
    boxS = (90,50)
    percentage1 = 0.6
    percentage2 = 0.6
    num =1
if position == 14:                                   #define the cropped size and peak percentage for position 14
    boxS = (100,30)
    percentage1 = 0.6
    percentage2 = 0.6
    num = 1
if position == 15:                                   #define the cropped size and peak percentage for position 15
    boxS = (80, 60)
    percentage1 = 0.35
    percentage2 = 0.8
if position in range(16,18):                         #define the cropped size and peak percentage for position 16 to 17
    boxS =  (100,60)
    percentage1 = 0.25
    percentage2 = 0.80

a = boxO[position-1]                                 #convert the actual position number to computer range number
boxesSize = (a[0], a[1],a[0]+boxS[0],a[1]+boxS[1])   #define the position dimension on the big image and ready for crop
holdSize =  [ 0, 0 , boxS[0]*3+2, (boxS[1]+1)*41]    #define a hold size which is croped in big image
#-------------------------------------------------------------------------------------------------------------------------------

fof = csv.writer(open("C:\\Documents and Settings\\lili\\Desktop\\icingNum.csv", 'wb'))#define a Excel file to record result
cnt = 1                                                                                #define counter
cmlist = []                                                                            #define a holder for holding measurement 
orginalColor=[]                                                                        #define a holder to hold colored images
name = []                                                                              #define a holder to hold file name

for infile in glob.glob("C:\\Documents and Settings\\lili\\Desktop\\test\\original\\*.jpg"):#save the original images which have color
    orginalColor.append(Image.open(infile))
    name.append(infile)

hold = orginalColor[1].crop(holdSize)            #create image to hold visual results

for i in range(len(orginalColor)):               #start image analysis
    filepath, filename = os.path.split(name[i])  #give file path and file name
    filename, ext = os.path.splitext(filename)   #give file name and extension
    
    #image processing-------------------------------------------------------------------------------------
    im = orginalColor[i]                                          #open an color image

    region = im.rotate(boxR[position-1], resample=2)              #rotate image
    hold.paste(region.crop(boxesSize), (0, (boxS[1]+1)*i))        #save cropped original on holder
    region = ImageOps.grayscale(region)                           #grayscale image
    region = ImageOps.autocontrast(region, cutoff=10)             #color enhance
    region = region.filter(ImageFilter.MedianFilter(3))           #median filter for image
    region = region.filter(ImageFilter.SMOOTH)                    #smooth the image 
    region = ImageOps.autocontrast(region, cutoff=1)              #color enhance
    
    edge = region.filter(ImageFilter.MedianFilter(3))             #median filter for image
    edge = edge.filter(ImageFilter.FIND_EDGES)                    #edge detection in PIL
    edge = ImageOps.autocontrast(edge, cutoff=2)                  #color enhance   
    edge = edge.crop(boxesSize)                                   #crop the edge detected image for analyzing
    
    hold.paste(region.crop(boxesSize),(boxS[0]+1, (boxS[1]+1)*i)) #save grayscale and color enhanced cropped image 

    hold.paste(edge,((boxS[0]+1)*2, (boxS[1]+1)*i))               #save edge detected cropped image 
    #--------------------------------------------------------------------------------------------------------------

    width,height = edge.size        #get the size of the cropped image
    data = list(edge.getdata())     #convert image into list 

    first1 = []                     #define for hold measurement for left edge
    temp1 = first1
    last1 = []                      #defind for hold measurement for right edge
    temp2 = last1
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~edge measurement~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    for n in range(height/(height/num)):                          #convert the list into matrix
        rge_htx = (0 + (height/num)*n)                            #define a part of matrix from rge_htx to rge_hty
        rge_hty = ((height/num) + (height/num)*n)
        temp = [0]*width                                          #create temp to hold the intensity matrix    
            
        for j in range(width):                                    # average values for each column
            for k in range(rge_htx,rge_hty):
                    temp[j] += float(data[k*width+j])/(height/num)#temp hold the average intensities for each column
        
        
        peak1 = int(max(temp[5:width/2])*percentage1)             #define the percentage of the peak value in left side of the array is left edge
        peak2 = int(max(temp[width/2:-5])*percentage2)            #define the percentage of the peak value in right side of the array is right edge

        for k in range(5, width/2):                               #find left edge, code run from 5th pixel to the middle of the cropped image 
            if peak1 < temp[k]:                                   #find the value greater than the peak1 that defined before
                first1.append(k-1)
                break
        
        for k in range(width-5, width/2, -1):                     #find right edge, code run from the last 5th pixel to the middle of the cropped image 
            if peak2 < temp[k]:                                   #find the value greater than peak2 that define before
                last1.append(k+1)
                break
    #measurement filter------------------------------------------------------------------------------------
    if len(first1) != 0 and len(last1) != 0:          #Values will be filter by this process
        error = (first1 - mean(first1))**2
        ermedian = median(error) * 2
        g = 0
        for f in range(0,len(first1)):
            if error[f] > ermedian:
                first1 = delete(first1, [g])
                g = g-1
            elif error[f] < ermedian/4:
                first1 = delete(first1, [g])
                g = g-1
            g += 1
        if len(first1) == 0 :                         #In case the value not define, so I set the value back to original value that before filter 
            first1 = temp1

        error = (last1 - mean(last1))**2
        ermedian = median(error) * 2
        g = 0
        for f in range(0,len(last1)):
            if error[f] > ermedian:
                last1 = delete(last1, [g])
                g = g-1
            elif error[f] < ermedian/4:
                last1 = delete(last1, [g])
                g = g-1
            g += 1
        if len(last1) == 0 :                          #In case the value not define, so I set the value back to original value that before filter 
            last1 = temp2
    #-----------------------------------------------------------------------------------------            
    first = mean(first1)                    #average the measurement that stand for left edge
    last = mean(last1)                      #average the measurement that stand for right edge
    print first,last, cnt                   #the two edge and the number of the image will be print on screen
        
    pixelwidth = (last-first)               #calculate the with in pixel
    draw = ImageDraw.Draw(hold)             #draw something on image
    cmwidth = calib[position-1] * pixelwidth#convert the width from pixel to actual 
        
    if len(first1) == 0 or len(last1) == 0: #if no measurement 'could not find edges' will be write on image
        draw.text((5, (boxS[1]*i+20)), 'Could not find edges')
        cmlist.append(0)                    #convert the incorrect measurement into 0
    else:
        cmlist.append(cmwidth)              #the other case hold the measurement
        
    text = ' %s ,%3d, %3d, %3d' % (filename, pixelwidth, int(first), int(last))# define the text

    string = '%2.1f' % (cmwidth) + 'cm'                     #define the text of with in actual
    pos = (int(boxS[0]/3), int((boxS[1]+1)*i+boxS[1]/2)-1)  #define the position on all cropped images
    draw.text( pos, string)                                 # write edge width on image

    topline = int((boxS[1])/4+(boxS[1]+1)*i)        #define the start point for the line to draw stand for measurement 
    botline1 = int((boxS[1])*3/4+(boxS[1]+1)*i-1)   #define line stand for measurement
    botline2 = int((boxS[1])+(boxS[1]+1)*i-1)       #define line stand for measurement
    draw.line(((0, (boxS[1])*(i+1)+i),(boxS[0]*3, (boxS[1])*(i+1)+i)),fill=(255,255,255),width=1) #draw white image to seperate image 
    draw.line(((boxS[0],0), (boxS[0],(boxS[1]+1)*41)), fill= (255,255,255) ,width=1)              #draw white image to seperate image 
    draw.line(((boxS[0]*2+1,0), (boxS[0]*2+1,(boxS[1]+1)*41)), fill= (255,255,255),width=1)       #draw white image to seperate image 
    
    if position in range(12,15):                                             #draw lines from round structure
        htline = (boxS[1]+1)*i + boxS[1]/2
        draw.line(((0,htline), (first,htline)),fill=255,width=2)             #line stand for left edge
        draw.line(((last,htline),(boxS[0],htline)),fill=255,width=2)         #line stand for right edge
    else:                                                                    #draw lines for vertical structure
        draw.line(((first,(boxS[1]+1)*i), (first,topline)),fill=256,width=1) #left top
        draw.line(((first,botline1), (first, botline2)),fill=256,width=1)    #left bottom
        draw.line(((last,(boxS[1]+1)*i),(last,topline)),fill=256,width=1)    #right top    
        draw.line(((last,botline1),(last,botline2)),fill=256,width=1)        #right bottom

    draw = ImageDraw.Draw(hold)                                         #draw text on image
    draw.text((boxS[0]-15, ((boxS[1]+1)*i+boxS[1]-10)),('%d' %int(i+1)))#draw slice number for each cropped image
    draw.text((4,5),('%d' % position))                                  #draw position on the top
      
    cnt +=1        #counter adding 1
    if cnt >= 50:  #exit if the code run over 50 times
        break      #stop
    close('all')   #close all temp data
    
picture = "C:\\Documents and Settings\\lili\\Desktop\\test\\ImagesOfPosition"                           #define the path for save
follow = ".jpg"                                                                                         #define the extension save as
hold.save(picture[0:len(picture)] + "%s" % position  +"("+"%s" %num +"Division)"+ follow[0:len(follow)])#save the image
print "Done for the results of position", position                                                      #output to screen
fof.writerow(cmlist)                                                                                    #write results to excel file 
print 'cmlist', cmlist                                                                                  #show the measurement on screen

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~result plotting process~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

x_list = arange(0,8.2,0.2)  #define x-axis range from 0 to 8.2 and with seperate for 0.2
y_list = cmlist             #define y-axis is measurement
y_list = array(y_list)      #convert the tuple into an array

#result filter---------------------------------------------------------------------------
medianCmlist = median(cmlist)             #define the median measurement
for i in range(0,len(y_list)):            #the filter is to filter the measurement which is very large than median value
    if y_list[i] >= (1+0.3)*medianCmlist: #define the value will be filtered if it greater than 30% of the median value
        y_list[i] = 0
yhold = y_list
g=0

for i in range(0,len(yhold)):             #the filter is to filter the measurement which is 0
    if yhold[i] == 0.0:
        y_list = delete(y_list, [g])
        x_list = delete(x_list, [g])
        g = g-1
    g += 1
#----------------------------------------------------------------------------------------------

w =  polyfit(x_list,y_list,2)                           #define the function with up to x^2 
f = polyval(w,x_list)                                   #combine the curve on x axis

plot(x_list, y_list, 'bo', x_list, f, '-k', linewidth=2)#plot the curve
#axis([0, 9,49,53 ])                                     #create certain range for x-axis
string = '%s' % position                                #define the position number
anotherString = '%s' % num                              #define the number that you want to divide the iamge in
title('Ice Progression for Position ' + string + ' of Image (Dec 29)['+ anotherString+ 'division]')#create the title for plotting
xlabel('Time (hr)')                                     #create the title for x axis
ylabel('Iced Structure Width (cm)')                     #create the title for y axis

savefig('C:\\Documents and Settings\\lili\\Desktop\\test\\TheGraphOfPosition' + string +'(' + anotherString+ 'Division)'+ '.png')#save the plotting
clf()                                                   #clean temp figures
endTime = time.time()                                   #record end time 
print 'The time of running the code',  endTime-startTime#calculate the time need to process

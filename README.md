# Analysis Strategies for Marine Icing and Impact Module Images

Image analysis strategy has been developed to analyze Marine Icing images for the purpose of obtaining quantitative time series icing thickness growth. The same technique has been also found to be very effective for acquiring pressure data from images from a novel opto-mechanical pressure sensor technology that is incorporated in a new ice impact panel. The images from the Impact Module provide the test information of dropping an ice block onto the Module, and the analysis technique is able to analyze the images because the test information is recorded on the width of the object and can be calculated from the measurements. 


## Image Analysis for Marine Icing

Ice accumulation on a vessel is usually caused by fog, freezing rain, and sea spray accumulating on the superstructure or the hull and freezing under their freezing points. In order to enhance the icing strength of a boat, researchers need to find the maximum icing impact and to provide necessary emergency warning. The requirement of researching ice impact is to collect detailed data from ice accumulation. In order to collect the data of vessel icing, the Marine Icing Monitoring System (MIMS) is designed for monitoring the event on the boat. MIMS consists of two high-resolution cameras, a computer enclosure, a telephone enclosure and a power enclosure. 

For surveying the rate of ice accumulation, the selected icing events should continue as long as possible. The Starboard images at daytime of Dec 29, 2006 provide more than forty continuous icing events. The images show a very detailed marine icing process. The first few images have no icing event, and the marine ice is accumulating on the vessel along with time passing. Not only the increasing ice thickness can be distinguished, but many sea sprays during the time period can be viewed as well. As a result, these images are treated as analysis research material for measuring ice thickness. 

Leah Gibling (2007) first claimed a manual method of measuring ice thickness in the report “Marine Icing Events: An Analysis of Images Collected from the Marine Icing Monitoring System (MIMS)”.  She notes that the measurement is to count pixels between two edges of the selected position for each ice accumulated image, and then compares the record result with the image with no icing event.  All measurements are recorded in a Microsoft Excel spreadsheet, and the software will display a linear graph to show the ice growth. The measurement is accurate but it takes too long to measure, so it is desirable that the analysis method be automated. 
Based on Gibling’s method, Wayne Bruce programmed an automatic image analysis method in Python in winter 2008. Python is an object-oriented programming (OOP) language, which provides a variety of modules. Comparing with C++, Python programming language is much easier to learn, and the code does not need to have a main function. Python is supported by many kinds of libraries, and the Python Image Library (PIL) is very useful to analyze ice event images. PIL is widely used in processing lattice images for Python. PIL lists the intensity of each pixel for interpreters to input an image to their code. The code contains the image for interpreters to analyze, and they can change the values of intensity, thereby changing the output of the image. Depending on the property of PIL and the method from Gibling, Bruce programmed a Python code to count the pixels between edges of the selected structures that are shown in Figure 3. 





## Image Analysis for Impact Module




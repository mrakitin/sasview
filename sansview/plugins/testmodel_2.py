"""
Test plug-in model
These are links of available functions:

http://docs.python.org/library/math.html
http://www.scipy.org/Numpy_Functions_by_Category
"""
from sans.models.pluginmodel import Model1DPlugin  ##DO NOT CHANGE THIS LINE!!!
from math import *                    ##DO NOT CHANGE THIS LINE!!!
from numpy import *                ##DO NOT CHANGE THIS LINE!!!

##PLEASE READ COMMENTS CAREFULLY !!! COMMENT ARE IN CAPITAL LETTERS AND AFTER ##
## THESE COMMENTS ARE THERE TO GUIDE YOU. YOU CAN REMOVE THEM ONLY WHEN YOU ARE
## CONFORTABLE ENOUGH WITH OUR MODEL PLUGIN OPTION


## <-----  SIGN DEFINES WHERE YOU CAN MODIFY THE CODE

class Model(Model1DPlugin): ##DO NOT CHANGE THIS LINE!!!
    """
    ##YOU CAN BE MODIFY ANYTHING BETWEEN """ """
    ##DESCRIPTION OF MODEL PLUG-IN GOES HERE
    
    ##EXAMPLE: Class that evaluates a polynomial model. 
    """
    ## YOU CAN MODIFY THE LINE BELLOW. CHANGE ONLY WORDS BETWEEN " " 
    ## TO RENAME YOUR MODEL
    name = "sin(poly)/(poly)" ## <----- NAME OF THE MODEL   
                                
    def __init__(self):      ##DO NOT CHANGE THIS LINE!!!
        """
        Initialization
        """
        Model1DPlugin.__init__(self, name=self.name) ##DO NOT CHANGE THIS LINE!!!
        
        ## EDIT PARAMETERS' NAMES AND VALUE
        ## DELETE MODIFIABLE LINE HERE WILL REDUCE THE NUMBER OF PARAMETERS
        self.params = {}                ##DO NOT CHANGE THIS LINE!!!
        
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ' AND NUMBER 
        ## YOU CAN ALSO DELETE THIS LINE
        self.params['scale'] = 1.0   ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ' AND NUMBER 
        ## YOU CAN ALSO DELETE THIS LINE                                                      
        self.params['A'] = 0.0       ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ' AND NUMBER 
        ## YOU CAN ALSO DELETE THIS LINE                 
        self.params['B'] = 10.0      ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ' AND NUMBER 
        ## YOU CAN ALSO DELETE THIS LINE                  
        self.params['C'] = 0.0       ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ' AND NUMBER 
        ## YOU CAN ALSO DELETE THIS LINE                
        self.params['D'] = 0.0     ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ' AND NUMBER 
        ## YOU CAN ALSO DELETE THIS LINE                   
        self.params['E'] = 0.0     ## <-----   
        ## YOU CAN MODIFY THELINE BELLOW.CHANGE WORD BETWEEN ' ' AND NUMBER 
        ## YOU CAN ALSO DELETE THIS LINE                  
        self.params['F'] = 0.0     ## <-----          

        ## STORING PARAMETERS  [UNIT, MINIMUM VALUE, MAXIMUM VALUE]
        self.details = {}    ##DO NOT CHANGE THIS LINE!!!
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ',WORD BETWEEN
        ## ' ', TWO OTHER NUMBESR TO NEW VALUE OR YOU CAN ALSO DELETE TH LINE      
        self.details['scale'] = ['',None, None]    ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ',WORD BETWEEN
        ## ' ', TWO OTHER NUMBERS TO NEW VALUE OR YOU CAN ALSO DELETE TH LINE     
        self.details['A'] = ['', None, None]        ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ',WORD BETWEEN
        ## ' ', TWO OTHER NUMBERS TO NEW VALUE OR YOU CAN ALSO DELETE TH LINE     
        self.details['B'] = ['', None, None]        ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ',WORD BETWEEN
        ## ' ', TWO OTHER NUMBERS TO NEW VALUE OR YOU CAN ALSO DELETE TH LINE     
        self.details['C'] = ['', None, None]        ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ',WORD BETWEEN
        ## ' ', TWO OTHER NUMBERS TO NEW VALUE OR YOU CAN ALSO DELETE TH LINE     
        self.details['D'] = ['', None, None]        ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ',WORD BETWEEN
        ## ' ', TWO OTHER NUMBERS TO NEW VALUE OR YOU CAN ALSO DELETE TH LINE     
        self.details['E'] = ['', None, None]        ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.CHANGE WORD BETWEEN ' ',WORD BETWEEN
        ## ' ', TWO OTHER NUMBERS TO NEW VALUE OR YOU CAN ALSO DELETE TH LINE     
        self.details['F'] = ['', 0, 1e16]           ## <-----   
        ## YOU CAN MODIFY THE LINE BELLOW.MODIFY WORDS BETWEEN """   """  ONLY!!!!
        self.description = """
            scale * sin(F(x)/F(x)) \n where F(x)=A+B*x+C*x^2+D*x^3+E*x^4+F*x^5
                 """                        ## <-----   
   
    def function(self, x = 0.0): ##DO NOT CHANGE THIS LINE!!!
        """ 
        Evaluate the model
        
        :param x: input x
        
        :return: function value
        
        """
        ## ADD YOUR FUNCTION HERE.
        ## REUSE THE PARAMETERS DEFINED PREVIOUSLY TO WRITE YOUR FUNCTION.
        
        ## IN THIS EXAMPLE THE FUNTION IS:
        ## scale * sin(F(x)/F(x)) \n where F(x)=A+B*x+C*x^2+D*x^3+E*x^4+F*x^5
        
        ## YOU CAN REWRITE OUR EXAMPLE WITH EVERYTING INSIDE " " :
        ## "RETURN self.params['scale']* (self.params['A'] + self.params['B']*x + \
        ##   self.params['C']* pow(x,2) + self.params['D']*pow(x,3)+\
        ## self.params['E']*pow(x,4) +self.params['F']*pow(x,5)  ) "  
         
        ## NOTE: pow IS A FUNCTION IMPORTED FROM PYTHON MATH LIBRARY
        ## FOR MORE INFORMATION CHECK http://docs.python.org/library/math.html      
        ## OTHER FUNCTIONS ARE ALSO 
        ###  AVAILABLE http://www.scipy.org/Numpy_Functions_by_Category
        ## numpy FUNCTIONS ARE FOR EXPERT USER
        
         
        ## YOU CAN ERASE EVERYTHING BELLOW FOR YOUR OWN FUNCTION
        #Redefine parameters as local parameters
        a = self.params['A']       ## <-----   
        b = self.params['B']       ## <-----   
        c = self.params['C']       ## <-----   
        d = self.params['D']       ## <-----   
        e = self.params['E']       ## <-----   
        f = self.params['F']        ## <-----   
        scl = self.params['scale']   ## <-----   
        ##THIS OUR FUNCTION TEMPLATE
        poly = a + b*x + c*math.pow(x,2) + d*math.pow(x,3) \
             + e*math.pow(x,4) +f*math.pow(x,5)      ## <-----                
        
        #Remove a singular point (lim poly --> 0) for sin(poly)/poly
        #(Just note: In Python, indentation defines the belongings of 'if', 'for', and so on..)
        if poly == 0:                       ## <-----   
            result = 1                      ## <-----   
        else:                               ## <-----   
            result = sin(poly)/poly    ## <-----   
            
        #Re-scale                          ## <-----   
        result *=scl                       ## <-----   

        return result ## MODIFY ONLY RESULT. DON'T DELETE RETURN!!!!
   
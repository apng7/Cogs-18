import numpy as np
import pandas as pd

class WilksScore():
    #The default is the path for the block from my computer. 
    def take_current_weight_current_bw(self, df = pd.read_excel (r'/home/ann129/Final_Proj/final_proj_block_ex.xlsx')):
        
        #This line of code and docstring instructions for it were copied from https://datatofish.com/read_excel/
        """Takes values for squat weight lifted and bodyweight and puts them into an array for use in the other methods. This is specific for squat weights from the block file 
    
    Parameters
    ----------
    df : method
        Pandas method: pd.read_excel (r'C:\\Users\\Ron\\Desktop\\Product List.xlsx'), (use "r" before the path string to address special character, such as '\'). Don't forget to put the file name at the end of the path + '.xlsx'
        Used to call the excel file that contains the block from the directory. The default is my personal path to the file & is a format example. 
        
        
    Returns
    -------
    arr_weight_and_bw : array
        Array of that contains one list of weight values from the block and one list of bodyweight values that correspond to those weights. 
        
    """

        current_weight = []
        current_bw = []
        #This calls the row number for the list so that you could call specific cells that correspond to each other 
        #For "Paused Bench" and "Sumo Deadlift" exercises, change 'Low Bar Squat' to the exercise name
        #For simplification purposes, all of the bodyweights from the block file will be 66 kg
        #The file must be formatted as Week, Day, Lift, Weight (kg), BW
        for item_number in range(len(df)):
            #df.loc[] is a pandas method
            if 'Low Bar Squat' in df.loc[item_number, 'Lift']: 
                current_weight.append(df.loc[item_number, 'Weight (kg)'])
                current_bw.append(df.loc[item_number, 'BW'])
                for n in current_weight:
                    int(n)
                for n in current_bw:
                    int(n)
                #The outputted array has lift weights and corresponding bodyweights
                #Array is a numpy method
                arr_weight_and_bw = np.array([current_weight, current_bw])
                
        return arr_weight_and_bw


    #These default values are specific for male lifters. 
    #Female lifters will have values of a=594.31747775582, b=-27.23842536447, c=0.82112226871, d=-0.00930733913, e=4.731582E-05, f=-9.054E-08
    def wilks_coefficient(self, bw, a = -216.0475144, b = 16.2606339, c = -0.002388645, d = -0.00113732, e = 0.00000701863, f = -0.00000001291):
        
        """Converts an inputted bodyweight to a wilks coefficient that is used to standardize lift weight values. 
    
    Parameters
    ----------
    bw : int or float
        Bodyweight value that is converted to a wilks coefficient. 
    
    
    Returns
    -------
    wilks_coefficient : float
        The resulting wilks coefficient. 
    """
        
        wilks_coefficient = 500/(a + b*bw + c*(bw**2) + d*(bw**3) + e*(bw**4) + f*(bw**5))
        
        return wilks_coefficient      


    #Outputs a list of wilks coefficients that are calculated from the array output of the take_current_weight_current_bw method
    #Takes all of the bodyweights that correspond to the specified exercise
    def current_wilks_coefficient(self):
        
        """Takes bodyweights from the current bodyweight array and converts them to wilks coefficients. 
    
    Parameters
    ----------
    No parameters. 
    
    
    Returns
    -------
    current_wilks_coefficient : list
        The resulting wilks coefficient of each bodyweight value in the take_current_weight_current_bw array. 
    """
        current_wilks_coefficient = []
        #Loops through items in the first list of the current weights array
        for items in self.take_current_weight_current_bw()[1]:
            each_wilks = self.wilks_coefficient(bw = items)
            current_wilks_coefficient.append(each_wilks)
            
        return current_wilks_coefficient



    #Outputs a list of the wilks-standardized lifted weight values
    #For more general purposes, add inputs and set the lift/weight from the excel files as defaults
    def calc_wilks_score(self):
        
        """Takes the wilks coefficient for the bodyweights from the block excel file and multiplies it by each of the corresponding lift weights. 
    
    Parameters
    ----------
    No parameters. 
    
    
    Returns
    -------
    current_wilks_coefficient : list
        The resulting list of wilks-standardized values for lifted weights. 
    """
        
        standardized_lifts = []
        lift_weight_list = self.take_current_weight_current_bw()[0]
        wilks_coeff_list = self.current_wilks_coefficient()
        #This finds the row number and can be used to call specific cells
        for item_number in range(len(lift_weight_list)):
            #This standardizes the lifted weights
            output = lift_weight_list[item_number] * wilks_coeff_list[item_number]
            standardized_lifts.append(output)
            
        return standardized_lifts

    
class Suggest():

    #To improve this, change the dictionaries to lists and put it into array
    #Add accessories for other aspects of the lift
    def suggest_accessory(self):
        
        """Suggests workouts if the condition in the SquatOptimizer.compare_wilks() method and in the questionaire are met. Loops through questions regarding aspects of the lift that need improvement. Suggests accessory exercises accordingly. 
    
    Parameters
    ----------
    No parameters. 
    
    
    Returns
    -------
    suggest_type : dictionary
        One or more dictionaries of suggestions to improve upon the lift. 
    """
        accumulation_quad_accessory_dict = {'Quad 1' : 'DB Bulgarian Split Squat 3x10 @ 7',
                                            'Quad 2' : 'Leg Extensions 3x10 @ 7',
                                            'Quad 3' : 'Front Squat 2x9 @ 7',
                                            'Quad 4' : 'Walking DB Lunge 3x8 @ 6-7',
                                            'Quad 5' : 'Single Leg Static Lunges (Dips) 3x10 @ 7',
                                            'Quad 6' : 'Leg Press Machine 3x8 @ 7'
        }

        accumulation_posterior_chain_accessory_dict = {'Posterior Chain 1' : 'Hamstring Curls 3x8 @ 6',
                                                       'Posterior Chain 2' : 'Good Morning 3x8 @ 6',
                                                       'Posterior Chain 3' : 'Hip Thrust 3x8 @ 7',
                                                       'Posterior Chain 4' : 'Hamstring Curls 3x10 @7',
                                                       'Posterior Chain 5' : 'DB RDL 3x12 @ 7',
                                                       'Posterior Chain 6' : 'Conv. SLDL 3x12 @ 7',
                                                       'Posterior Chain 7' : 'Paused Squat 3x8 @ 6-7',
                                                       'Posterior Chain 8' : 'Sumo RDL 3x8 @ 7'                                               
        }

        accumulation_core_accessory_dict = {'Core 1' : 'Back Extensions 3x15 @ 6-7',
                                            'Core 2' : 'High Bar Squat 3x8 @ 6',
                                            'Core 3' : 'Tempo Squat 3x7 @ 7',
                                            'Core 4' : 'Hanging Knee Raises 3 sets @ 7',
                                            'Core 5' : 'Ab Pulldown 3x8 @ 7-8',
                                            'Core 6' : 'DB RDL 3x12 @ 6-7',
                                            'Core 7' : 'Seated Row 3x10 @ 7'

        }           
        
        
        suggest_type = print('Please enter a response as either "y" or "n"')
        suggest_quad = []
        suggest_core = []
        suggest_posterior_chain = []
        
        #This initiates the questionaire
        stop = True
        while stop == True: 
            suggest_quad = input('Do you struggle with quad engagement? y/n')
            suggest_core = input('Do you struggle with core engagement? y/n')
            suggest_posterior_chain = input('Do you struggle with posterior chain engagement? y/n')
            stop = False
        
        
        if suggest_quad == 'y':
            suggest_type = print('Here are some quad accessories: ') 
            print(accumulation_quad_accessory_dict)
        elif suggest_quad == 'n':
            suggest_type = print ('Good work on quads!')
        if suggest_core == 'y': 
            suggest_type = print('Here are some core accessories: ') 
            print(accumulation_core_accessory_dict)
        elif suggest_core == 'n':
            suggest_type = print ('Good work on core!')
        if suggest_posterior_chain == 'y':
            suggest_type = print ('Here are some posterior chain accessories: ')
            print(accumulation_posterior_chain_accessory_dict)
        elif suggest_posterior_chain == 'n':
            suggest_type = print ('Good work on posterior chain!')
            
        return suggest_type
    
    #This class uses parent methods from the specified parent classes
class SquatOptimizer(WilksScore, Suggest):

    #Outputs a float value of the wilks score
    def ask_max_and_convert(self):
        
        """This calls on the WilksScore.wilks_coefficient() method and multiplies it by the one-repitition max weight to convert it to a wilks-standardized value. This is used as a basis of comparison.  
    
    Parameters
    ----------
    No parameters. 
    
    
    Returns
    -------
    output : float
        Standarized value of your one-rep max
    """
        
        output = (int(input('What is your 1 rep max for the squat? (kilograms)'))) * self.wilks_coefficient(bw = int(input('What was your bodyweight at the time when you attempted this lift? (kilograms)'))) 
        
        return output
    
    
    #For the excel file that is inputted, the wilks scores should be: 105.04893253656917, 78.341576806932935, 76.561086424957196, 80.122067188908687
    def compare_wilks(self):
        
        """This takes the standardized max weight value from the ask_max_and_convert() method and makes an upper and lower limit for the optimal training weight values. Then, it compares those standardized weights to the standardized weights obtained from the excel file in order to see whether I have overshot or not.  
    
    Parameters
    ----------
    No parameters method
    But running this method will initiate the program and will run other methods that will have a parameter input. Those parameters will be either float or str inputs. 
    
    
    Returns
    -------
    current_wilks_coefficient : str or method
        The output will either be a string that warns about overshooting, a string that confirms that the lifted weights are in the right range, or call the Suggest.suggest_accessory() method for further conditionals. 
        
     Executing this method will run the program. 
    """
        
        current_scores = self.calc_wilks_score()
        max_score = self.ask_max_and_convert()
        suggest_counter = 0
        #The lower limit for a max lift of 165 @ 66bw = 77.73442958667921
        lower_lim = int(max_score) * 0.6
        #The upper limit for a max lift of 165 @ 66bw = 97.16803698334901
        upper_lim = int(max_score) * 0.75 
        #If the weight on the block file is too high, the counter will increase
        #If the weight on the block file is too low, the counter will decrease and call on suggest_accessory method. 
        for scores in current_scores:
            if scores > upper_lim:
                suggest_counter += 1
            elif scores < lower_lim:
                suggest_counter -= 1
            else: 
                suggest_counter = suggest_counter
        if suggest_counter >= 2:
             output = 'Stop overshooting or you might get injured!'
            #To get this output, enter: 100 for 1rm and 66 for bodyweight
        elif suggest_counter <= -2:
            output = self.suggest_accessory()
            #To get this output, enter: 200 for 1rm and 66 for bodyweight
        else: 
            output = 'Pocket work'
            #To get this output, enter: 150 for 1rm and 66 for bodyweight
            
        return output

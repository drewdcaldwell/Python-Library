#************************************************************************************
# Nicely Format Numbers for readability | (INT -> String) ---- Ex. 12500 -> 12,500  *
#************************************************************************************

#input = 1000000000000          #*********Passed************
# input 1,000,000,000,000       #         Date: 1/7/2026
input = 50000000000             #*********Passed************
# input 50,000,000,000          #         Date: 1/7/2026
#input = 150000000000000        #*********Passed************
# input 150,000,000,000,000     #         Date: 1/7/2026

def add_commas_to_number(input):
    # Change from Int to Str to traverse
    inputChar = str(input)
    # Get Length to traverse 
    length = len(str(input))
    # Main Loop
    i=0; count = 0; output = ""
    while i < length:
        count += 1
        if count % 3 == 0:
            if i != length - 1:
                output = "," + str(inputChar[length-count:length-count+1]) + output
            else:
                output = str(inputChar[length-count:length-count+1]) + output
        else: 
            output = str(inputChar[length-count:length-count+1]) + output
        i += 1
    return output
    
#print(output)
print("********Formatted Change Amount**********")
print(add_commas_to_number(input))
print("*****************************************")
#print("Random Testing Notes")
#print(str(inputChar[length-1:length]))
#print(str(inputChar[length-2:length-1]))
#print(str(inputChar[length-3:length-2]))
#print(str(inputChar[length-4:length-3]))

#####################################################################################
## Nicely Format Numbers for readability | (DEC -> String) ---- Ex. 12500 -> 12,500 #
#####################################################################################

def add_commas_to_number(input):
    # Change from Int to Str to traverse
    inputChar = str(input)
    # Get Length to traverse
    length = len(str(input))
    # Main Loop
    i=0; count = 0; output = ""
    while i < length:
        count += 1
        if count % 3 == 0:
            if inputChar[length-count:length-count+1] == '.':
                output = str(inputChar[length-count:length-count+1]) + output
            elif i != length - 1:
                output = "," + str(inputChar[length-count:length-count+1]) + output
            else:
                output = str(inputChar[length-count:length-count+1]) + output
        else:
            output = str(inputChar[length-count:length-count+1]) + output
        i += 1
    return output        


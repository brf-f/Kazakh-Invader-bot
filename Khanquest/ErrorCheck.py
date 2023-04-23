from ast import literal_eval

# Returns type of input and Capitalises strings
def getType(input):
    try:
        input = literal_eval(input)
        return type(input), input
    except (ValueError, SyntaxError):
        # A string, so return str
        return str, input.capitalize()

#checks if user input is valid and expected
def CheckInput(InpStr, expected, type):    
    inp = input(InpStr)
    while True:
        getT = getType(inp)
        if getT[0] == type:
            if expected == "noList" or getT[1] in expected:
                return getT[1]

        print("Please enter a valid value")
        inp = input(InpStr)
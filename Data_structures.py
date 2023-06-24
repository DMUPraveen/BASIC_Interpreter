def isSingleDigit(char):
    return (ord(char) < 58 and ord(char) >47)
from math import sin

class Stack:

    def __init__(self):
        self.stack_buffer = []
        self.stack_frame = [0]

    def push(self,value):
        self.stack_buffer.append(value)
    
    def pop(self):
        if(not self.isEmpty()):
            return self.stack_buffer.pop(-1)
        else:
            raise Exception

    def flush(self):
        self.stack_buffer.clear()

    def isEmpty(self):  
        return (len(self.stack_buffer) == self.stack_frame[-1])
    def see(self):
        if(not self.isEmpty()):
            return self.stack_buffer[-1]
        else:
            return None
    def get_length(self):
        return len(self.stack_buffer)
    def add_frame(self):
        self.stack_frame.append(self.get_length())
    def remove_frame(self):
        while not self.isEmpty():
            self.pop()
        self.stack_frame.pop(-1)

class ReversePolish:
    '''
    OPERATOR PRESIDENCE

     '^' > '/' = '*' > '+' = '-'
    '''
    operatorOrder = {
        '=' : 0,
        '<' : 0,
        '>' : 0,
        '<=': 0,
        '>=': 0,
        '!=': 0,
        '&' : 0,
        '|' : 0,
        '!' : 0,
        '-' : 1,
        '+' : 1,
        '*' : 2,
        '/' : 2,
        '@neg':3,
        '^' : 4,
        '(' : 5,
        'f' : 5
        
    }
    operators = set(["+","-","*","/","^","=","<",">","@neg",'!=','>=','<=',"&","|"])
    negationpredecors = set(["+","-","*","/","^","=","<",">","(",'','@neg','&','|'])
    specialcharacter = set(["+","-","*","/","^","(",")"])
    attachedoperator = set(["<",">","="])
    @classmethod
    def nobracketreversePolish(cls,sExpression):
        delemeter = " "
        operatorstack = Stack()
        translated = ''
        variable = ''
        for i in sExpression:
            if(i == " "):
                continue
            if(i in cls.operatorOrder):
                if(len(variable) !=0):
                    translated += variable + delemeter
                    variable = ''
                
                if(operatorstack.isEmpty()):
                    operatorstack.push(i)
                elif(cls.operatorOrder[operatorstack.see()]>=cls.operatorOrder[i]):
                    while(not operatorstack.isEmpty() and
                    (cls.operatorOrder[operatorstack.see()]>=cls.operatorOrder[i])):
                        translated += operatorstack.pop() + delemeter
                    operatorstack.push(i)
                else:
                    operatorstack.push(i)
                
            else:
                variable +=i
        translated += variable + delemeter
        while(not operatorstack.isEmpty()):
            translated +=operatorstack.pop() + delemeter

        return translated[:-1]
    
    @staticmethod
    def revPolCal(revPol):
        inst = revPol.split(" ")
        print(inst)
        calStack = Stack()
        for i in inst:
            if(i == "+"):
                a = calStack.pop()
                b = calStack.pop()
                calStack.push(b+a)
            elif(i == "-"):
                a = calStack.pop()
                b = calStack.pop()
                calStack.push(b-a)
            elif(i == "*"):
                a = calStack.pop()
                b = calStack.pop()
                calStack.push(b*a)
            elif(i == "/"):
                a = calStack.pop()
                b = calStack.pop()
                calStack.push(b/a)
            elif(i == "^"):
                a = calStack.pop()
                b = calStack.pop()
                calStack.push(b**a)
            elif(i == "sin"):
                calStack.push(sin(calStack.pop()))
            else:
                calStack.push(int(i))
        return calStack.pop()

    @classmethod
    def calculate(cls,expression):
        rPExp = cls.convert(expression)
        print(rPExp)
        return cls.revPolCal(rPExp)

    @classmethod
    def convert(cls,sExpression):
        sExpression = sExpression.lstrip()
        delemeter = " "
        operatorstack = Stack()
        functionStack = Stack()
        translated = ''
        variable = ''
        attachedoperatorFlag = False
        previous =''
        for index,i in enumerate(sExpression):
            if(i == " "):
                continue
            if(i == ","):
                if(variable != ""):
                    translated += variable + delemeter
                while(not operatorstack.isEmpty() and operatorstack.see() != "f"):
                    translated += operatorstack.pop()+delemeter
                variable = ""
                continue
            if(i == "-" and previous in cls.negationpredecors):
                i = '@neg' #the the minus sign does not represent substraction but negation
            previous = i
            if(i in cls.attachedoperator):
                if(index+1 != len(sExpression) and sExpression[index+1] == "="):
                    attachedoperatorFlag = True
                    if(i == ">"):
                        i = ">="
                    elif(i == "<"):
                        i = "<="
                elif(index+1 != len(sExpression) and sExpression[index+1] == ">" and i=="<"):
                    attachedoperatorFlag = True
                    i = "!="

                elif(attachedoperatorFlag):
                    attachedoperatorFlag = False
                    continue
                    
            
              
    
            if(i == "("):
                
                operatorstack.push(i)
                preval = sExpression[index-1]
                if(preval not in cls.specialcharacter and not isSingleDigit(preval)):
                    operatorstack.push("f")
                    functionStack.push(variable)
                    variable = ''
                continue
                
            if(i == ")"):
                if(variable != ''):
                    translated += variable + delemeter
                variable = ''
                while(not operatorstack.isEmpty()):
                    val = operatorstack.pop()
                    if(val == "f"):
                        _ = operatorstack.pop()
                        translated += functionStack.pop() + delemeter
                        break

                    elif(val != "("):
                        translated += val + delemeter
                    else:
                        break
                continue

            if(i in cls.operators):
                if(variable !=''):
                    translated += variable + delemeter
                    variable = ''
                
                if(operatorstack.isEmpty()):
                    operatorstack.push(i)
                elif(operatorstack.see() == "("):
                    operatorstack.push(i)
                    
                elif(cls.operatorOrder[operatorstack.see()]>=cls.operatorOrder[i]):
                    while(not operatorstack.isEmpty() and
                    (cls.operatorOrder[operatorstack.see()]>=cls.operatorOrder[i])):
                        if(operatorstack.see() == "(" or operatorstack.see() == "f"):
                            break
                        translated += operatorstack.pop() + delemeter
                    operatorstack.push(i)
                else:
                    operatorstack.push(i)

            
            else:
                variable +=i
        if(variable != ''):  
            translated += variable + delemeter
        while(not operatorstack.isEmpty()):
            translated +=operatorstack.pop() + delemeter
        #print(translated[:-1])
        return translated[:-1]

class Queue:
     
    def __init__(self):
        self.stack_buffer = []
       
    def flush(self):
        self.stack_buffer.clear()
    def isEmpty(self):
        return (len(self.stack_buffer) == 0)
    def pop(self):
        return self.stack_buffer.pop(0)
    def push(self,val):
        self.stack_buffer.append(val)

  
if __name__ == "__main__":
    ReversePolish.calculate("(5+3)*(4/(3+1)*(2^4)/(1+1*1))")
    ReversePolish.convert("3*5>=6")
    print(ReversePolish.convert('EXP(-(X^2/2))/SQR(2*3.14159265)'))


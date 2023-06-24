'''
Resources for BASIC Syntax reference

http://physics.clarku.edu/sip/tutorials/True_BASIC.html


https://www.dartmouth.edu/basicfifty/commands.html

https://en.wikipedia.org/wiki/BASIC
'''

from Data_structures import Stack,ReversePolish,Queue
import operatorfuncs as Of
import os

ALL_VARIABLES_ARE_INITIALISED_TO_ZERO_flag = False

##############################''' Utility functions''' ######################################
def isfloat(a):
    try:
        float(a)
    except:
        return False
    return True

def Invalid_Syntax():
    print("Invlaid syntax")

def getNextSpace(String):
    return String.find(" ")

def getNextWord(String):
    SpacePos = getNextSpace(String)
    if(SpacePos == -1):
        return String
    else:
        return String[:SpacePos].lstrip()

def isCapitalLetter(char):
    return (ord(char) >64 and ord(char) < 91)

def isSingleDigit(char):
    return (ord(char) < 58 and ord(char) >47)

def getLineAndCommand(sCommand):
    Invalid_Line_Number = -1
    spacePos = sCommand.find(" ")
    lineNo = sCommand[:spacePos]
    sCommand = sCommand[spacePos:].lstrip()
    
    if(lineNo !=-1 and lineNo.isdigit()):
        return (int(lineNo),sCommand)
    else:
        
        return (Invalid_Line_Number,sCommand)

def getBetween(string,start='',end=''):
    startPos    = string.find(start) + len(start)
    if(startPos == -1):
        return None
    if(end !=''):
        endPos  = string.find(end)
        if(endPos == -1):
            return None
    else:
        endPos  = len(string)
    return string[startPos:endPos].lstrip().rstrip()   
    

####################################'''Command interpretation'''################################

def interpretCommand(sCommand):
    global ALL_VARIABLES_ARE_INITIALISED_TO_ZERO_flag
    sCommand = sCommand.lstrip().rstrip()
    '''
    Commands are in the form of
    
    Line Number, Command ,....

    '''
    if(sCommand == 'REPL'):
        Computer.mode = 'REPL'
        return
    elif(sCommand == 'PROGRAM'):
        Computer.mode = 'PROGRAM'
        return
    if(sCommand == 'RUN'):
        Computer.run()
        return
    if(sCommand == 'LIST'):
        Computer.List()
        return 
    if(sCommand == 'QUIT'):
        os.system('color f')
        os.system('cls')
        quit()
        return
    if(sCommand == 'CLEAR'):
        os.system('cls')
        return
    if(sCommand == 'SAVE'):
        file_name = input('NAME OF FILE TO WRITE : ')
        if(file_name !=''):
            with open('PROGRAMS\\'+file_name.rstrip().lstrip()+'.BASIC','w+') as f:
                Computer.LineNos.sort()
                for line in Computer.LineNos:
                    f.write(
                        f"{line} {Computer.Instructions[line]}\n"
                        )
        return
    if(sCommand == 'LOAD'):
        basicfile = input('FILE TO BE LOADED : ')
        if(basicfile != ''):
            try:
                with open('PROGRAMS\\'+basicfile+'.BASIC','r') as f:
                    Computer.clearProgram()
                    Computer.mode = 'PROGRAM'
                    lines = f.readlines()
                    for line in lines:
                        interpret_computer_command(line[:-1]) #-1 to remove the new line
            except FileNotFoundError:
                print(f'{basicfile} IS NOT FOUND')
            Computer.List()
        return
    if(sCommand == 'CLEARPROGRAM'):
        Computer.clearProgram()
        return
    if(sCommand == 'TOGGLEFLAG'):
        print('1. ALL_VARIABLES_ARE_INITIALIZED_TO ZER0')
        flag = input('NUMBER OF FLAG TO TOGGLE : ')
        try:
            flag = int(flag)
        except:
            print('INVALID FLAG NUMBER')
            return
        if(flag == 1):
            ALL_VARIABLES_ARE_INITIALISED_TO_ZERO_flag = not ALL_VARIABLES_ARE_INITIALISED_TO_ZERO_flag
        else:
            print('INVALID FLAG')
        return
    if(sCommand == 'REMOVE'):
        line = input('LINE TO REMOVE : ')
        try:
            line = int(line)
        except:
            print('INVALID LINE NUMBER')
            return
        if(line in Computer.LineNos):
            Computer.LineNos.remove(line)
            Computer.Instructions.pop(line)
        return


    interpret_computer_command(sCommand)


def interpret_computer_command(sCommand):
    nLineNumber,sCommand = getLineAndCommand(sCommand)
    if(nLineNumber == -1):
        Invalid_Syntax()
    else:
        Instruction = CreateInstructionObject(sCommand,nLineNumber)
        if(Instruction == None):
            Invalid_Syntax()
        if(Instruction.bValid):
            if(Computer.mode == 'REPL'):
                Instruction.run()
            elif(Computer.mode == 'PROGRAM'):
                if(nLineNumber not in Computer.Instructions):
                    Computer.LineNos.append(nLineNumber)
                Computer.Instructions[nLineNumber] = Instruction
                

        else:
            Invalid_Syntax()
################################################################################################

class DefaultVariable():
    Type = 'DEFAULT'
    def __init__(self,variable):
        self.variable_name = variable
        self.Initialized = False
    def process(self):
        Computer.runtimeError(f"{self.variable_name} is uninitialized")
        return False


class LiteralType():
    Type = 'LITERAL'
    def __init__(self,value):
        self.value = float(value)
        self.Initialized = True
    def process(self):
        Computer.computerStack.push(self.value)
        return True
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

class operatortype():
    Type = 'OPERATOR'
    def __init__(self,function):
        self.function = function
        self.Initialized = True
    def process(self):
        self.function(Computer.computerStack)
        return True

class VariableType():
    Type = 'VARIABLE'
    def __init__(self,value):
        self.value = value
        self.Initialized = True
    def process(self):
        
        Computer.computerStack.push(self.value)
        return True
    
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return self.__str__()

class PlaceHolderType():
    Type = 'PLACEHOLDER'
    def __init__(self,instruction_name):
        self.instruction_name = instruction_name
    def process(self):
        return Computer.getVariable(self.instruction_name).process()
  
    def __str__(self):
        return f"Place holder {self.instruction_name}"
    
    def __repr__(self):
        return self.__str__()

class InlineFunctionType():
    Type ='INLINEFUNCTION'
    def __init__(self,FunctionObject):
        self.FunctionObject = FunctionObject
        self.Initialized = True
    def process(self):
        self.FunctionObject.process(Computer.computerStack)

class Computer():
    mode = 'PROGRAM'
    Variables = {
        "+"     : operatortype(Of.plus),
        "-"     : operatortype(Of.minus),
        "*"     : operatortype(Of.mul),
        "/"     : operatortype(Of.div),
        "^"     : operatortype(Of.power),
        ">"     : operatortype(Of.greater),
        "<"     : operatortype(Of.lesser),
        "="     : operatortype(Of.eq),
        "!="    : operatortype(Of.neq),
        ">="    : operatortype(Of.greatereq),
        "<="    : operatortype(Of.lessereq),
        "@neg"  : operatortype(Of.neg),
        "ABS"   : operatortype(Of.Abs),
        "ATN"   : operatortype(Of.Atn),
        "COS"   : operatortype(Of.Cos),
        "EXP"   : operatortype(Of.Exp),
        "INT"   : operatortype(Of.Int),
        "LOG"   : operatortype(Of.Log),
        "RND"   : operatortype(Of.Rnd),
        "SIN"   : operatortype(Of.Sin),
        "SQR"   : operatortype(Of.Sqr),
        "TAN"   : operatortype(Of.Tan),
        "TAB"   : operatortype(Of.Tab),
        "CHR"   : operatortype(Of.Chr)
        
    } 
    InstructionPointer = 0
    ReturnStack = Stack()
    computerStack = Stack()
    Instructions = {}           #Line : Instruction
    LineNos = []
    LinetoIptr = {}
    ForInstructionstobematched = None
    Forscope = Stack()
    Running = False
    VariableScope = Stack()
    DataStack = Queue()
    @classmethod
    def reset(cls):
        cls.Variables = {
        "+"     : operatortype(Of.plus),
        "-"     : operatortype(Of.minus),
        "*"     : operatortype(Of.mul),
        "/"     : operatortype(Of.div),
        "^"     : operatortype(Of.power),
        ">"     : operatortype(Of.greater),
        "<"     : operatortype(Of.lesser),
        "="     : operatortype(Of.eq),
        "!="    : operatortype(Of.neq),
        ">="    : operatortype(Of.greatereq),
        "<="    : operatortype(Of.lessereq),
        "@neg"  : operatortype(Of.neg),
        "ABS"   : operatortype(Of.Abs),
        "ATN"   : operatortype(Of.Atn),
        "COS"   : operatortype(Of.Cos),
        "EXP"   : operatortype(Of.Exp),
        "INT"   : operatortype(Of.Int),
        "LOG"   : operatortype(Of.Log),
        "RND"   : operatortype(Of.Rnd),
        "SIN"   : operatortype(Of.Sin),
        "SQR"   : operatortype(Of.Sqr),
        "TAN"   : operatortype(Of.Tan),
        "TAB"   : operatortype(Of.Tab),
        "CHR"   : operatortype(Of.Chr)
        
        } 
        cls.InstructionPointer = 0
        cls.ReturnStack.flush()
        cls.computerStack.flush()


        cls.LinetoIptr.clear()
        cls.ForInstructionstobematched = None
        cls.Forscope.flush()
        cls.Running = False
        cls.VariableScope.flush()
        cls.DataStack.flush()

    @staticmethod
    def power_lamda(s):
        a = s.pop()
        s.push(s.pop()**a)

    @classmethod
    def clearProgram(cls):
        cls.Instructions.clear()
        cls.LineNos.clear()
        cls.reset()
    @classmethod
    def getVariable(cls,sVarname):
        if(sVarname in cls.Variables):
            return cls.Variables[sVarname]
        else:
            if(ALL_VARIABLES_ARE_INITIALISED_TO_ZERO_flag and sVarname[:2]!='FN'):
                return VariableType(0)
            #cls.Uninitialized_Varibale_Error(sVarname)
            return DefaultVariable(sVarname)
    
    @classmethod
    def createVariable(cls,sVarname,Variable):
        cls.Variables[sVarname] = Variable

    @staticmethod
    def Uninitialized_Varibale_Error(sName):
        print(f"{sName} variable is uninitialized")
    
    @classmethod
    def run(cls):
        cls.Running = True
        cls.compile()
        
        cls.LineNos.sort()
        if(len(cls.LineNos)==0):
            print('\nREADY')
            cls.reset()
            return
        instructionLength = len(cls.LineNos)
        cls.LinetoIptr = { val:index for index,val in enumerate(cls.LineNos)}
        cls.InstructionPointer = 0
        while cls.Running:
            if(cls.InstructionPointer<0 or cls.InstructionPointer >= instructionLength):
                print("Invalid Instruction Address")
                return
            Line = cls.LineNos[cls.InstructionPointer]
            Instruction = cls.Instructions[Line]
            Instruction.run()
            cls.InstructionPointer +=1
            if(cls.InstructionPointer == instructionLength):
                break

        cls.reset()
        print('\nREADY')
        return
   
    @classmethod
    def List(cls):
        cls.LineNos.sort()
        for line in cls.LineNos:
            print(f"{line} {cls.Instructions[line]}")
    
    @classmethod
    def addinstruction(cls,Instruction,Linenumber):
        cls.Instructions[Linenumber] = Instruction
        cls.LineNos.append(Linenumber)
    
    @classmethod
    def setNextInstructionptr(cls,Linenumber):
        if(Linenumber in cls.LinetoIptr):
            cls.InstructionPointer = cls.LinetoIptr[Linenumber] -1
            return True
        else:
            return False
    
    @classmethod  
    def setCurrentInstructionptr(cls,Linenumber):
        if(Linenumber in cls.LinetoIptr):
            cls.InstructionPointer = cls.LinetoIptr[Linenumber]
            return True
        else:
            return False

    @classmethod
    def runtimeError(cls,errorMsg):
        cls.Running = False
        print(F'RUNTIME ERROR AT LINE NUMBER{cls.LineNos[cls.InstructionPointer]}')
        print(f"RUNTIME ERROR : {errorMsg}")

    @classmethod
    def endProgram(cls,endmessage=None):
        cls.Running = False
        if(endmessage != None):  
            print(endmessage) 
    @classmethod
    def getInstruction(cls,index):
        return cls.Instructions[cls.LineNos[index]]
    
    @classmethod
    def getNumberOfInstructions(cls):
        return len(cls.LineNos)

    @classmethod
    def compile(cls):
        for Line in cls.Instructions:
            cls.Instructions[Line].interpret_command()
            if(not cls.Instructions[Line].bValid):
                print(f'Invalid Command at Line number {Line}')
                cls.Running = False

class Scope():
    def __init__(self,variable_dic):
        self.variable_dic = variable_dic
        self.old_variable_dic = {}
        
        for variable_name in self.variable_dic:
            if(variable_name in Computer.Variables):
                self.old_variable_dic[variable_name] = Computer.getVariable(variable_name)
            Computer.createVariable(variable_name,VariableType(self.variable_dic[variable_name]))

    def cleanup(self):
        for variable_name in self.variable_dic:
            if(variable_name in self.old_variable_dic):
                Computer.createVariable(variable_name,self.old_variable_dic[variable_name])
            else:
                Computer.Variables.pop(variable_name)
        self.variable_dic = None
        self.old_variable_dic = {}

    def __enter__(self):
        return self

    def __exit__(self,exptype,expvalue,exptraceback):
        self.cleanup()
        
##########################################''''Algebraic function data types''''##########################

class Expression():
    def __init__(self,expression):
        self.expression = ReversePolish.convert(expression).split(" ")
        self.instructionStack = Stack()
        self.valid = True
        
        for instruction in self.expression:
            if(isfloat(instruction)):
                self.instructionStack.push(LiteralType(instruction))
            elif(instruction in Computer.Variables):
                variable = Computer.getVariable(instruction)
                self.instructionStack.push(variable)

            else:
                self.instructionStack.push(PlaceHolderType(instruction))

    def evaluate(self):
        Computer.computerStack.add_frame()
        for i in self.instructionStack.stack_buffer:
            try:
                if(not i.process()):
                    Computer.computerStack.push(None)
            except:
                Computer.runtimeError('INVALID EXPRESSION EVALUATION')
                Computer.computerStack.remove_frame()
                return None
        if(Computer.computerStack.isEmpty()):
            return None
        a = Computer.computerStack.pop()
        Computer.computerStack.remove_frame()
        return a

    def __str__(self):
        a = self.evaluate()
        if(type(a) == str):
            return a
        try:
            if(int(a) == a):
                a = int(a)
        except:
            pass
        return f' {a} '
      
      
################ Instruction object ###############################

class DefaultInstructionObject():
    def __init__(self):
        self.bValid = False
        self.sCommand = ''
    def run(self):
        Computer.runtimeError('DefaultInstructionObjectCalled')
    def __str__(self):
        return self.sCommand
    def __repr__(self):
        return self.__str__() 
    def HandleError(self):
        self.bValid = False
    def remove_first(self,str):
        spacePos = getNextSpace(self.sCommand)
        if(spacePos == -1):
            self.HandleError()
            return 
        return self.sCommand[spacePos:].lstrip()
    def get_type(self):
        return 'DEFAULT'
    
    def interpret_command(self):
        pass

class LETOBject(DefaultInstructionObject):

    #Interprets and constructs an object to run the let command

    def __init__(self,sCommand):
        self.bValid = True
        self.sCommand = sCommand
        self.expressionObj = None
        self.variable_name = None
        #self.interpret_command()

    def interpret_command(self):

        ##############Getting rid of Let
        rest  = self.remove_first(self.sCommand)
        if(not self.bValid):
            return
        ################################

        #Seperating the intruction to variable name and expression to be assigned
        equal_pos = rest.find("=")
        if(equal_pos == -1):
            self.HandleError()
            return
        variable_name,expression = rest[:equal_pos],rest[equal_pos+1:]
        #####################################################################
        variable_name = variable_name.rstrip()
        #Imposing BASIC RESTRICTION FOR VARIBLE NAMES SINGLE CAPITAL LETTER OR LETTER FOLOWED BY SINGLE DIGIT
        if(not self.ImposeNamerestriction(variable_name)):
            self.HandleError()
            return
        ####################################################################################
        self.variable_name = variable_name
        self.expressionObj = Expression(expression)
        if(self.expressionObj == None or not self.expressionObj.valid):
            self.HandleError()

    def run(self):
        if (self.variable_name == None and self.expressionObj == None):
            return
        else:
            if(self.variable_name in Computer.Variables):
                val = self.expressionObj.evaluate()
                if(val == None):
                    return
               
                variable = Computer.getVariable(self.variable_name)
                if(variable.Type == 'VARIABLE'):
                    variable.value = val
                else:
                    Computer.runtimeError(f'{self.variable_name} is not a variable')
            else:

                #Computer.Variables[self.variable_name] = VariableType(self.expressionObj.evaluate())
                Computer.createVariable(self.variable_name,VariableType(self.expressionObj.evaluate()))
    
    def HandleError(self,str=""):
        print("Variable Name Error")
        self.bValid = False

    @staticmethod
    def ImposeNamerestriction(name):
        #print(f"#{name}#")
        if(len(name) ==1 and isCapitalLetter(name[0])):
            return True
        elif(len(name) == 2 and isCapitalLetter(name[0]) and isSingleDigit(name[1])):
            return True
        
        return False

    def get_type(self):
        return 'LET'

class PRINTObject(DefaultInstructionObject):
    #Interprets the print command and runs the command

    def __init__(self,sCommand):
        self.bValid = True
        self.sCommand = sCommand

        self.toprint = []
        self.newLine = True
        #self.interpret_command()
    
    def interpret_command(self):
        self.toprint.clear()
        rest  = self.remove_first(self.sCommand)
        if(rest.endswith(',') or rest.endswith(';')):
            self.newLine = False
        if(not self.bValid):
            return
        printables = self.make_list(rest)
    
        for printable in printables:
            
            printable = printable.lstrip().rstrip()
            if(printable == ''):
                continue
            condition1 = printable.startswith("\"") and printable.endswith("\"")
            condition2 = printable.startswith("\'") and printable.endswith("\'")
            if(condition1 or condition2):
                self.toprint.append(printable[1:-1])
            else:
                expression = Expression(printable)
                if(expression == None or not expression.valid):
                    self.HandleError()
                    return
                self.toprint.append(expression)

    def run(self):
        for printable in self.toprint:
            print(printable,end='')
        if(self.newLine):
            print()

    def HandleError(self):
        print(f"invalid expression for printing : {self.sCommand}")
        self.bValid = False
    
    def get_type(self):
        return 'PRINT'

    def make_list(self,string):
        printables = []
        startindex = 0
        bracket_count = 0
        for index,letter in enumerate(string):
            if(letter == "("):
                bracket_count += 1
            elif(letter == ")"):
                bracket_count -=1
            if(letter == ',' and bracket_count == 0):
                printables.append(string[startindex:index])
                startindex = index+1
                printables.append('"\t"')
            elif(letter == ';'):
                printables.append(string[startindex:index])
                startindex = index+1
                
        printables.append(string[startindex:])
        return printables

class ENDObject(DefaultInstructionObject):
    def __init__(self,sCommand):
        self.sCommand = sCommand
        self.bValid = True
    def run(self):
        Computer.Running = False
    def get_type(self):
        return 'END'

class GOTOObject(DefaultInstructionObject):
    def __init__(self,sCommand):
        self.sCommand = sCommand
        self.bValid = True 
        self.Line =0
        #self.interpret_command()
    def interpret_command(self):
        rest = self.remove_first(self.sCommand)
        if(not self.bValid):
            return
        self.Line = int(rest)
    def run(self):
        Computer.setNextInstructionptr(self.Line)
    def get_type(self):
            return 'GOTO'

class IFTHENObject(DefaultInstructionObject):
    def __init__(self,sCommand):
        self.sCommand = sCommand
        self.bValid = True 
        self.expressionObj = None
        self.destination = None
        #self.interpret_command()
    def interpret_command(self):
        rest = self.remove_first(self.sCommand)
        if(not self.bValid):
            return
        THENpos =rest.find(" THEN ")
        if(THENpos == -1):
            self.bValid = False
            return
        exp = rest[:THENpos]
        destination = rest[THENpos+6:]
        self.expressionObj = Expression(exp)
        if(self.expressionObj == None or not self.expressionObj.valid):
            self.bValid = False
            return
        try:
            destination = int(destination)
        except:
            self.bValid = False
            return
        self.destination = destination

    def run(self):
        value = self.expressionObj.evaluate()
        if(value):
            Computer.setNextInstructionptr(self.destination)
    def HandleError(self):
        print("Invalid Expression")
    
    def get_type(self):
        return 'IFTHEN'

class FORObject(DefaultInstructionObject):
    def __init__(self,sCommand,linenumber):
        
        self.sCommand = sCommand
        self.bValid = True 
        self.ValueName = None
        self.EndVal = None
        self.StartVal = None
        self.Step = None
        self.Nextpos = None
        self.started = False
        self.previous = None
        self.internal_variable_ptr = None
        self.linenumber = linenumber
        #self.interpret_command()
   
    def interpret_command(self):
        self.reset()
        self.ValueName = getBetween(self.sCommand,start='FOR ',end="=").lstrip().rstrip()
        StartVal  = getBetween(self.sCommand,start='=',end=' TO ')
        EndVal    = getBetween(self.sCommand,start=" TO ",end='STEP')
        if(EndVal == None):
            EndVal = getBetween(self.sCommand,start=' TO ')
            Step = '1'
        else:
            Step = getBetween(self.sCommand,start="STEP")

        if(self.ValueName == None or StartVal==None or Step == None or EndVal == None):
            self.HandleError()
            return
        self.StartValexp = Expression(StartVal)
        self.EndValexp   = Expression(EndVal)
        self.Stepexp     = Expression(Step)
 
        if(self.StartValexp==None or self.Stepexp == None or self.EndValexp == None):
            self.HandleError()
            return
        Computer.Forscope.push(self)
          
    def run(self):
        if(self.started):
            self.internal_variable_ptr.value = self.internal_variable_ptr.value + self.Step

        if(not self.started):
            self.started    = True
            self.StartVal   = self.StartValexp.evaluate()
            self.EndVal     = self.EndValexp.evaluate()
            self.Step       = self.Stepexp.evaluate()
            
            if(self.StartVal == None or self.EndVal == None or self.Step == None):
                return
            if(self.ValueName in Computer.Variables):
                #self.previous = Computer.Variables[self.ValueName]
                self.previous = Computer.getVariable(self.ValueName)
            self.internal_variable_ptr = VariableType(self.StartVal)
            #Computer.Variables[self.ValueName] = self.internal_variable_ptr
            Computer.createVariable(self.ValueName,self.internal_variable_ptr)
            



            
            
      

        if (self.internal_variable_ptr.value - self.EndVal)*self.Step > 0:
            self.started = False
            if(self.Nextpos == None):
                Computer.runtimeError('NEXT not found')
                return

                
               
            else:
                Computer.setCurrentInstructionptr(self.Nextpos)
            if(self.previous != None):
                #Computer.Variables[self.ValueName] = self.previous
                Computer.createVariable(self.ValueName,self.previous)
            elif(self.ValueName in Computer.Variables):
                Computer.Variables.pop(self.ValueName)
            self.reset()
    
            return
        #self.internal_variable_ptr.value = self.internal_variable_ptr.value + self.Step
             
    def reset(self):
        self.started = False
        self.StartVal = None
        self.EndVal = None
        self.Step = None
        self.internal_variable_ptr = None

    def HandleError(self):
        self.bValid = False
        Invalid_Syntax()
    
    def get_type(self):
        return 'FOR'

class NEXTObject(DefaultInstructionObject):
    def __init__(self,sCommand,linenumber):

        self.Nextpos = linenumber

        
        self.ValueName = getBetween(sCommand,start='NEXT ').lstrip().rstrip()
        self.sCommand = sCommand
        self.bValid = True
        self.forlineNo = None
    def interpret_command(self):
        if(Computer.Forscope.isEmpty()):
            Computer.runtimeError('Called NEXT outside FOR scope')
        elif(Computer.Forscope.see().ValueName == self.ValueName):
            Computer.Forscope.see().Nextpos = self.Nextpos
            self.forlineNo = Computer.Forscope.pop().linenumber
        else:
            Computer.runtimeError('Called NEXT inside incorrect FOR scope')

    def run(self):



        Computer.setNextInstructionptr(self.forlineNo)

    
    def get_type(self):
        return 'NEXT'

class GOSUBObject(DefaultInstructionObject):
    def __init__(self,sCommand,linenumber):
        self.sCommand = sCommand
        self.linenumber = linenumber
        self.bValid = True
        self.target = None

    def interpret_command(self):
        rest = self.remove_first(self.sCommand)
        try:
            self.target = int(rest)
        except:
            self.HandleError()
            return

    def run(self):
        Computer.ReturnStack.push(self.linenumber)
        if(not Computer.setNextInstructionptr(self.target)):
            Computer.runtimeError(f'GOSUB called for invalid linenumber : {self.target}')
           
    def HandleError(self):
        print('Invalid GOSUB Command')
        self.bValid = False     
            
class RETURNObject(DefaultInstructionObject):
    def __init__(self,sCommand):
        self.sCommand = sCommand
        self.bValid = True
    def run(self):
        if(Computer.ReturnStack.isEmpty()):
            Computer.runtimeError('RETURN called without GOSUB command')
        elif(not Computer.setCurrentInstructionptr(Computer.ReturnStack.pop())):
            Computer.runtimeError('GOSUB command does not exist')
            
class REMObject(DefaultInstructionObject):
    def __init__(self,sCommand):
        self.sCommand = sCommand
        self.bValid = True

    def run(self):
        pass
    def interpret_command(self):
        pass

class DATAObject(DefaultInstructionObject):
    def __init__(self,sCommand):
        self.sCommand = sCommand
        self.bValid = True
        
    def interpret_command(self):
        rest = self.remove_first(self.sCommand)
        if(not self.bValid):
            return
        data = rest.split(",")
        for value in data:
            if(value == ""):
                continue
            try:
                Computer.DataStack.push(float(value))
            except:
                Computer.runtimeError('DATA MUST BE OF TYPE FLOAT')
    def run(self):
        pass

class READObject(DefaultInstructionObject):
    def __init__(self,sCommand):
        self.sCommand = sCommand
        self.bValid = True
    
    def interpret_command(self):
        self.variable_names = [name.lstrip().rstrip() for name in self.remove_first(self.sCommand).split(",")]
        for variable_name in self.variable_names:
            if(not LETOBject.ImposeNamerestriction(variable_name)):
                self.bValid = False
                print('NAME PROVIDED DOESN\'T CONFER WITH THE BASIC STANDERED BEING USED')
                return
    def run(self):
        for variable_name in self.variable_names:
            if(Computer.DataStack.isEmpty()):
                Computer.endProgram('OUT OF DATA')
                return
            else:
                Computer.createVariable(variable_name,VariableType(Computer.DataStack.pop()))

class DEFInlineObject(DefaultInstructionObject):
    def __init__(self,sCommand):
        self.sCommand = sCommand
        self.bValid = True

    def interpret_command(self):
        rest = self.remove_first(self.sCommand)
        if(not self.bValid):
            return False
        self.function_name = getBetween(rest,end='(')
        if(self.function_name == None):
            self.HandleError()
            return
        self.Variable_names = getBetween(rest,start='(',end=')')
        if(self.Variable_names == None):
            self.HandleError()
            return
        
        self.Variable_names = self.Variable_names.split(",")
        self.Expression = getBetween(rest,start="=")
        if(self.Expression == None):
            self.HandleError()
            return
        self.Expression = Expression(self.Expression)
        
        Computer.createVariable(self.function_name,operatortype(self.process))

    def run(self):
        pass
    def process(self,computerstack):
        variable_dic = {}
        for index in range(len(self.Variable_names)-1,-1,-1):
            variable_dic[self.Variable_names[index]] = computerstack.pop()
        with Scope(variable_dic):
            computerstack.push(self.Expression.evaluate())

        

    def HandleError(self,msg=''):
        Computer.runtimeError(f'INVALID INLINE FUNCTION {msg}')

class INPUTObject(DefaultInstructionObject):
    def __init__(self,sCommand):
        self.sCommand = sCommand
        self.bValid = True
    def interpret_command(self):
        rest = self.remove_first(self.sCommand)
        self.variables = rest.split(",")
    def run(self):
        userinput = input('?')
        userinput = userinput.split(',')
        if(len(userinput)!=len(self.variables)):
            self.HandleError()
            return
        for index,variable_name in enumerate(self.variables):
            try:
                val = float(userinput[index])
            except:
                self.HandleError()
                return
            if(not LETOBject.ImposeNamerestriction(variable_name)):
                self.HandleError()
                return
            Computer.createVariable(variable_name,VariableType(val))
        
    def HandleError(self):
        self.bValid = False
        Computer.runtimeError('INVALID INPUT')


def create_function_object(sCommand):
    condition1 = (sCommand.find('DEF') != -1)
    condition2 = (sCommand.find('=') != -1)
    if(condition1 and condition2):
        return DEFInlineObject(sCommand)
    else:
        return DefaultInstructionObject()

def CreateInstructionObject(sCommand,linenumber):
    #Determines the type of command and pass on to various object Constructors
    obj = DefaultInstructionObject()
    Type = getNextWord(sCommand)
        

   
    if(Type == "LET"):
        obj= LETOBject(sCommand)
      
    elif(Type == "PRINT"):
        obj = PRINTObject(sCommand)

    elif(Type == "END"):
        obj = ENDObject(sCommand)
        pass

    elif(Type == "GOTO"):
        obj = GOTOObject(sCommand)

    elif(Type == "IF"):
        obj = IFTHENObject(sCommand)


    elif(Type == "FOR"):
        obj = FORObject(sCommand,linenumber)
    elif(Type == "NEXT"):
        obj = NEXTObject(sCommand,linenumber)

    elif(Type == "GOSUB"):
        obj = GOSUBObject(sCommand,linenumber)      
    elif(Type == "RETURN"):
        obj = RETURNObject(sCommand)

    elif(Type == "DEF"):
        obj = create_function_object(sCommand)
        pass


    elif(Type == "DIM"):
        pass
    elif(Type == "REM"):
        obj = REMObject(sCommand)
    elif(Type == "STOP"):
        pass
    elif(Type == 'DATA'):
        obj = DATAObject(sCommand)
    elif(Type == 'READ'):
        obj = READObject(sCommand)


    elif(Type == 'INPUT'):
        obj = INPUTObject(sCommand)

    else:
        pass
    
    return obj
   
##################################################################
   
def main():
    os.system('cls')
    os.system('color A')
    while True:
        sCommand = input()
        interpretCommand(sCommand)

if __name__ == "__main__":
    main()
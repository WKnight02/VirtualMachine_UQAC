"""
The class Parser
"""

__all__ = ['parser']
text = "     ADD    1      2     3"
textSplit = text.split(" ")
while textSplit.count(''): del textSplit[textSplit.index('')]
prefix , op1, *op2 = textSplit
print (prefix)
# print (op2)

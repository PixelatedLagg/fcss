from libs.fcssParser import fcssParser
from libs.fcssParserVisitor import fcssParserVisitor
from typing import *


unary_operands = {
    '+': lambda x: x,
    '-': lambda x: {'Multiply': {'left': x, 'right': -1}},
    '_': lambda x: {'Floor': x},
    '^': lambda x: {'Ceil': x},
    '!': lambda x: {'Not': x}
}

operations = {
    '**': lambda x, y: {'Power': {'left': x, 'right': y}},
    '*': lambda x, y: {'Multiply': {'left': x, 'right': y}},
    '/': lambda x, y: {'Divide': {'left': x, 'right': y}},
    '%': lambda x, y: {'Modulo': {'left': x, 'right': y}},
    '+': lambda x, y: {'Add': {'left': x, 'right': y}},
    '-': lambda x, y: {'Subtract': {'left': x, 'right': y}},
    '==': lambda x, y: {'Equals': {'left': x, 'right': y}},
    '!=': lambda x, y: {'NotEquals': {'left': x, 'right': y}},
    '>': lambda x, y: {'Greater': {'left': x, 'right': y}},
    '>=': lambda x, y: {'GreaterEquals': {'left': x, 'right': y}},
    '<': lambda x, y: {'Less': {'left': x, 'right': y}},
    '<=': lambda x, y: {'LessEquals': {'left': x, 'right': y}},
    '||': lambda x, y: {'Or': {'left': x, 'right': y}},
    '&&': lambda x, y: {'And': {'left': x, 'right': y}},
}


class fcssVisitor(fcssParserVisitor):
    def visitMain_tree(self, ctx: fcssParser.Main_treeContext):
        if not ctx or not ctx.children:
            return []

        instructions = []

        for child in ctx.children:
            if isinstance(child, fcssParser.SelectorContext):
                instructions.append(self.visitSelector(child))
        
        return instructions

    def visitTree(self, ctx: fcssParser.TreeContext):
        if not ctx or not ctx.children:
            return []

        instructions = []

        for child in ctx.children:
            if isinstance(child, fcssParser.Assign_stmtContext):
                instructions.append(self.visitAssign_stmt(child))

            elif isinstance(child, fcssParser.Append_stmtContext):
                instructions.append(self.visitAppend_stmt(child))

            elif isinstance(child, fcssParser.Conditional_blockContext):
                instructions.append(self.visitConditional_block(child))
            
            elif isinstance(child, fcssParser.SwitchContext):
                instructions.append(self.visitSwitch(child))

        return instructions
    
    ## Visitors for atoms/exprs

    def visitAttribute(self, ctx: fcssParser.AttributeContext):
        attributes = ctx.IDENTIFIER(None)
        return {'Attribute': [attribute.getText() for attribute in attributes]}
    
    def visitFunction_call(self, ctx: fcssParser.Function_callContext):
        attributes = self.visitAttribute(ctx.attribute())

        ## TODO: Function parameters
        return {'Call': {**attributes, 'Parameters': []}}

    def visitAtom(self, ctx: fcssParser.AtomContext):
        if (attr := ctx.attribute()):
            return self.visitAttribute(attr)
        elif (func_c := ctx.function_call()):
            return self.visitFunction_call(func_c)
        elif ctx.NULL():
            return None
        elif (integral := ctx.INTEGRAL()):
            return int(integral.getText())
        elif (double := ctx.DOUBLE()):
            return float(double.getText())
        elif (boolean := ctx.BOOLEAN()):
            if (boolean.getText() == 'true'):
                return True
            return False
        
        return ctx.STRING().getText()[1:-1]

    def visitExpr(self, ctx: fcssParser.ExprContext):
        if not ctx:
            return
        if (atom := ctx.atom()):
            return self.visitAtom(atom)
        
        if (ctx.right and not ctx.left):
            ## unary op used
            return unary_operands[ctx.unary_left.text](self.visitExpr(ctx.right))
        elif not (ctx.right or ctx.left):
            return self.visitExpr(ctx.expr()[0])
        
        op = ctx.op.text
        return operations[op](self.visitExpr(ctx.left), self.visitExpr(ctx.right))

    ## Visitors for statements

    def visitAssign_stmt(self, ctx: fcssParser.Assign_stmtContext):
        attributes = self.visitAttribute(ctx.attribute())
        return {'Assign': {'Name': attributes, 'Value': self.visitExpr(ctx.expr())}}
    
    def visitAppend_stmt(self, ctx: fcssParser.Append_stmtContext):
        attributes = self.visitAttribute(ctx.attribute())
        expr = self.visitExpr(ctx.expr())

        op = ctx.op.text
        if (op == '+='):
            return {'Assign': {'Name': attributes, 
                               'Value': {'Add': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '-='):
            return {'Assign': {'Name': attributes, 
                               'Value': {'Subtract': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '*='):
            return {'Assign': {'Name': attributes, 
                               'Value': {'Multiply': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '/='):
            return {'Assign': {'Name': attributes, 
                               'Value': {'Divide': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '**='):
            return {'Assign': {'Name': attributes, 
                               'Value': {'Power': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '%='):
            return {'Assign': {'Name': attributes, 
                               'Value': {'Modulo': {'left': attributes, 'right': expr}}
                              }
                   }
        raise ValueError('Unknown appendage operation')
    
    def visitIf_stmt(self, ctx: fcssParser.If_stmtContext):
        expr = self.visitExpr(ctx.expr())
        instructions = self.visitTree(ctx.tree())

        return {'If': {'Condition': expr, 'Instructions': instructions}}
    
    def visitElse_if_stmt(self, ctx: fcssParser.Else_if_stmtContext):
        expr = self.visitExpr(ctx.expr())
        instructions = self.visitTree(ctx.tree())

        return {'ElseIf': {'Condition': expr, 'Instructions': instructions}}
    
    def visitElse_stmt(self, ctx: fcssParser.Else_stmtContext):
        instructions = self.visitTree(ctx.tree())

        return {'Else': {'Instructions': instructions}}
    
    def visitConditional_block(self, ctx: fcssParser.Conditional_blockContext):
        instr = {'ConditionalBlock': 
                    {**self.visitIf_stmt(ctx.if_stmt()), 'ElseIfs': [], 'Else': None}
                }
        
        if (else_ifs := ctx.else_if_stmt()):
            for stmt in else_ifs:
                instr['ConditionalBlock']['ElseIfs'].append(self.visitElse_if_stmt(stmt))
        
        if (else_stmt := ctx.else_stmt()):
            instr['ConditionalBlock']['Else'] = self.visitElse_stmt(else_stmt)
        return instr
    
    ## Visitors for selectors

    def visitSelector_name(self, ctx: fcssParser.Selector_nameContext):
        if not ctx:
            return

        if ctx.token:
            if ctx.token.text == '.':
                return {'Class': ctx.IDENTIFIER().getText()}
            return {'Id': ctx.IDENTIFIER().getText()}

        elif ctx.wildcard:
            return {'WildCard': ctx.wildcard.text}
        return {'Element': ctx.IDENTIFIER().getText()}
    
    def visitSelector_pattern(self, ctx: fcssParser.Selector_patternContext):
        ## Helps deal with recursive stops
        if isinstance(ctx, dict):
            return ctx

        if ctx.unary:
            return {'Not': self.visitSelector_name(*ctx.selector_name())}
        
        if not ctx.operand:
            if pat := ctx.selector_pattern():
                if len(pat) > 1:
                    return self.visitManySelector_pattern(pat)
                return self.visitSelector_pattern(pat[0])
            return self.visitSelector_name(ctx.selector_name())
        
        left, _, *children = ctx.children
        left = self.visitSelector_pattern(left)
        if len(children) == 1:
            right = self.visitSelector_pattern(children[0])
            if ctx.operand.text == '||':
                return {'Or': {'left': left, 'right': right}}
            return {'And': {'left': left, 'right': right}}
        
        raise RuntimeError('Something went wrong here')

    def visitManySelector_pattern(self, ctx: List[fcssParser.Selector_patternContext]):
        paths = []

        for path in ctx:
            paths.append(self.visitSelector_pattern(path))
        return {'Paths': paths}
    
    def visitSelector(self, ctx: fcssParser.SelectorContext):
        selector = self.visitManySelector_pattern(ctx.selector_pattern())
        instructions = self.visitTree(ctx.tree())
        event = getattr(ctx.IDENTIFIER(), 'text', None) or 'init'

        return {'Selector': {**selector, 'Instructions': instructions, 'Event': event}}
    
    ## Switch case

    def visitCase(self, ctx: fcssParser.CaseContext):
        e = ctx.expr()
        if not e:
            expr = '$NoMatch'
        else:
            expr = self.visitExpr(e)
        tree = self.visitTree(ctx.tree())

        return {'Case': {'Condition': expr, 'Instructions': tree}}
    
    def visitSwitch(self, ctx: fcssParser.SwitchContext):
        expr = self.visitExpr(ctx.expr())
        cases = []
        c_n = []        ## Validate whether 2 no expression cases are given

        if (l := ctx.case()):
            for case in l:
                i = self.visitCase(case)
                if i['Case']['Condition'] in c_n:
                    raise ValueError(f'Repeated case condition: {i["Case"]["Condition"]}')
                c_n.append(i['Case']['Condition'])

                cases.append(i)
        return {'Switch': {'Condition': expr, 'Cases': cases}}

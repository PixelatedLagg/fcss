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
        instructions = []

        for child in ctx.children:
            if isinstance(child, fcssParser.SelectorContext):
                instructions.append(self.visitSelector(child))
        
        return instructions

    def visitTree(self, ctx: fcssParser.TreeContext):
        if not ctx:
            return []

        instructions = []

        for child in ctx.children:
            child_class = child.__class__
            if child_class == fcssParser.Assign_stmtContext:
                instructions.append(self.visitAssign_stmt(child))
            elif child_class == fcssParser.Append_stmtContext:
                instructions.append(self.visitAppend_stmt(child))
            elif child_class == fcssParser.Conditional_blockContext:
                instructions.append(self.visitConditional_block(child))

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
        return {'Assign': {'name': attributes, 'value': self.visitExpr(ctx.expr())}}
    
    def visitAppend_stmt(self, ctx: fcssParser.Append_stmtContext):
        attributes = self.visitAttribute(ctx.attribute())
        expr = self.visitExpr(ctx.expr())

        op = ctx.op.text
        if (op == '+='):
            return {'Assign': {'name': attributes, 
                               'value': {'Add': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '-='):
            return {'Assign': {'name': attributes, 
                               'value': {'Subtract': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '*='):
            return {'Assign': {'name': attributes, 
                               'value': {'Multiply': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '/='):
            return {'Assign': {'name': attributes, 
                               'value': {'Divide': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '**='):
            return {'Assign': {'name': attributes, 
                               'value': {'Power': {'left': attributes, 'right': expr}}
                              }
                   }
        elif (op == '%='):
            return {'Assign': {'name': attributes, 
                               'value': {'Modulo': {'left': attributes, 'right': expr}}
                              }
                   }
        raise ValueError('Unknown appendage operation')
    
    def visitIf_stmt(self, ctx: fcssParser.If_stmtContext):
        expr = self.visitExpr(ctx.expr())
        instructions = self.visitTree(ctx.tree())

        return {'If': {'condition': expr, 'instructions': instructions}}
    
    def visitElse_if_stmt(self, ctx: fcssParser.Else_if_stmtContext):
        expr = self.visitExpr(ctx.expr())
        instructions = self.visitTree(ctx.tree())

        return {'ElseIf': {'condition': expr, 'instructions': instructions}}
    
    def visitElse_stmt(self, ctx: fcssParser.Else_stmtContext):
        instructions = self.visitTree(ctx.tree())

        return {'Else': {'instructions': instructions}}
    
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
        if ctx.token:
            if ctx.token.text == '.':
                return {'id': ctx.IDENTIFIER().getText()}
            return {'class': ctx.IDENTIFIER().getText()}

        elif ctx.wildcard:
            return {'wildcard': ctx.wildcard.text}
        return {'element': ctx.IDENTIFIER().getText()}
    
    def visitSelector_pattern(self, ctx: fcssParser.Selector_patternContext):
        if ctx.unary:
            return {'Not': self.visitSelector_name(*ctx.selector_name())}
        
        if not ctx.operand:
            return self.visitSelector_name(*ctx.selector_name())
        
        left, right = map(self.visitSelector_name, ctx.selector_name())
        if ctx.operand.text == '||':
            return {'Or': [left, right]}
        return {'And': [left, right]}

    def visitManySelector_pattern(self, ctx: List[fcssParser.Selector_patternContext]):
        paths = []

        for path in ctx:
            paths.append(self.visitSelector_pattern(path))
        return {'Paths': paths}
    
    def visitSelector(self, ctx: fcssParser.SelectorContext):
        selector = self.visitManySelector_pattern(ctx.selector_pattern())
        instructions = self.visitTree(ctx.tree())

        return {'Selector': {**selector, 'Instructions': instructions}}

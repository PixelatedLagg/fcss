#include <string>
#include "antlr4-runtime.h"
#include "fcssParserBaseVisitor.h"
#include "fcssNodes.h"


namespace fcss::Parser {

    class NodeVisitor : fcssParserVisitor {

        public:

            std::any visitAttr(fcssParser::AttrContext *ctx);

            std::any visitName_or_attr(fcssParser::Name_or_attrContext *ctx);

            std::any visitAssign_stmt(fcssParser::Assign_stmtContext *ctx);

            std::any visitIf_stmt(fcssParser::If_stmtContext *ctx);

            std::any visitElse_if_stmt(fcssParser::Else_if_stmtContext *ctx);

            std::any visitElse_stmt(fcssParser::Else_stmtContext *ctx);

            std::any visitBlock(fcssParser::BlockContext *ctx);

            std::any visitSelector_type(fcssParser::Selector_typeContext *ctx);

            std::any visitSelector(fcssParser::SelectorContext *ctx);

            std::any visitSelector_meth(fcssParser::Selector_methContext *ctx);

            std::any visitGeneric_style(fcssParser::Generic_styleContext *ctx);

            std::any visitParameters(fcssParser::ParametersContext *ctx);

            std::any visitArgslist(fcssParser::ArgslistContext *ctx);

            std::any visitParam_spec(fcssParser::Param_specContext *ctx);

            std::any visitPassable_arglist(fcssParser::Passable_arglistContext *ctx);

            std::any visitAtoms(fcssParser::AtomsContext *ctx);

            std::any visitExpr(fcssParser::ExprContext *ctx);
    };
}

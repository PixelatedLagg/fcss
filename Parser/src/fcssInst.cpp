#include "fcssInst.h"

namespace fcss::Instructions {

    Assign::Assign(std::string Name, std::any Value) {
        this->Name = Name;
        this->Value = Value;
    }

}

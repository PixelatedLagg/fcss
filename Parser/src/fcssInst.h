#include <iostream>
#include <any>
#include <string>


namespace fcss::Instructions {

    class Assign {

        public:
            std::string Name;
            std::any Value;

            Assign(std::string Name, std::any Value);
    };

}

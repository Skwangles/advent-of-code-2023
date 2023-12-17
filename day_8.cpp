#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <numeric>

// https://adventofcode.com/2023/day/8
// This challenge requires exploring a map based on Nodes with children IDs (which refer to other nodes)
// This continues until a value ending with 'Z' returns.

int main(int argc, char const *argv[]);

class TreeChilds {
    public:
    std::string left;
    std::string right;

    TreeChilds(std::string leftstr, std::string rightstr){
        left = leftstr;
        right = rightstr;
    }
};

bool all_at_z(std::vector<std::string> current){
    for (int i = 0; i < current.size(); i++){
        if (current[i][2] != 'Z') return false;
    }
    return true;
}

int main(int argc, char const *argv[])
{
    bool isFirst = true;
    std::ifstream myfile ("input");
    std::string instructions;
    std::string mystring;
    std::map<std::string, TreeChilds> nodes;
    std::vector<std::string> current_states;

    // Parsing
    if (myfile.is_open())
    {

        while (myfile) {
            std::getline (myfile, mystring);
            if (isFirst){
                instructions = mystring;
                isFirst = false;
            }
            else 
            {
                // Handle '' empty line
                if (mystring.length() == 0) continue;

                std::string id = mystring.substr(0, 3);
                if (id[2] == 'A'){
                    current_states.push_back(id);
                }
                std::string left =  mystring.substr(7, 3);
                std::string right = mystring.substr(12, 3);
                
                TreeChilds childs(left, right);
                nodes.insert(std::pair<std::string, TreeChilds>(id, childs));
            }
        }
        std::cout << instructions << std::endl;
        std::cout << "First " << nodes.begin()->first << std::endl;
    }


    // Loop through instructions
    int64_t result = 1;
    for (int i = 0; i < current_states.size(); i++)
    {
        // Theory: Each individual entry point XXA has a cycle - little bit of a logical jump gleaned from observing the dataset.
        // LCM of all cycles == total steps needed to match up

        int step_count = 0;
        while(current_states[i][2] != 'Z')
        {
            // Take another step
            if (instructions[step_count % instructions.length()] == 'L'){
                current_states[i] = nodes.at(current_states[i]).left;
            }
            else {
                current_states[i] = nodes.at(current_states[i]).right;
            }
            step_count++;
        }
        result = std::lcm(result, step_count);
    }
    std::cout << "Steps:" << result << std::endl;
    return 0;
}

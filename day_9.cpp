#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <numeric>
#include <sstream>

// https://adventofcode.com/2023/day/9

int main(int argc, char const *argv[]);

bool is_all_zero(std::vector<int> hist){
    for (int i = 0; i < hist.size(); i++){
        if (hist[i] != 0) 
            return false; 
    }
    return true;
}

int predict(std::vector<int> hist)
{
    if (is_all_zero(hist)){
        return 0;
    }

    std::vector<int> next_lvl;
    for (int i = 0; i < hist.size() - 1 ; i++){
        next_lvl.push_back(hist[i+1] - hist[i]);
    }
    return hist[0] - predict(next_lvl);
}

int main(int argc, char const *argv[])
{
    bool isFirst = true;
    std::ifstream myfile ("input");
    std::string instructions;
    std::string mystring;
    
    std::vector<int> predictions;

    // Parsing
    if (myfile.is_open())
    {
        
        while (myfile) {
            std::getline (myfile, mystring);
            std::string number_str;
            std::stringstream ss (mystring);

            std::vector<int> diffs;

            while (std::getline(ss, number_str, ' ')){
                diffs.push_back(std::stoi(number_str));
            }
            predictions.push_back(predict(diffs));
        }
    }





    // Recursively create arr
    // pass new arr
    //
    int64_t sum_of_elems = 0;

     for(std::vector<int>::iterator it = predictions.begin(); it != predictions.end(); ++it)
        sum_of_elems += *it;

    std::cout << "Steps:" << sum_of_elems << std::endl;
    return 0;
}

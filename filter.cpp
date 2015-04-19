#include <iostream>
#include <fstream>
#include <unordered_set>

int main () {
    std::unordered_set<std::string> companies;
    std::string line;
    std::ifstream company_id_file("data/ids.txt");
    std::string cur_id;
    int start, end;
    if (company_id_file.is_open()) {
        while (getline(company_id_file, line)) {
            companies.insert(line);
        }
        company_id_file.close();
    }
    while (std::getline(std::cin, line)) {
        start = line.find("curid=") + 6;
        end = line.find("\t");
        cur_id = line.substr(start, end-start);
        if (companies.find(cur_id) != companies.end()) {
            std::cout << line << '\n';
        }
    }

}

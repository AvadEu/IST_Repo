#include <vector>
#include <string>
#include <fstream>
#include "Tree.h"
#include "Result.h"
#include "Error.h"

#ifndef L4_FILEWRITER_H
#define L4_FILEWRITER_H

class FileWriter {
public:
  template <typename T, typename E>
  static void vSaveToFile(Result<T, E>& res, std::string sFileName) {
    std::ofstream fFile(sFileName.c_str(), std::ios::app);
    if (fFile.is_open()) {
      if (!res.isSuccess()) {
        fFile << "Errors:\n";
        std::vector<E*>& vErrs = res.getErrors();
        for (size_t i = 0; i < vErrs.size(); i++) {
          fFile << vErrs[i]->getMsg() << "\n";
        }
      } else {
        fFile << res.getValue().toString() << "\n";
      }
      fFile.close();
    }
  }

  template <typename E>
  static void vSaveToFile(Result<Tree*, E>& res, std::string sFileName) {
    std::ofstream fFile(sFileName.c_str(), std::ios::app);
    if (fFile.is_open()) {
      if (!res.isSuccess()) {
        fFile << "Errors:\n";
        std::vector<E*>& vErrs = res.getErrors();
        for (size_t i = 0; i < vErrs.size(); i++) {
          fFile << vErrs[i]->getMsg() << "\n";
        }
      } else {
        fFile << "Success: " << res.getValue()->toString() << "\n";
      }
      fFile.close();
    }
  }
};

#endif //L4_FILEWRITER_H
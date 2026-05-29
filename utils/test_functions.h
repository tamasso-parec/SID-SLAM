//
// Created by font_al on 10/8/18.
//

#ifndef TEST_FUNCTIONS_H
#define TEST_FUNCTIONS_H

#include "definesAndIncludes.h"

namespace IDNav {

    // debug point
    inline void dp(int i){
        std::cout << "DEBUG POINT: " << i << std::endl;
    }

    // wait function. Disabled by default because these are interactive debug
    // breakpoints that stop batch evaluation runs.
    inline void wf(const std::string& expectedInput){
        if(!std::getenv("SID_SLAM_ENABLE_WAITS")) return;

        std::string input;

        std::cout << "Continue("<< expectedInput << ")?: " << std::endl;
        std::cin >> input;

        while (input != expectedInput) {
            std::cout << "Continue("<< expectedInput << ")?: " << std::endl;
            std::cin >> input;
        }
    }
}

#endif //TEST_FUNCTIONS_H

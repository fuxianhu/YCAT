/*

算法相关的主文件，用于统一调用所有算法功能

*/

// 考虑到部分编译器没有bits/stdc++.h，所以加到了/src/header/stdc++.h中
#define bits / stdc++.h header / stdc++.h

# include "bits/stdc++.h"
# include "algebra.hpp"



int main(int argc, char *argv[])
{
    // std::cout << "Hello World!" << std::endl;
    // auto start = std::chrono::high_resolution_clock::now();
    Find_GCD_LCM gcd_lcm;
    gcd_lcm.get_all("../user/input.in", "../user/output.out");
    // auto end = std::chrono::high_resolution_clock::now();

    // // 计算时间差（毫秒）
    // auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    // std::cout << "耗时: " << duration.count() << " 毫秒" << std::endl;
    return 0;
}
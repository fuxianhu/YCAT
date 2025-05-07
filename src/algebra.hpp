/*

代数

请忽略以下错误：
namespace "std" has no member "gcd"C/C++(135)
namespace "std" has no member "lcm"C/C++(135)


*/



# include <numeric> // for std::gcd and std::lcm (C++17)
# include <chrono>


class Find_GCD_LCM
{
    /*
     * 求最大公约数和最小公倍数
     */
public:
    void get_gcd(std::string input_file, std::string output_file, std::string segmentation = "\n")
    {
        freopen(input_file.c_str(), "r", stdin);
        freopen(output_file.c_str(), "w", stdout);
        long long a, b;
        while (true)
        {
            scanf("%lld", &a);
            if (a < 0)
            {
                return;
            }
            scanf("%lld", &b);
            if (b < 0)
            {
                return;
            }
            printf("%lld%s", std::gcd(a, b), segmentation);
        }
        fclose(stdin);
        fclose(stdout);
    }
    void get_lcm(std::string input_file, std::string output_file, std::string segmentation = "\n")
    {
        freopen(input_file.c_str(), "r", stdin);
        freopen(output_file.c_str(), "w", stdout);
        long long a, b;
        while (true)
        {
            scanf("%lld", &a);
            if (a < 0)
            {
                return;
            }
            scanf("%lld", &b);
            if (b < 0)
            {
                return;
            }
        }
        printf("%lld%s", std::lcm(a, b), segmentation);
        fclose(stdin);
        fclose(stdout);
    }
    void get_all(std::string input_file, std::string output_file)
    {
        freopen(input_file.c_str(), "r", stdin);
        freopen(output_file.c_str(), "w", stdout);
        putchar('g'), putchar('c'), putchar('d'), putchar(' '), putchar('|'), putchar(' ');
        putchar('l'), putchar('c'), putchar('m'), putchar('\n');
        long long a, b;
        while (true)
        {
            scanf("%lld", &a);
            if (a < 0)
            {
                return;
            }
            scanf("%lld", &b);
            if (b < 0)
            {
                return;
            }
            printf("%lld %lld\n", std::gcd(a, b), std::lcm(a, b));
        }
        fclose(stdin);
        fclose(stdout);
    }
};

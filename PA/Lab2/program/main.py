from test import Test


def main():
    x = 1
    while x != '0':
        print('Select an algorithm(LDFS - 1, A Star - 2): ')
        x = input()
        if x=='0':
            break
        print('Choose the number of tests: ')
        n = input()
        tester = Test()
        if x=='1':
            tester.test_ldfs(int(n))
        if x=='2':
            tester.test_astar(int(n))


if __name__ == "__main__":
    main()
# 定义一个全局变量
global_variable = "I am a global variable"

def function1():
    # 在函数中使用全局变量
    print("Inside function1:", global_variable)

def function2():
    # 修改全局变量的值
    global global_variable
    global_variable = "Modified global variable"

# 调用函数1
function1()

# 调用函数2
function2()

# 在主程序中使用修改后的全局变量
print("Outside any function:", global_variable)

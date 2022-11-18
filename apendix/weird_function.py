# weird_function.py
# 
# Create function that will have next result:
#     print(super_weird_sum(5)())           -> 5
#     print(super_weird_sum(5)(3)())        -> 8
#     print(super_weird_sum(5)(4)(-10)())   -> -1

# 1
# def super_weird_sum(value):
#     inner_lst = [value]

#     def inner_fun(arg=0):
#         if arg:
#             inner_lst.append(arg)
#             return inner_fun
#         else:
#             return sum(inner_lst)
#     return inner_fun    

# 2 Без if
# def super_weird_sum(value):
#     inner_lst = [value]

#     def inner_fun(arg=None):
#         cases = {None: sum(inner_lst)}
#         inner_lst.append(arg)
#         return cases.get(arg, inner_fun)

#     return inner_fun    

# 3 без списка, але із nonlocal
# def super_weird_sum(value):
#     inner_sum = value

#     def inner_fun(arg=None):
#         nonlocal inner_sum
#         cases = {None: inner_sum}
#         inner_sum += arg or 0
#         return cases.get(arg, inner_fun)

#     return inner_fun    

# # 4 - без nonlocal, functools.partial
# from functools import partial


# def super_weird_sum(value):

#     def inner_fun(arg=None, keep_sum=0):
#         keep_sum += arg or 0
#         cases = {None: keep_sum}
#         return cases.get(arg, partial(inner_fun, keep_sum=keep_sum))

#     return partial(inner_fun, keep_sum=value)    

# 5 - partial без functools
# def super_weird_sum(value):

#     def partial(func, *part_args):
#         def wrapper(*extra_args):
#             args = list(part_args)
#             args.extend(extra_args)
#             return func(*args) if extra_args else part_args[0]

#         return wrapper

#     def inner_fun(*args):
#         return partial(inner_fun, sum(args))

#     return partial(inner_fun, value)    

# 6 - partial без functools, тільки 1 аргумент
def super_weird_sum(value):

    def partial(func, *part_args):
        def wrapper(*extra_args):
            args = list(part_args)
            if extra_args:
                args.extend([extra_args[0]])
                return func(*args)
            return part_args[0]

        return wrapper

    def inner_fun(*args):
        return partial(inner_fun, sum(args))

    return partial(inner_fun, value)    


if __name__ == "__main__":
    print(f"super_weird_sum(5)(4)(-10)() = {super_weird_sum(5)(4)(-10)()}")
    print(f"super_weird_sum(5)() = {super_weird_sum(5)()}")
    print(f"super_weird_sum(5)(3)() = {super_weird_sum(5)(3)()}")
    print(f"super_weird_sum(5)(3, 1000)() = {super_weird_sum(5)(3, 1000)()}")
    print(f"super_weird_sum(5)(4)(-10)(11)() = "
          f"{super_weird_sum(5)(4)(-10)(11)()}")

    assert super_weird_sum(5)() == 5, "super_weird_sum(5)() must be the 5"
    assert super_weird_sum(5)(3)() == 8, \
        "super_weird_sum(5)(3)()} must be the 8"
    assert super_weird_sum(5)(4)(-10)() == -1, \
        "super_weird_sum(5)(4)(-10)() must be the -1"
    assert super_weird_sum(5)(4)(-10)(11)() == 10, \
        "super_weird_sum(5)(4)(-10)(11)()} must be the 10"

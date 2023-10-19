
! 子程序没有返回值，但可以修改其参数。
! 需要使用call语句来调用一个子程序。
! 下面的例子演示了一个子程序交换，改变其参数值的定义和使用。
subroutine swap(x, y) 
    implicit none
    real :: x, y, temp

    temp = x
    x = y 
    y = temp

end subroutine swap


program calling_func
    implicit none
    real :: a, b
    a = 2.0
    b = 3.0

    Print *, "Before calling swap"
    Print *, "a = ", a
    Print *, "b = ", b

    call swap(a, b)

    Print *, "After calling swap"
    Print *, "a = ", a
    Print *, "b = ", b
   
end program calling_func



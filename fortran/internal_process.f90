
! 当一个过程被包含在程序中，它被称为程序的内部程序

program mainprog
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

contains
    subroutine swap(x, y)
        real :: x, y, temp
        temp = x 
        x = y  
        y = temp   
    end subroutine swap 

end program mainprog

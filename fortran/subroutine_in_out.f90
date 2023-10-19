
! 意图属性允许指定与参数的过程中使用的意向。下表提供intent属性的值：
! 值      使用为                解释
! in      intent(in)          参数是输入参数。该过程不能修改参数的值。
! out     intent(out)         参数是输出参数。该过程可以修改参数的值。
! inout   intent(inout)       参数是输入/输出参数。该过程可以修改参数的值。

program calling_func
    implicit none

    real :: x, y, z, disc

    x= 1.0
    y = 5.0
    z = 2.0

    call intent_example(x, y, z, disc)

    Print *, "The value of the discriminant is"
    Print *, disc

end program calling_func


subroutine intent_example (a, b, c, d)     
    implicit none     

    ! dummy arguments      
    real, intent (in) :: a     
    real, intent (in) :: b      
    real, intent (in) :: c    
    real, intent (out) :: d   

    d = b * b - 4.0 * a * c 

end subroutine intent_example

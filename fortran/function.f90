
! this function computes the area of a circle with radius r  
function area_of_circle(r)
implicit none      

    real :: area_of_circle       ! function name
    ! local variables 
    real :: r
    real :: pi

    pi = 4 * atan (1.0)
    area_of_circle = pi * r**2

end function area_of_circle



! 函数是返回一个数量的过程。函数不修改其参数。
! 返回数值被称为函数值，并将其表示为函数名
function area_of_circle_result(r) result(area_of_circle)
implicit none
    real :: area_of_circle
    real :: r
    real :: pi

    pi = 4 * atan (1.0)     
    area_of_circle = pi * r**2  

end function area_of_circle_result


program calling_func
    real :: a, b
    a = area_of_circle(2.0) 
    b = area_of_circle_result(2.0)

    Print *, "The area of a circle with radius 2.0 is"
    Print *, a
    Print *, b
end program calling_func








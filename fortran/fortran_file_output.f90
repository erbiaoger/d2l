
! 这个例子演示了写一些数据到一个新的打开文件
! 它创建文件data1.dat和x和y数组值写入到其中。然后关闭该文件

program outputdata
implicit none

    real, dimension(100) :: x, y  
    real, dimension(100) :: p, q
    integer :: i  

    ! data  
    do i=1,100  
        x(i) = i * 0.1 
        y(i) = sin(x(i)) * (1-cos(x(i)/3.0))  
    end do  

    ! output data into a file 
    ! 单元数u可以是任何数量范围内9-99，它表明该文件，可以选择任何号码，但在程序中每一个打开的文件必须有一个唯一的数字
    open(1, file='data1.dat', status='new')  
        do i=1,100  
            write(1,*) x(i), y(i)   
        end do  
    close(1) 

end program outputdata
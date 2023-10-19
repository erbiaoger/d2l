# myString <- "RUNOOB"

# print(myString)


# 定义函数 f
f = function (x) {
    if (x >= 0) {
        x
    } else {
        x ^ 2
    }
}

# 生成自变量序列
x = seq(-2, 2, length=100)

# 生成因变量序列
y = rep(0, length(x))
j = 1
for (i in x) {
    y[j] = f(i)
    j = j + 1
}

# 绘制图像
plot(x, y, type='l')
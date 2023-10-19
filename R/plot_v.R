# 向量数据
v <- c(7,12,28,3,41)

# 生成图片
png(file = "line_chart_label_colored.jpg")

# 绘图、线图颜色为红色，main 参数用于设置标题
plot(v,type = "o", col = "red", xlab = "Month", ylab = "Rain fall",
    main = "Rain fall chart")